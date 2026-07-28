using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Queries;

public sealed record GetObservationSession(ObservationSessionId SessionId);
public sealed record SearchObservationSessions(DateTimeOffset? From, DateTimeOffset? To, TargetId? TargetId, string? Status, int Page, int PageSize);
public sealed record GetEquipmentStatus(EquipmentId EquipmentId);
public sealed record GetWeather(ObservatoryId ObservatoryId, DateTimeOffset? At);
public sealed record GetTelemetry(string Source, string? Metric, DateTimeOffset From, DateTimeOffset To);
