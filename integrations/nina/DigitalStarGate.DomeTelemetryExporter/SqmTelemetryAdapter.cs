using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Threading;

namespace DigitalStarGate.Nina.DomeTelemetryExporter;

internal sealed class SqmTelemetryAdapter : IDisposable {
    private const string DefaultEndpoint = "http://meteo.deeplab.space:8080/cgi-bin/cgiLastData";
    private const int PollMilliseconds = 30000;
    private const int FreshnessSeconds = 120;
    private const int HttpTimeoutSeconds = 5;

    private readonly object stateLock = new();
    private readonly ManualResetEvent stopEvent = new(false);
    private readonly Thread worker;
    private readonly HttpClient httpClient;
    private readonly Uri endpoint;
    private Dictionary<string, object> latest;
    private bool disposed;

    public SqmTelemetryAdapter(string endpointUrl = DefaultEndpoint) {
        endpoint = new Uri(endpointUrl, UriKind.Absolute);
        httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(HttpTimeoutSeconds) };
        latest = BuildUnknown("SQM_SOURCE_INITIALIZING", null, null, null, null);
        worker = new Thread(PollLoop) {
            IsBackground = true,
            Name = "DSG-CloudWatcher-SOLO-SQM-Telemetry"
        };
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
        try { worker.Join(TimeSpan.FromSeconds(HttpTimeoutSeconds + 1)); } catch { }
        httpClient.Dispose();
        stopEvent.Dispose();
    }

    private void PollLoop() {
        while (!stopEvent.WaitOne(0)) {
            try {
                var payload = httpClient.GetStringAsync(endpoint).GetAwaiter().GetResult();
                SetLatest(Parse(payload, DateTime.UtcNow));
            } catch {
                SetLatest(BuildUnknown("SQM_HTTP_READ_FAILED", null, null, null, null));
            }
            stopEvent.WaitOne(PollMilliseconds);
        }
    }

    private Dictionary<string, object> Parse(string payload, DateTime receivedAtUtc) {
        var fields = ParseFields(payload);
        fields.TryGetValue("cwinfo", out var cwinfo);
        fields.TryGetValue("lightmpsas", out var mpsasText);
        fields.TryGetValue("dataGMTTime", out var timestampText);

        if (!DateTime.TryParseExact(
                timestampText,
                "yyyy/MM/dd HH:mm:ss",
                CultureInfo.InvariantCulture,
                DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal,
                out var observedAtUtc)) {
            return BuildUnknown("SQM_SOURCE_TIMESTAMP_INVALID", cwinfo, null, null, null);
        }

        if (!double.TryParse(mpsasText, NumberStyles.Float, CultureInfo.InvariantCulture, out var mpsas) ||
            double.IsNaN(mpsas) || double.IsInfinity(mpsas) || mpsas <= 0) {
            return BuildUnknown("SQM_LIGHTMPSAS_INVALID", cwinfo, observedAtUtc, null, null);
        }

        var age = receivedAtUtc - observedAtUtc;
        if (age < TimeSpan.FromSeconds(-5)) {
            return BuildUnknown("SQM_SOURCE_TIMESTAMP_IN_FUTURE", cwinfo, observedAtUtc, null, null);
        }

        var serial = ParseCwInfoPart(cwinfo, "Serial:");
        var firmware = ParseCwInfoPart(cwinfo, "FW:");
        var freshUntilUtc = observedAtUtc.AddSeconds(FreshnessSeconds);
        if (receivedAtUtc > freshUntilUtc) {
            return BuildService(true, "STALE", "SQM_SOURCE_STALE", new Dictionary<string, object> {
                { "source", "AAG CloudWatcher SOLO HTTP / lightmpsas" },
                { "endpoint", endpoint.ToString() },
                { "sqmMagArcsec2", null },
                { "observedAtUtc", observedAtUtc.ToString("o") },
                { "freshUntilUtc", freshUntilUtc.ToString("o") },
                { "quality", "STALE" },
                { "serial", serial },
                { "firmware", firmware }
            });
        }

        return BuildService(true, "AVAILABLE", null, new Dictionary<string, object> {
            { "source", "AAG CloudWatcher SOLO HTTP / lightmpsas" },
            { "endpoint", endpoint.ToString() },
            { "sqmMagArcsec2", mpsas },
            { "observedAtUtc", observedAtUtc.ToString("o") },
            { "freshUntilUtc", freshUntilUtc.ToString("o") },
            { "quality", "CURRENT" },
            { "serial", serial },
            { "firmware", firmware }
        });
    }

    private Dictionary<string, object> BuildUnknown(string reason, string cwinfo, DateTime? observedAtUtc, string serial, string firmware) {
        if (serial == null) serial = ParseCwInfoPart(cwinfo, "Serial:");
        if (firmware == null) firmware = ParseCwInfoPart(cwinfo, "FW:");
        return BuildService(null, "UNKNOWN", reason, new Dictionary<string, object> {
            { "source", "AAG CloudWatcher SOLO HTTP / lightmpsas" },
            { "endpoint", endpoint.ToString() },
            { "sqmMagArcsec2", null },
            { "observedAtUtc", observedAtUtc?.ToString("o") },
            { "freshUntilUtc", null },
            { "quality", "UNKNOWN" },
            { "serial", serial },
            { "firmware", firmware }
        });
    }

    private static Dictionary<string, string> ParseFields(string payload) {
        var result = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        using var reader = new StringReader(payload ?? string.Empty);
        string line;
        while ((line = reader.ReadLine()) != null) {
            var separator = line.IndexOf('=');
            if (separator <= 0) continue;
            result[line.Substring(0, separator).Trim()] = line.Substring(separator + 1).Trim();
        }
        return result;
    }

    private static string ParseCwInfoPart(string cwinfo, string prefix) {
        if (string.IsNullOrWhiteSpace(cwinfo)) return null;
        foreach (var part in cwinfo.Split(',')) {
            var trimmed = part.Trim();
            if (trimmed.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)) {
                return trimmed.Substring(prefix.Length).Trim();
            }
        }
        return null;
    }

    private static Dictionary<string, object> BuildService(bool? connected, string state, string reason, Dictionary<string, object> details) => new() {
        { "connected", connected }, { "state", state }, { "reason", reason }, { "details", details }
    };

    private void SetLatest(Dictionary<string, object> value) {
        lock (stateLock) { latest = value; }
    }

    private static Dictionary<string, object> Clone(Dictionary<string, object> source) {
        var clone = new Dictionary<string, object>();
        foreach (var pair in source) {
            clone[pair.Key] = pair.Value is Dictionary<string, object> nested
                ? new Dictionary<string, object>(nested)
                : pair.Value;
        }
        return clone;
    }
}
