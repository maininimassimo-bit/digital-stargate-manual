namespace DigitalStarGate.Contracts.Common;

public readonly record struct ObservationSessionId(Guid Value);

public readonly record struct EquipmentId(Guid Value);

public readonly record struct TargetId(Guid Value);

public readonly record struct ImageId(Guid Value);

public readonly record struct ObservatoryId(Guid Value);

public readonly record struct UserId(Guid Value);

public readonly record struct AlertId(Guid Value);

public readonly record struct NotificationId(Guid Value);

public readonly record struct CorrelationId(Guid Value);

public readonly record struct CausationId(Guid Value);
