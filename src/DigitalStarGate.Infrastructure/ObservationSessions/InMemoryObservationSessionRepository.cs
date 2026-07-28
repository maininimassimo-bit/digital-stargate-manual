using System.Collections.Concurrent;
using DigitalStarGate.Application.ObservationSessions;
using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Domain.ObservationSessions;

namespace DigitalStarGate.Infrastructure.ObservationSessions;

public sealed class InMemoryObservationSessionRepository : IObservationSessionRepository
{
  private readonly ConcurrentDictionary<Guid, ObservationSession> sessions = new();

  public Task AddAsync(ObservationSession session, CancellationToken cancellationToken)
  {
    cancellationToken.ThrowIfCancellationRequested();

    if (!sessions.TryAdd(session.Id.Value, session))
    {
      throw new InvalidOperationException($"La sessione {session.Id.Value} esiste già.");
    }

    return Task.CompletedTask;
  }

  public Task<ObservationSession?> GetAsync(ObservationSessionId id, CancellationToken cancellationToken)
  {
    cancellationToken.ThrowIfCancellationRequested();
    sessions.TryGetValue(id.Value, out var session);
    return Task.FromResult(session);
  }
}
