using System;
using System.IO;
using System.Text.Json;

namespace DigitalStarGate.Nina.DomeTelemetryExporter;

internal sealed class SqmTelemetryOptions {
    private static readonly JsonSerializerOptions SerializerOptions = new() {
        PropertyNameCaseInsensitive = true
    };

    public const string DefaultEndpoint = "http://meteo.deeplab.space:8080/cgi-bin/cgiLastData";
    public const int DefaultPollSeconds = 30;
    public const int DefaultFreshnessSeconds = 120;
    public const int DefaultHttpTimeoutSeconds = 5;

    public string Endpoint { get; init; } = DefaultEndpoint;
    public int PollSeconds { get; init; } = DefaultPollSeconds;
    public int FreshnessSeconds { get; init; } = DefaultFreshnessSeconds;
    public int HttpTimeoutSeconds { get; init; } = DefaultHttpTimeoutSeconds;
    public string ConfigurationSource { get; init; } = "built-in-defaults";

    public static SqmTelemetryOptions Load() {
        var path = GetConfigurationPath();
        if (!File.Exists(path)) return new SqmTelemetryOptions();

        try {
            var json = File.ReadAllText(path);
            var configured = JsonSerializer.Deserialize<SqmTelemetryOptions>(json, SerializerOptions);
            if (configured == null) return InvalidConfiguration("CONFIG_EMPTY");
            if (!Uri.TryCreate(configured.Endpoint, UriKind.Absolute, out var endpoint) ||
                (endpoint.Scheme != Uri.UriSchemeHttp && endpoint.Scheme != Uri.UriSchemeHttps)) {
                return InvalidConfiguration("CONFIG_ENDPOINT_INVALID");
            }
            if (configured.PollSeconds < 5 || configured.PollSeconds > 3600) return InvalidConfiguration("CONFIG_POLL_INVALID");
            if (configured.FreshnessSeconds < configured.PollSeconds || configured.FreshnessSeconds > 7200) return InvalidConfiguration("CONFIG_FRESHNESS_INVALID");
            if (configured.HttpTimeoutSeconds < 1 || configured.HttpTimeoutSeconds > 30) return InvalidConfiguration("CONFIG_TIMEOUT_INVALID");

            return new SqmTelemetryOptions {
                Endpoint = endpoint.ToString(),
                PollSeconds = configured.PollSeconds,
                FreshnessSeconds = configured.FreshnessSeconds,
                HttpTimeoutSeconds = configured.HttpTimeoutSeconds,
                ConfigurationSource = path
            };
        } catch {
            return InvalidConfiguration("CONFIG_READ_FAILED");
        }
    }

    public static string GetConfigurationPath() {
        var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        return Path.Combine(localAppData, "DigitalStarGate", "telemetry", "sqm-source.json");
    }

    private static SqmTelemetryOptions InvalidConfiguration(string reason) => new() {
        Endpoint = DefaultEndpoint,
        PollSeconds = DefaultPollSeconds,
        FreshnessSeconds = DefaultFreshnessSeconds,
        HttpTimeoutSeconds = DefaultHttpTimeoutSeconds,
        ConfigurationSource = "invalid-config-fallback:" + reason
    };
}
