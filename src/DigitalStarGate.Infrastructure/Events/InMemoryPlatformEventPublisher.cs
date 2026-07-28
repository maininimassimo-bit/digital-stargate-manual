using System.Collections.Concurrent;
using DigitalStarGate.Application.ObservationSessions;
using DigitalStarGate.Contracts.Events;

namespace DigitalStarGate.Infrastructure.Events;

public sealed class InMemoryPlatformEventPublisher : IPlatformEventPublisher
{
  private readonly ConcurrentQueue<IPlatformEvent> events = new();

  public IReadOnlyCollection<IPlatformEvent> PublishedEvents => events.ToArray();

  public Task PublishAsync(IPlatformEvent platformEvent, CancellationToken cancellationToken)
  {
    cancellationToken.ThrowIfCancellationRequested();
    events.Enqueue(platformEvent);
    return Task.CompletedTask;
  }
}
