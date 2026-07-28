using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Telemetry;

public sealed record TelemetryContext(CorrelationId CorrelationId, CausationId? CausationId, TraceId? TraceId, SpanId? SpanId);

public sealed record StructuredLogEntry(DateTimeOffset TimestampUtc, string Service, string Environment, string Severity, string EventName, string Message, TelemetryContext Context, string SchemaVersion, IReadOnlyDictionary<string, object?> Properties);

public sealed record OpenTelemetryConvention(string ServiceNamespace, string ServiceName, string ActivitySourceName, string MeterName, string SchemaVersion);
