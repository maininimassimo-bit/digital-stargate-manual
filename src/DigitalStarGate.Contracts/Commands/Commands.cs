using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Commands;

public sealed record CreateObservationSession(TargetId TargetId, ObservatoryId ObservatoryId, CorrelationId CorrelationId);
public sealed record StartObservationSession(ObservationSessionId SessionId, CorrelationId CorrelationId);
public sealed record AbortObservationSession(ObservationSessionId SessionId, string Reason, CorrelationId CorrelationId);
public sealed record ParkMount(EquipmentId MountId, CorrelationId CorrelationId);
public sealed record OpenRoof(EquipmentId RoofId, CorrelationId CorrelationId);
public sealed record CloseRoof(EquipmentId RoofId, CorrelationId CorrelationId);
public sealed record AcquireTarget(ObservationSessionId SessionId, TargetId TargetId, CorrelationId CorrelationId);
public sealed record StartExposure(ObservationSessionId SessionId, ExposureTime ExposureTime, Gain Gain, Offset Offset, CorrelationId CorrelationId);
public sealed record CalibrateFrames(ObservationSessionId SessionId, IReadOnlyList<ImageId> ImageIds, CorrelationId CorrelationId);
public sealed record PublishObservation(ObservationSessionId SessionId, CorrelationId CorrelationId);
