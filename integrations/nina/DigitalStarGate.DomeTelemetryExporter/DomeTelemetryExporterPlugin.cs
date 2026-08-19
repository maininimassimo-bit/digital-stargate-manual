using NINA.Equipment.Equipment.MyDome;
using NINA.Equipment.Interfaces;
using NINA.Equipment.Interfaces.Mediator;
using NINA.Plugin;
using NINA.Plugin.Interfaces;
using System;
using System.Collections.Generic;
using System.ComponentModel.Composition;
using System.Globalization;
using System.IO;
using System.Reflection;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace DigitalStarGate.Nina.DomeTelemetryExporter;

/*
 * Digital StarGate Observatory Telemetry Exporter
 * Author: Massimo Mainini
 *
 * Read-only services monitored for Observatory Status:
 * - Dome / roll-off roof: connection and shutter state through IDomeMediator.
 * - Mount: connection, park/home/tracking state through ITelescopeMediator.
 * - Imaging camera: connection and available runtime temperature/exposure state through ICameraMediator.
 * - Weather: connection and available observing-condition metrics through IWeatherDataMediator.
 * - Safety Monitor: connection and observed IsSafe state through ISafetyMonitorMediator.
 * - Power: reserved in the unified contract; remains UNKNOWN until a verified power source is approved.
 * - Network: reserved in the unified contract; remains UNKNOWN until a verified network source is approved.
 *
 * The exporter never connects or disconnects equipment, never sends device commands and never acts as
 * a safety authority. It only reads snapshots already owned by N.I.N.A. and writes a local JSON projection.
 */
[Export(typeof(IPluginManifest))]
public sealed class DomeTelemetryExporterPlugin : PluginBase, IDomeConsumer {
    private const int ProjectionIntervalSeconds = 5;

    private readonly IDomeMediator domeMediator;
    private readonly ITelescopeMediator telescopeMediator;
    private readonly ICameraMediator cameraMediator;
    private readonly IWeatherDataMediator weatherDataMediator;
    private readonly ISafetyMonitorMediator safetyMonitorMediator;
    private readonly string projectionPath;
    private readonly object writeLock = new();
    private readonly Timer projectionTimer;
    private bool disposed;

    [ImportingConstructor]
    public DomeTelemetryExporterPlugin(
        IDomeMediator domeMediator,
        ITelescopeMediator telescopeMediator,
        ICameraMediator cameraMediator,
        IWeatherDataMediator weatherDataMediator,
        ISafetyMonitorMediator safetyMonitorMediator) {

        this.domeMediator = domeMediator ?? throw new ArgumentNullException(nameof(domeMediator));
        this.telescopeMediator = telescopeMediator ?? throw new ArgumentNullException(nameof(telescopeMediator));
        this.cameraMediator = cameraMediator ?? throw new ArgumentNullException(nameof(cameraMediator));
        this.weatherDataMediator = weatherDataMediator ?? throw new ArgumentNullException(nameof(weatherDataMediator));
        this.safetyMonitorMediator = safetyMonitorMediator ?? throw new ArgumentNullException(nameof(safetyMonitorMediator));

        var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        projectionPath = Path.Combine(localAppData, "DigitalStarGate", "telemetry", "nina-observatory-status.json");

        domeMediator.RegisterConsumer(this);
        projectionTimer = new Timer(_ => TryWriteProjection(), null, TimeSpan.Zero, TimeSpan.FromSeconds(ProjectionIntervalSeconds));
    }

    public void UpdateDeviceInfo(DomeInfo deviceInfo) {
        if (!disposed) {
            TryWriteProjection();
        }
    }

    public override Task Teardown() {
        Dispose();
        return base.Teardown();
    }

    public void Dispose() {
        if (disposed) {
            return;
        }

        disposed = true;
        projectionTimer.Dispose();

        try {
            domeMediator.RemoveConsumer(this);
        } catch {
            // Teardown is best-effort and must never interfere with N.I.N.A. shutdown.
        }
    }

    private void TryWriteProjection() {
        if (disposed) {
            return;
        }

        try {
            lock (writeLock) {
                WriteProjection();
            }
        } catch {
            // Telemetry is non-authoritative. A write/read failure ages naturally to stale/UNKNOWN outside N.I.N.A.
        }
    }

    private void WriteProjection() {
        var observedAtUtc = DateTime.UtcNow;
        var domeInfo = SafeGetInfo(domeMediator);
        var telescopeInfo = SafeGetInfo(telescopeMediator);
        var cameraInfo = SafeGetInfo(cameraMediator);
        var weatherInfo = SafeGetInfo(weatherDataMediator);
        var safetyInfo = SafeGetInfo(safetyMonitorMediator);

        var payload = new Dictionary<string, object> {
            { "schemaVersion", 2 },
            { "source", "nina-observatory-telemetry-exporter" },
            { "author", "Massimo Mainini" },
            { "observedAtUtc", observedAtUtc.ToString("o") },
            { "services", new Dictionary<string, object> {
                { "dome", BuildDome(domeInfo) },
                { "mount", BuildMount(telescopeInfo) },
                { "camera", BuildCamera(cameraInfo) },
                { "weather", BuildWeather(weatherInfo) },
                { "safety", BuildSafety(safetyInfo) },
                { "power", BuildUnavailable("NO_VERIFIED_POWER_SOURCE") },
                { "network", BuildUnavailable("NO_VERIFIED_NETWORK_SOURCE") }
            }}
        };

        WriteJsonAtomically(projectionPath, JsonSerializer.Serialize(payload));
    }

    private static object SafeGetInfo(object mediator) {
        try {
            return mediator.GetType().GetMethod("GetInfo", BindingFlags.Instance | BindingFlags.Public)?.Invoke(mediator, null);
        } catch {
            return null;
        }
    }

    private static Dictionary<string, object> BuildDome(object info) {
        var connected = ReadBool(info, "Connected");
        var raw = ReadString(info, "ShutterStatus");
        var state = connected == true ? MapDomeState(raw) : "UNKNOWN";
        return BuildService(connected, state, connected == true ? null : "DOME_DISCONNECTED", new Dictionary<string, object> {
            { "rawShutterStatus", raw }
        });
    }

    private static Dictionary<string, object> BuildMount(object info) {
        var connected = ReadBool(info, "Connected");
        var atPark = ReadBool(info, "AtPark");
        var atHome = ReadBool(info, "AtHome");
        var tracking = ReadBool(info, "TrackingEnabled", "Tracking");

        var state = "UNKNOWN";
        if (connected == true) {
            state = atPark == true ? "PARKED" : atHome == true ? "HOME" : tracking == true ? "TRACKING" : "IDLE";
        }

        return BuildService(connected, state, connected == true ? null : "MOUNT_DISCONNECTED", new Dictionary<string, object> {
            { "atPark", atPark },
            { "atHome", atHome },
            { "tracking", tracking },
            { "sideOfPier", ReadString(info, "SideOfPier") }
        });
    }

    private static Dictionary<string, object> BuildCamera(object info) {
        var connected = ReadBool(info, "Connected");
        var exposing = ReadBool(info, "IsExposing", "Exposing");
        var state = connected == true ? (exposing == true ? "EXPOSING" : "READY") : "UNKNOWN";

        return BuildService(connected, state, connected == true ? null : "CAMERA_DISCONNECTED", new Dictionary<string, object> {
            { "temperatureC", ReadDouble(info, "Temperature", "CCDTemperature", "SensorTemperature") },
            { "coolerOn", ReadBool(info, "CoolerOn") },
            { "coolerPowerPct", ReadDouble(info, "CoolerPower") },
            { "exposing", exposing }
        });
    }

    private static Dictionary<string, object> BuildWeather(object info) {
        var connected = ReadBool(info, "Connected");
        var state = connected == true ? "AVAILABLE" : "UNKNOWN";

        return BuildService(connected, state, connected == true ? null : "WEATHER_DISCONNECTED", new Dictionary<string, object> {
            { "temperatureC", ReadDouble(info, "Temperature") },
            { "humidityPct", ReadDouble(info, "Humidity") },
            { "dewPointC", ReadDouble(info, "DewPoint") },
            { "windSpeed", ReadDouble(info, "WindSpeed") },
            { "windGust", ReadDouble(info, "WindGust") },
            { "pressure", ReadDouble(info, "Pressure") },
            { "cloudCoverPct", ReadDouble(info, "CloudCover") },
            { "rainRate", ReadDouble(info, "RainRate") },
            { "skyTemperatureC", ReadDouble(info, "SkyTemperature") }
        });
    }

    private static Dictionary<string, object> BuildSafety(object info) {
        var connected = ReadBool(info, "Connected");
        var isSafe = ReadBool(info, "IsSafe");
        var state = connected == true && isSafe.HasValue ? (isSafe.Value ? "SAFE" : "UNSAFE") : "UNKNOWN";

        return BuildService(connected, state, connected == true ? null : "SAFETY_MONITOR_DISCONNECTED", new Dictionary<string, object> {
            { "isSafe", isSafe }
        });
    }

    private static Dictionary<string, object> BuildUnavailable(string reason) {
        return BuildService(null, "UNKNOWN", reason, new Dictionary<string, object>());
    }

    private static Dictionary<string, object> BuildService(bool? connected, string state, string reason, Dictionary<string, object> details) {
        return new Dictionary<string, object> {
            { "connected", connected },
            { "state", state },
            { "reason", reason },
            { "details", details }
        };
    }

    private static string MapDomeState(string raw) {
        return raw switch {
            "ShutterOpen" => "OPEN",
            "ShutterClosed" => "CLOSED",
            "ShutterOpening" => "MOVING",
            "ShutterClosing" => "MOVING",
            "ShutterError" => "FAULT",
            _ => "UNKNOWN"
        };
    }

    private static object ReadProperty(object source, params string[] names) {
        if (source == null) {
            return null;
        }

        foreach (var name in names) {
            try {
                var property = source.GetType().GetProperty(name, BindingFlags.Instance | BindingFlags.Public);
                if (property != null) {
                    return property.GetValue(source);
                }
            } catch {
            }
        }

        return null;
    }

    private static bool? ReadBool(object source, params string[] names) {
        var value = ReadProperty(source, names);
        if (value == null) {
            return null;
        }

        try {
            return Convert.ToBoolean(value, CultureInfo.InvariantCulture);
        } catch {
            return null;
        }
    }

    private static double? ReadDouble(object source, params string[] names) {
        var value = ReadProperty(source, names);
        if (value == null) {
            return null;
        }

        try {
            var number = Convert.ToDouble(value, CultureInfo.InvariantCulture);
            return double.IsNaN(number) || double.IsInfinity(number) ? null : number;
        } catch {
            return null;
        }
    }

    private static string ReadString(object source, params string[] names) {
        var value = ReadProperty(source, names);
        return value?.ToString();
    }

    private static void WriteJsonAtomically(string path, string json) {
        var directory = Path.GetDirectoryName(path);
        Directory.CreateDirectory(directory);

        var tempPath = path + ".tmp";
        File.WriteAllText(tempPath, json, new UTF8Encoding(false));

        if (File.Exists(path)) {
            var backupPath = path + ".bak";
            try {
                File.Replace(tempPath, path, backupPath, true);
                TryDelete(backupPath);
                return;
            } catch (PlatformNotSupportedException) {
            }
        }

        TryDelete(path);
        File.Move(tempPath, path);
    }

    private static void TryDelete(string path) {
        try {
            if (File.Exists(path)) {
                File.Delete(path);
            }
        } catch {
        }
    }
}
