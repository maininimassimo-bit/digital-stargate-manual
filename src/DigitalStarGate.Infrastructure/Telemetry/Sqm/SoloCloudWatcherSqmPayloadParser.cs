using System.Globalization;
using System.Text.RegularExpressions;
using DigitalStarGate.Application.Telemetry.Sqm;

namespace DigitalStarGate.Infrastructure.Telemetry.Sqm;

public static partial class SoloCloudWatcherSqmPayloadParser
{
    public static SqmInstrumentSample Parse(
        string payload,
        DateTimeOffset receivedAtUtc,
        TimeSpan freshnessWindow)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(payload);
        if (freshnessWindow <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(freshnessWindow));
        }

        var fields = ParseFields(payload);
        var identity = ParseIdentity(fields);

        if (!fields.TryGetValue("dataGMTTime", out var timestampText) ||
            !DateTimeOffset.TryParseExact(
                timestampText,
                "yyyy/MM/dd HH:mm:ss",
                CultureInfo.InvariantCulture,
                DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal,
                out var observedAtUtc))
        {
            return Unknown(receivedAtUtc, identity, payload, "INVALID_OR_MISSING_GMT_TIMESTAMP");
        }

        if (!fields.TryGetValue("lightmpsas", out var mpsasText) ||
            !double.TryParse(mpsasText, NumberStyles.Float, CultureInfo.InvariantCulture, out var mpsas) ||
            !double.IsFinite(mpsas) ||
            mpsas <= 0)
        {
            return Unknown(observedAtUtc, identity, payload, "INVALID_OR_MISSING_LIGHTMPSAS");
        }

        var age = receivedAtUtc - observedAtUtc;
        if (age < TimeSpan.FromSeconds(-5))
        {
            return Unknown(observedAtUtc, identity, payload, "SOURCE_TIMESTAMP_IN_FUTURE");
        }

        if (age > freshnessWindow)
        {
            return new SqmInstrumentSample(
                null,
                observedAtUtc,
                SqmSampleQuality.Stale,
                identity,
                payload,
                null,
                "SOURCE_SAMPLE_STALE");
        }

        return new SqmInstrumentSample(
            mpsas,
            observedAtUtc,
            SqmSampleQuality.Current,
            identity,
            payload,
            null,
            null);
    }

    private static Dictionary<string, string> ParseFields(string payload)
    {
        var result = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        using var reader = new StringReader(payload);

        while (reader.ReadLine() is { } line)
        {
            var separator = line.IndexOf('=');
            if (separator <= 0)
            {
                continue;
            }

            var key = line[..separator].Trim();
            var value = line[(separator + 1)..].Trim();
            if (key.Length > 0)
            {
                result[key] = value;
            }
        }

        return result;
    }

    private static SqmSourceIdentity ParseIdentity(IReadOnlyDictionary<string, string> fields)
    {
        string? serial = null;
        string model = "CloudWatcher SOLO HTTP feed";

        if (fields.TryGetValue("cwinfo", out var cwinfo))
        {
            var match = CwInfoRegex().Match(cwinfo);
            if (match.Success)
            {
                serial = match.Groups["serial"].Value;
                var firmware = match.Groups["firmware"].Value;
                model = $"CloudWatcher via SOLO (FW {firmware})";
            }
        }

        return new SqmSourceIdentity(
            "DSG.SoloCloudWatcherSqmAdapter",
            "Lunatico",
            model,
            serial,
            "http");
    }

    private static SqmInstrumentSample Unknown(
        DateTimeOffset observedAtUtc,
        SqmSourceIdentity source,
        string payload,
        string diagnostic) =>
        new(
            null,
            observedAtUtc,
            SqmSampleQuality.Unknown,
            source,
            payload,
            null,
            diagnostic);

    [GeneratedRegex(@"Serial:\s*(?<serial>[^,]+),\s*FW:\s*(?<firmware>\S+)", RegexOptions.CultureInvariant | RegexOptions.IgnoreCase)]
    private static partial Regex CwInfoRegex();
}
