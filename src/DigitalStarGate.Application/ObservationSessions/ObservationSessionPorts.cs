using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Contracts.Events;
using DigitalStarGate.Domain.ObservationSessions;

namespace DigitalStarGate.Application.ObservationSessions;

public interface IObservationSessionRepository
{
  Task AddAsync(ObservationSession session, CancellationToken cancellationToken);

  Task<ObservationSession?> GetAsync(ObservationSessionId id, CancellationToken cancellationToken);
}

public interface IPlatformEventPublisher
{
  Task PublishAsync(IPlatformEvent platformEvent, CancellationToken cancellationToken);
}
