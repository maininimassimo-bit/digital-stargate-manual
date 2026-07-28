using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Dto;

public sealed record ObservationSessionDto(ObservationSessionId Id, TargetId TargetId, ObservatoryId ObservatoryId, DateTimeOffset? StartedAt, DateTimeOffset? CompletedAt, string Status);
public sealed record TargetDto(TargetId Id, string Name, Coordinates Coordinates);
public sealed record EquipmentDto(EquipmentId Id, string Name, string Type, string Status);
public sealed record ObservatoryDto(ObservatoryId Id, string Name, string TimeZone, Coordinates Location);
public sealed record CameraDto(EquipmentId Id, string Name, string Sensor, bool IsCooled);
public sealed record MountDto(EquipmentId Id, string Name, string Status, bool IsParked);
public sealed record FilterWheelDto(EquipmentId Id, string Name, IReadOnlyList<string> Filters);
public sealed record ImageFrameDto(ImageId Id, ObservationSessionId SessionId, TargetId TargetId, ExposureTime ExposureTime, Gain Gain, Offset Offset, string FrameType, DateTimeOffset CapturedAt);
public sealed record CalibrationFrameDto(ImageId Id, string CalibrationType, ExposureTime ExposureTime, Temperature? Temperature, DateTimeOffset CapturedAt);
public sealed record WeatherSnapshotDto(DateTimeOffset CapturedAt, Temperature Temperature, Humidity Humidity, WindSpeed WindSpeed, SkyQuality? SkyQuality, bool IsSafe);
public sealed record TelemetrySampleDto(DateTimeOffset CapturedAt, string Source, string Metric, decimal Value, string Unit);
public sealed record ObservationPlanDto(Guid Id, string Name, IReadOnlyList<TargetId> Targets, string Status);
public sealed record SafetyStatusDto(bool IsSafe, string Reason, DateTimeOffset EvaluatedAt);
public sealed record UserDto(UserId Id, string DisplayName, string Email, IReadOnlyList<string> Roles);
public sealed record RoleDto(string Name, IReadOnlyList<string> Permissions);
public sealed record PermissionDto(string Name, string Description);
public sealed record NotificationDto(NotificationId Id, string Type, string Message, DateTimeOffset CreatedAt, bool IsRead);
public sealed record AlertDto(AlertId Id, string Severity, string Code, string Message, DateTimeOffset RaisedAt, bool IsResolved);
public sealed record SystemConfigurationDto(string Section, string Key, string Value, string Source, bool IsSecretReference);
