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
 * Read-only local telemetry boundary for Observatory Status.
 * N.I.N.A. equipment snapshots and approved passive host adapters are consolidated into one projection.
 * Power is observed read-only through TS Shelter SafetyMonitor/J6 using the commissioned power fault mask 0x01.
 */
[Export(typeof(IPluginManifest))]
public sealed class DomeTelemetryExporterPlugin : PluginBase, IDomeConsumer {
    private const int ProjectionIntervalSeconds = 5;

    private readonly IDomeMediator domeMediator;
    private readonly ITelescopeMediator telescopeMediator;
    private readonly ICameraMediator cameraMediator;
    private readonly IWeatherDataMediator weatherDataMediator;
    private readonly ISafetyMonitorMediator safetyMonitorMediator;
    private readonly NetworkTelemetryAdapter networkTelemetryAdapter = new();
    private readonly PowerTelemetryAdapter powerTelemetryAdapter = new();
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
        if (!disposed) TryWriteProjection();
    }

    public override Task Teardown() {
        Dispose();
        return base.Teardown();
    }

    public void Dispose() {
        if (disposed) return;
        disposed = true;
        projectionTimer.Dispose();
        powerTelemetryAdapter.Dispose();
        try { domeMediator.RemoveConsumer(this); } catch { }
    }

    private void TryWriteProjection() {
        if (disposed) return;
        try { lock (writeLock) { WriteProjection(); } }
        catch { }
    }

    private void WriteProjection() {
        var observedAtUtc = DateTime.UtcNow;
        var domeInfo = SafeGetInfo(domeMediator);
        var telescopeInfo = SafeGetInfo(telescopeMediator);
        var cameraInfo = SafeGetInfo(cameraMediator);
        var weatherInfo = SafeGetInfo(weatherDataMediator);
        var safetyInfo = SafeGetInfo(safetyMonitorMediator);
        var networkInfo = networkTelemetryAdapter.Observe();
        var powerInfo = powerTelemetryAdapter.Observe();

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
                { "power", powerInfo },
                { "network", networkInfo }
            }}
        };
        WriteJsonAtomically(projectionPath, JsonSerializer.Serialize(payload));
    }

    private static object SafeGetInfo(object mediator) {
        try { return mediator.GetType().GetMethod("GetInfo", BindingFlags.Instance | BindingFlags.Public)?.Invoke(mediator, null); }
        catch { return null; }
    }

    private static Dictionary<string, object> BuildDome(object info) {
        var connected = ReadBool(info, "Connected");
        var raw = connected == true ? ReadString(info, "ShutterStatus") : null;
        var state = connected == true ? MapDomeState(raw) : "UNKNOWN";
        return BuildService(connected, state, connected == true ? null : "DOME_DISCONNECTED", new Dictionary<string, object> { { "rawShutterStatus", raw } });
    }

    private static Dictionary<string, object> BuildMount(object info) {
        var connected = ReadBool(info, "Connected");
        var atPark = connected == true ? ReadBool(info, "AtPark") : null;
        var atHome = connected == true ? ReadBool(info, "AtHome") : null;
        var tracking = connected == true ? ReadBool(info, "TrackingEnabled", "Tracking") : null;
        var sideOfPier = connected == true ? ReadString(info, "SideOfPier") : null;
        var state = "UNKNOWN";
        if (connected == true) state = atPark == true ? "PARKED" : atHome == true ? "HOME" : tracking == true ? "TRACKING" : "IDLE";
        return BuildService(connected, state, connected == true ? null : "MOUNT_DISCONNECTED", new Dictionary<string, object> {
            { "atPark", atPark }, { "atHome", atHome }, { "tracking", tracking }, { "sideOfPier", sideOfPier }
        });
    }

    private static Dictionary<string, object> BuildCamera(object info) {
        var connected = ReadBool(info, "Connected");
        var exposing = connected == true ? ReadBool(info, "IsExposing", "Exposing") : null;
        var state = connected == true ? (exposing == true ? "EXPOSING" : "READY") : "UNKNOWN";
        return BuildService(connected, state, connected == true ? null : "CAMERA_DISCONNECTED", new Dictionary<string, object> {
            { "temperatureC", connected == true ? ReadDouble(info, "Temperature", "CCDTemperature", "SensorTemperature") : null },
            { "coolerOn", connected == true ? ReadBool(info, "CoolerOn") : null },
            { "coolerPowerPct", connected == true ? ReadDouble(info, "CoolerPower") : null },
            { "exposing", exposing }
        });
    }

    private static Dictionary<string, object> BuildWeather(object info) {
        var connected = ReadBool(info, "Connected");
        var state = connected == true ? "AVAILABLE" : "UNKNOWN";
        return BuildService(connected, state, connected == true ? null : "WEATHER_DISCONNECTED", new Dictionary<string, object> {
            { "temperatureC", connected == true ? ReadDouble(info, "Temperature") : null },
            { "humidityPct", connected == true ? ReadDouble(info, "Humidity") : null },
            { "dewPointC", connected == true ? ReadDouble(info, "DewPoint") : null },
            { "windSpeed", connected == true ? ReadDouble(info, "WindSpeed") : null },
            { "windGust", connected == true ? ReadDouble(info, "WindGust") : null },
            { "pressure", connected == true ? ReadDouble(info, "Pressure") : null },
            { "cloudCoverPct", connected == true ? ReadDouble(info, "CloudCover") : null },
            { "rainRate", connected == true ? ReadDouble(info, "RainRate") : null },
            { "skyTemperatureC", connected == true ? ReadDouble(info, "SkyTemperature") : null }
        });
    }

    private static Dictionary<string, object> BuildSafety(object info) {
        var connected = ReadBool(info, "Connected");
        var isSafe = connected == true ? ReadBool(info, "IsSafe") : null;
        var state = connected == true && isSafe.HasValue ? (isSafe.Value ? "SAFE" : "UNSAFE") : "UNKNOWN";
        return BuildService(connected, state, connected == true ? null : "SAFETY_MONITOR_DISCONNECTED", new Dictionary<string, object> { { "isSafe", isSafe } });
    }

    private static Dictionary<string, object> BuildService(bool? connected, string state, string reason, Dictionary<string, object> details) => new() {
        { "connected", connected }, { "state", state }, { "reason", reason }, { "details", details }
    };

    private static string MapDomeState(string raw) => raw switch {
        "ShutterOpen" => "OPEN", "ShutterClosed" => "CLOSED", "ShutterOpening" => "MOVING", "ShutterClosing" => "MOVING", "ShutterError" => "FAULT", _ => "UNKNOWN"
    };

    private static object ReadProperty(object source, params string[] names) {
        if (source == null) return null;
        foreach (var name in names) {
            try {
                var property = source.GetType().GetProperty(name, BindingFlags.Instance | BindingFlags.Public);
                if (property != null) return property.GetValue(source);
            } catch { }
        }
        return null;
    }

    private static bool? ReadBool(object source, params string[] names) {
        var value = ReadProperty(source, names);
        if (value == null) return null;
        try { return Convert.ToBoolean(value, CultureInfo.InvariantCulture); } catch { return null; }
    }

    private static double? ReadDouble(object source, params string[] names) {
        var value = ReadProperty(source, names);
        if (value == null) return null;
        try {
            var number = Convert.ToDouble(value, CultureInfo.InvariantCulture);
            return double.IsNaN(number) || double.IsInfinity(number) ? null : number;
        } catch { return null; }
    }

    private static string ReadString(object source, params string[] names) => ReadProperty(source, names)?.ToString();

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
            } catch (PlatformNotSupportedException) { }
        }
        TryDelete(path);
        File.Move(tempPath, path);
    }

    private static void TryDelete(string path) {
        try { if (File.Exists(path)) File.Delete(path); } catch { }
    }
}
