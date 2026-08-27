using System;
using System.Collections.Generic;
using System.Globalization;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Runtime.Versioning;
using System.Threading;

namespace DigitalStarGate.Nina.DomeTelemetryExporter;

[SupportedOSPlatform("windows")]
internal sealed class PowerTelemetryAdapter : IDisposable {
    private const string ProgId = "ASCOM.TS_Shelter.SafetyMonitor";
    private const string SafetiesCommand = "safeties";
    private const int PowerFaultMask = 0x00000001;
    private const int PollMilliseconds = 5000;

    private readonly object stateLock = new();
    private readonly ManualResetEvent stopEvent = new(false);
    private readonly Thread worker;
    private Dictionary<string, object> latest;
    private bool disposed;

    public PowerTelemetryAdapter() {
        latest = BuildUnknown("POWER_SOURCE_INITIALIZING", null, null, null);
        worker = new Thread(PollLoop) {
            IsBackground = true,
            Name = "DSG-TS-Shelter-Power-Telemetry"
        };
        worker.SetApartmentState(ApartmentState.STA);
        worker.Start();
    }

    public Dictionary<string, object> Observe() {
        lock (stateLock) {
            return Clone(latest);
        }
    }

    public void Dispose() {
        if (disposed) return;
        disposed = true;
        stopEvent.Set();
        try { worker.Join(TimeSpan.FromSeconds(3)); } catch { }
        stopEvent.Dispose();
    }

    private void PollLoop() {
        object comObject = null;
        Type comType = null;

        try {
            while (!stopEvent.WaitOne(0)) {
                try {
                    if (comObject == null) {
                        comType = Type.GetTypeFromProgID(ProgId, throwOnError: false);
                        if (comType == null) {
                            SetLatest(BuildUnknown("TS_SHELTER_COM_NOT_REGISTERED", null, null, null));
                            stopEvent.WaitOne(PollMilliseconds);
                            continue;
                        }

                        comObject = Activator.CreateInstance(comType);
                        SetConnected(comType, comObject, true);
                    }

                    var connected = ReadConnected(comType, comObject);
                    var isSafe = ReadIsSafe(comType, comObject);
                    var rawText = Convert.ToString(
                        comType.InvokeMember(
                            "CommandString",
                            BindingFlags.InvokeMethod,
                            null,
                            comObject,
                            new object[] { SafetiesCommand, false },
                            CultureInfo.InvariantCulture),
                        CultureInfo.InvariantCulture);

                    if (!int.TryParse(rawText, NumberStyles.Integer, CultureInfo.InvariantCulture, out var safetiesRaw)) {
                        SetLatest(BuildUnknown("TS_SHELTER_SAFETIES_PARSE_FAILED", connected, rawText, isSafe));
                    } else {
                        var powerFault = (safetiesRaw & PowerFaultMask) != 0;
                        var state = powerFault ? "MAINS_LOST" : "MAINS_PRESENT";
                        SetLatest(BuildService(connected, state, null, new Dictionary<string, object> {
                            { "source", "TS Shelter SafetyMonitor / J6 voltage supervision" },
                            { "progId", ProgId },
                            { "command", SafetiesCommand },
                            { "safetiesRaw", safetiesRaw },
                            { "powerFaultMask", PowerFaultMask },
                            { "powerFault", powerFault },
                            { "mainsPresent", !powerFault },
                            { "safetyIsSafe", isSafe }
                        }));
                    }
                } catch {
                    ReleaseCom(ref comObject, comType);
                    comType = null;
                    SetLatest(BuildUnknown("TS_SHELTER_POWER_READ_FAILED", null, null, null));
                }

                stopEvent.WaitOne(PollMilliseconds);
            }
        } finally {
            ReleaseCom(ref comObject, comType);
        }
    }

    private static void SetConnected(Type comType, object comObject, bool value) {
        comType.InvokeMember(
            "Connected",
            BindingFlags.SetProperty,
            null,
            comObject,
            new object[] { value },
            CultureInfo.InvariantCulture);
    }

    private static bool? ReadConnected(Type comType, object comObject) {
        try {
            var value = comType.InvokeMember("Connected", BindingFlags.GetProperty, null, comObject, null, CultureInfo.InvariantCulture);
            return Convert.ToBoolean(value, CultureInfo.InvariantCulture);
        } catch {
            return null;
        }
    }

    private static bool? ReadIsSafe(Type comType, object comObject) {
        try {
            var value = comType.InvokeMember("IsSafe", BindingFlags.GetProperty, null, comObject, null, CultureInfo.InvariantCulture);
            return Convert.ToBoolean(value, CultureInfo.InvariantCulture);
        } catch {
            return null;
        }
    }

    private static Dictionary<string, object> BuildUnknown(string reason, bool? connected, string raw, bool? isSafe) {
        return BuildService(connected, "UNKNOWN", reason, new Dictionary<string, object> {
            { "source", "TS Shelter SafetyMonitor / J6 voltage supervision" },
            { "progId", ProgId },
            { "command", SafetiesCommand },
            { "safetiesRaw", raw },
            { "powerFaultMask", PowerFaultMask },
            { "powerFault", null },
            { "mainsPresent", null },
            { "safetyIsSafe", isSafe }
        });
    }

    private static Dictionary<string, object> BuildService(bool? connected, string state, string reason, Dictionary<string, object> details) => new() {
        { "connected", connected },
        { "state", state },
        { "reason", reason },
        { "details", details }
    };

    private void SetLatest(Dictionary<string, object> value) {
        lock (stateLock) {
            latest = value;
        }
    }

    private static Dictionary<string, object> Clone(Dictionary<string, object> source) {
        var clone = new Dictionary<string, object>();
        foreach (var pair in source) {
            if (pair.Value is Dictionary<string, object> nested) {
                clone[pair.Key] = new Dictionary<string, object>(nested);
            } else {
                clone[pair.Key] = pair.Value;
            }
        }
        return clone;
    }

    private static void ReleaseCom(ref object comObject, Type comType) {
        if (comObject == null) return;
        try {
            if (comType != null) {
                try { SetConnected(comType, comObject, false); } catch { }
            }
            if (Marshal.IsComObject(comObject)) {
                Marshal.FinalReleaseComObject(comObject);
            }
        } catch { }
        comObject = null;
    }
}
