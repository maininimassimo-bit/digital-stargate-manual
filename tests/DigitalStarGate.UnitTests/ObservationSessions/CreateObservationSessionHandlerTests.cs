using DigitalStarGate.Application.ObservationSessions;
using DigitalStarGate.Contracts.Commands;
using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Contracts.Events;
using DigitalStarGate.Domain.ObservationSessions;
using Microsoft.Extensions.Logging.Abstractions;

namespace DigitalStarGate.UnitTests.ObservationSessions;

public sealed class CreateObservationSessionHandlerTests
{
    [Fact]
    public async Task HandleAsync_PersistsSessionAndPublishesSessionCreated()
    {
        var repository = new TestRepository();
        var publisher = new TestPublisher();
        var now = new DateTimeOffset(2026, 7, 28, 20, 0, 0, TimeSpan.Zero);
        var handler = new CreateObservationSessionHandler(
            repository,
            publisher,
            new FixedTimeProvider(now),
            NullLogger<CreateObservationSessionHandler>.Instance);

        var result = await handler.HandleAsync(
            new CreateObservationSession(
                new TargetId(Guid.NewGuid()),
                new ObservatoryId(Guid.NewGuid()),
                new CorrelationId(Guid.NewGuid())),
            CancellationToken.None);

        var persisted = Assert.IsType<ObservationSession>(repository.Session);
        Assert.Equal(result.Id, persisted.Id);
        var created = Assert.IsType<SessionCreated>(publisher.Event);
        Assert.Equal(result.Id, created.SessionId);
        Assert.Equal(now, created.OccurredAt);
    }

    private sealed class TestRepository : IObservationSessionRepository
    {
        public ObservationSession? Session { get; private set; }

        public Task AddAsync(ObservationSession session, CancellationToken cancellationToken)
        {
            Session = session;
            return Task.CompletedTask;
        }

        public Task<ObservationSession?> GetAsync(ObservationSessionId id, CancellationToken cancellationToken) =>
            Task.FromResult(Session?.Id == id ? Session : null);
    }

    private sealed class TestPublisher : IPlatformEventPublisher
    {
        public IPlatformEvent? Event { get; private set; }

        public Task PublishAsync(IPlatformEvent platformEvent, CancellationToken cancellationToken)
        {
            Event = platformEvent;
            return Task.CompletedTask;
        }
    }

    private sealed class FixedTimeProvider(DateTimeOffset value) : TimeProvider
    {
        public override DateTimeOffset GetUtcNow() => value;
    }
}
