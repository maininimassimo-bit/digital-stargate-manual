using DigitalStarGate.Application.Telemetry.Sqm;
using DigitalStarGate.Infrastructure.Telemetry.Sqm;

namespace DigitalStarGate.UnitTests.Telemetry.Sqm;

public sealed class SoloCloudWatcherSqmPayloadParserTests
{
    private const string ObservedPayload = """
        dataGMTTime=2026/08/30 20:31:42
        cwinfo=Serial: 2382, FW: 5.88
        clouds=-1.520000
        cloudsSafe=1
        temp=24.500000
        wind=6
        windSafe=1
        gust=7
        rain=3200
        rainSafe=1
        lightmpsas=18.74
        lightSafe=1
        switch=1
        safe=1
        hum=62
        humSafe=1
        dewp=16.750000
        rawir=9.880000
        abspress=993.175000
        relpress=1010.426464
        pressureSafe=1
        """;

    [Fact]
    public void Parse_ObservedSoloPayload_ReturnsCurrentInstrumentalSqm()
    {
        var receivedAt = new DateTimeOffset(2026, 8, 30, 20, 32, 0, TimeSpan.Zero);

        var sample = SoloCloudWatcherSqmPayloadParser.Parse(
            ObservedPayload,
            receivedAt,
            TimeSpan.FromMinutes(2));

        Assert.Equal(SqmSampleQuality.Current, sample.Quality);
        Assert.Equal(18.74, sample.MagArcsec2);
        Assert.Equal(new DateTimeOffset(2026, 8, 30, 20, 31, 42, TimeSpan.Zero), sample.ObservedAtUtc);
        Assert.Equal("2382", sample.Source.Serial);
        Assert.Equal("http", sample.Source.Transport);
        Assert.Null(sample.Diagnostic);
    }

    [Fact]
    public void Parse_OldSoloPayload_DoesNotPromoteStaleValue()
    {
        var receivedAt = new DateTimeOffset(2026, 8, 30, 20, 40, 0, TimeSpan.Zero);

        var sample = SoloCloudWatcherSqmPayloadParser.Parse(
            ObservedPayload,
            receivedAt,
            TimeSpan.FromMinutes(2));

        Assert.Equal(SqmSampleQuality.Stale, sample.Quality);
        Assert.Null(sample.MagArcsec2);
        Assert.Equal("SOURCE_SAMPLE_STALE", sample.Diagnostic);
    }

    [Fact]
    public void Parse_MissingLightMpsas_ReturnsUnknown()
    {
        var payload = ObservedPayload.Replace("lightmpsas=18.74", "brightness=18.74", StringComparison.Ordinal);
        var receivedAt = new DateTimeOffset(2026, 8, 30, 20, 32, 0, TimeSpan.Zero);

        var sample = SoloCloudWatcherSqmPayloadParser.Parse(
            payload,
            receivedAt,
            TimeSpan.FromMinutes(2));

        Assert.Equal(SqmSampleQuality.Unknown, sample.Quality);
        Assert.Null(sample.MagArcsec2);
        Assert.Equal("INVALID_OR_MISSING_LIGHTMPSAS", sample.Diagnostic);
    }
}
