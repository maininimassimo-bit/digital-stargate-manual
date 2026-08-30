using System.Globalization;
using System.Text.RegularExpressions;
using DigitalStarGate.Application.Telemetry.Sqm;

namespace DigitalStarGate.Infrastructure.Telemetry.Sqm;

public static partial class UnihedronSqmProtocolParser
{
    private const double SaturatedReading = 0.0;

    public static SqmInstrumentSample ParseReading(
        string rawResponse,
        DateTimeOffset observedAtUtc,
        SqmSourceIdentity source)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(rawResponse);
        ArgumentNullException.ThrowIfNull(source);

        var response = rawResponse.Trim();
        var match = ReadingRegex().Match(response);

        if (!match.Success)
        {
            return Unknown(observedAtUtc, source, rawResponse, "UNRECOGNIZED_RESPONSE");
        }

        if (!double.TryParse(
                match.Groups["magnitude"].Value,
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out var magnitude) ||
            !double.IsFinite(magnitude))
        {
            return Unknown(observedAtUtc, source, rawResponse, "INVALID_MAGNITUDE");
        }

        double? sensorTemperature = null;
        var temperatureText = match.Groups["temperature"].Value;
        if (!string.IsNullOrWhiteSpace(temperatureText) &&
            double.TryParse(
                temperatureText,
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out var parsedTemperature) &&
            double.IsFinite(parsedTemperature))
        {
            sensorTemperature = parsedTemperature;
        }

        var freshness = match.Groups["freshness"].Value.ToUpperInvariant();
        if (freshness == "S")
        {
            return new SqmInstrumentSample(
                null,
                observedAtUtc,
                SqmSampleQuality.Stale,
                source,
                rawResponse,
                sensorTemperature,
                "DEVICE_REPORTED_STALE");
        }

        if (magnitude == SaturatedReading)
        {
            return Unknown(observedAtUtc, source, rawResponse, "SENSOR_SATURATED");
        }

        if (freshness is not ("F" or "P"))
        {
            return Unknown(observedAtUtc, source, rawResponse, "UNKNOWN_FRESHNESS");
        }

        return new SqmInstrumentSample(
            magnitude,
            observedAtUtc,
            SqmSampleQuality.Current,
            source,
            rawResponse,
            sensorTemperature,
            null);
    }

    private static SqmInstrumentSample Unknown(
        DateTimeOffset observedAtUtc,
        SqmSourceIdentity source,
        string rawResponse,
        string diagnostic) =>
        new(
            null,
            observedAtUtc,
            SqmSampleQuality.Unknown,
            source,
            rawResponse,
            null,
            diagnostic);

    [GeneratedRegex(
        @"^r,(?<magnitude>[+-]?(?:\d+(?:\.\d*)?|\.\d+))m,(?<frequency>[+-]?(?:\d+(?:\.\d*)?|\.\d+))Hz,(?<period>\d+)c,(?<ticks>\d+)s,(?<temperature>[+-]?(?:\d+(?:\.\d*)?|\.\d+))C,(?<freshness>[FPS])$",
        RegexOptions.CultureInvariant)]
    private static partial Regex ReadingRegex();
}
