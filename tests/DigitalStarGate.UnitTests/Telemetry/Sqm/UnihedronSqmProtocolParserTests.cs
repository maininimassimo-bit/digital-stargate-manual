using DigitalStarGate.Application.Telemetry.Sqm;
using DigitalStarGate.Infrastructure.Telemetry.Sqm;

namespace DigitalStarGate.UnitTests.Telemetry.Sqm;

public sealed class UnihedronSqmProtocolParserTests
{
    private static readonly SqmSourceIdentity Source = new(
        "DSG.SqmInstrumentAdapter",
        "Unihedron",
        "SQM-LU-DL",
        null,
        "serial");

    private static readonly DateTimeOffset ObservedAt =
        new(2026, 8, 30, 20, 0, 0, TimeSpan.Zero);

    [Fact]
    public void ParseReading_FreshInstrumentReading_ReturnsCurrentSample()
    {
        var sample = UnihedronSqmProtocolParser.ParseReading(
            "r, 20.01m,000000591Hz,0000049234c,0000000.081s, 039.4C,F",
            ObservedAt,
            Source);

        Assert.Equal(SqmSampleQuality.Current, sample.Quality);
        Assert.Equal(20.01, sample.MagArcsec2);
        Assert.Equal(39.4, sample.SensorTemperatureC);
        Assert.Null(sample.Diagnostic);
    }

    [Fact]
    public void ParseReading_StaleInstrumentReading_DoesNotPromoteMagnitude()
    {
        var sample = UnihedronSqmProtocolParser.ParseReading(
            "r, 20.01m,000000591Hz,0000049234c,0000000.081s, 039.4C,S",
            ObservedAt,
            Source);

        Assert.Equal(SqmSampleQuality.Stale, sample.Quality);
        Assert.Null(sample.MagArcsec2);
        Assert.Equal("DEVICE_REPORTED_STALE", sample.Diagnostic);
    }

    [Fact]
    public void ParseReading_SaturatedReading_ReturnsUnknown()
    {
        var sample = UnihedronSqmProtocolParser.ParseReading(
            "r, 00.00m,000000000Hz,0000000000c,0000000.000s, 039.4C,F",
            ObservedAt,
            Source);

        Assert.Equal(SqmSampleQuality.Unknown, sample.Quality);
        Assert.Null(sample.MagArcsec2);
        Assert.Equal("SENSOR_SATURATED", sample.Diagnostic);
    }

    [Fact]
    public void ParseReading_MalformedResponse_ReturnsUnknown()
    {
        var sample = UnihedronSqmProtocolParser.ParseReading(
            "not-an-sqm-response",
            ObservedAt,
            Source);

        Assert.Equal(SqmSampleQuality.Unknown, sample.Quality);
        Assert.Null(sample.MagArcsec2);
        Assert.Equal("UNRECOGNIZED_RESPONSE", sample.Diagnostic);
    }
}
