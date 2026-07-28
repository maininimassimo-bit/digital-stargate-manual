using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Queries;

public interface IQueryContract;

public sealed record GetObservationSession(ObservationSessionId SessionId) : IQueryContract;
public sealed record SearchObservationSessions(DateTimeOffset? From, DateTimeOffset? To, TargetId? TargetId, string? Status, int Page, int PageSize) : IQueryContract;
public sealed record GetEquipmentStatus(EquipmentId EquipmentId) : IQueryContract;
public sealed record GetWeather(ObservatoryId ObservatoryId, DateTimeOffset? At) : IQueryContract;
public sealed record GetTelemetry(string Source, string? Metric, DateTimeOffset From, DateTimeOffset To) : IQueryContract;
