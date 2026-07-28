using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Notifications;

public sealed record NotificationRecipient(UserId UserId, string Channel);

public sealed record NotificationMessage(NotificationId NotificationId, string Type, string Subject, string Body, IReadOnlyList<NotificationRecipient> Recipients, CorrelationId CorrelationId);

public sealed record AlertNotification(AlertId AlertId, string Severity, string Code, string Message, IReadOnlyList<NotificationRecipient> Recipients, CorrelationId CorrelationId);
