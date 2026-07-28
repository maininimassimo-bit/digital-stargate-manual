namespace DigitalStarGate.Contracts.Common;

public readonly record struct Coordinates(RightAscension RightAscension, Declination Declination);

public readonly record struct ExposureTime(TimeSpan Value);

public readonly record struct Gain(decimal Value);

public readonly record struct Offset(decimal Value);

public readonly record struct Temperature(decimal Celsius);

public readonly record struct Humidity(decimal Percentage);

public readonly record struct WindSpeed(decimal MetersPerSecond);

public readonly record struct SkyQuality(decimal MagnitudesPerSquareArcsecond);

public readonly record struct RightAscension(decimal Hours);

public readonly record struct Declination(decimal Degrees);

public readonly record struct TraceId(string Value);

public readonly record struct SpanId(string Value);
