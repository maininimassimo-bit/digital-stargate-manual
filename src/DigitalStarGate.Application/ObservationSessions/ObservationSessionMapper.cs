using DigitalStarGate.Contracts.Dto;
using DigitalStarGate.Domain.ObservationSessions;

namespace DigitalStarGate.Application.ObservationSessions;

internal static class ObservationSessionMapper
{
  public static ObservationSessionDto ToDto(ObservationSession session) =>
      new(session.Id, session.TargetId, session.ObservatoryId, session.StartedAt, session.CompletedAt, session.Status.ToString());
}
