using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Commands;

public interface ICommandContract;

public sealed record CreateObservationSession(TargetId TargetId, ObservatoryId ObservatoryId, CorrelationId CorrelationId) : ICommandContract;
public sealed record StartObservationSession(ObservationSessionId SessionId, CorrelationId CorrelationId) : ICommandContract;
public sealed record AbortObservationSession(ObservationSessionId SessionId, string Reason, CorrelationId CorrelationId) : ICommandContract;
public sealed record ParkMount(EquipmentId MountId, CorrelationId CorrelationId) : ICommandContract;
public sealed record OpenRoof(EquipmentId RoofId, CorrelationId CorrelationId) : ICommandContract;
public sealed record CloseRoof(EquipmentId RoofId, CorrelationId CorrelationId) : ICommandContract;
public sealed record AcquireTarget(ObservationSessionId SessionId, TargetId TargetId, CorrelationId CorrelationId) : ICommandContract;
public sealed record StartExposure(ObservationSessionId SessionId, ExposureTime ExposureTime, Gain Gain, Offset Offset, CorrelationId CorrelationId) : ICommandContract;
public sealed record CalibrateFrames(ObservationSessionId SessionId, IReadOnlyList<ImageId> ImageIds, CorrelationId CorrelationId) : ICommandContract;
public sealed record PublishObservation(ObservationSessionId SessionId, CorrelationId CorrelationId) : ICommandContract;
