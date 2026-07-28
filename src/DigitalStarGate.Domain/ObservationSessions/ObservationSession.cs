using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Domain.ObservationSessions;

public enum ObservationSessionStatus
{
  Created,
  Running,
  Completed,
  Aborted
}

public sealed class ObservationSession
{
  private ObservationSession(
      ObservationSessionId id,
      TargetId targetId,
      ObservatoryId observatoryId,
      Guid observationPlanId,
      DateTimeOffset createdAt)
  {
    Id = id;
    TargetId = targetId;
    ObservatoryId = observatoryId;
    ObservationPlanId = observationPlanId;
    CreatedAt = createdAt;
    Status = ObservationSessionStatus.Created;
  }

  public ObservationSessionId Id { get; }

  public TargetId TargetId { get; }

  public ObservatoryId ObservatoryId { get; }

  public Guid ObservationPlanId { get; }

  public DateTimeOffset CreatedAt { get; }

  public DateTimeOffset? StartedAt { get; private set; }

  public DateTimeOffset? CompletedAt { get; private set; }

  public ObservationSessionStatus Status { get; private set; }

  public static ObservationSession Create(
      ObservationSessionId id,
      TargetId targetId,
      ObservatoryId observatoryId,
      Guid observationPlanId,
      DateTimeOffset createdAt)
  {
    if (id.Value == Guid.Empty)
    {
      throw new ArgumentException("L'identificativo della sessione è obbligatorio.", nameof(id));
    }

    if (targetId.Value == Guid.Empty)
    {
      throw new ArgumentException("Il Target è obbligatorio.", nameof(targetId));
    }

    if (observatoryId.Value == Guid.Empty)
    {
      throw new ArgumentException("L'osservatorio è obbligatorio.", nameof(observatoryId));
    }

    if (observationPlanId == Guid.Empty)
    {
      throw new ArgumentException("L'Observation Plan è obbligatorio.", nameof(observationPlanId));
    }

    if (createdAt == default)
    {
      throw new ArgumentException("La data di creazione è obbligatoria.", nameof(createdAt));
    }

    return new ObservationSession(id, targetId, observatoryId, observationPlanId, createdAt);
  }
}
