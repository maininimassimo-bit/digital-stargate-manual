using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Events;

public interface IPlatformEvent
{
  Guid EventId { get; }
  DateTimeOffset OccurredAt { get; }
  CorrelationId CorrelationId { get; }
  CausationId? CausationId { get; }
  string Version { get; }
}

public abstract record PlatformEvent(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version) : IPlatformEvent;
public sealed record SessionCreated(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId, TargetId TargetId, ObservatoryId ObservatoryId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record SessionStarted(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record SessionCompleted(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record SessionAborted(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId, string Reason) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record TargetAcquired(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId, TargetId TargetId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record ExposureStarted(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId, decimal ExposureTimeSeconds) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record ExposureCompleted(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId, ImageId ImageId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record CalibrationCompleted(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservationSessionId SessionId, IReadOnlyList<ImageId> ImageIds) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record WeatherUnsafeDetected(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, ObservatoryId ObservatoryId, string Reason) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record RoofOpened(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, EquipmentId RoofId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record RoofClosed(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, EquipmentId RoofId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record MountParked(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, EquipmentId MountId) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record TelemetryCollected(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, string Source, string Metric, decimal Value, string Unit) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record AlertRaised(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, AlertId AlertId, string Severity, string Code, string Message) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
public sealed record ConfigurationChanged(Guid EventId, DateTimeOffset OccurredAt, CorrelationId CorrelationId, CausationId? CausationId, string Version, string Section, string Key, string Source) : PlatformEvent(EventId, OccurredAt, CorrelationId, CausationId, Version);
