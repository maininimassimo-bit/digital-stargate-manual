namespace DigitalStarGate.Application.Telemetry.Sqm;

public enum SqmSampleQuality
{
    Current,
    Stale,
    Unknown
}

public sealed record SqmSourceIdentity(
    string Component,
    string Vendor,
    string Model,
    string? Serial,
    string Transport);

public sealed record SqmInstrumentSample(
    double? MagArcsec2,
    DateTimeOffset ObservedAtUtc,
    SqmSampleQuality Quality,
    SqmSourceIdentity Source,
    string RawResponse,
    double? SensorTemperatureC,
    string? Diagnostic);

public interface ISqmInstrumentReader
{
    ValueTask<SqmInstrumentSample> ReadAsync(CancellationToken cancellationToken = default);
}
