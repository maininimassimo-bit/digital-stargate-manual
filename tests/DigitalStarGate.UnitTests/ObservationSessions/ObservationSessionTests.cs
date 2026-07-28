using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Domain.ObservationSessions;

namespace DigitalStarGate.UnitTests.ObservationSessions;

public sealed class ObservationSessionTests
{
    [Fact]
    public void Create_WithValidValues_CreatesSessionInCreatedState()
    {
        var session = ObservationSession.Create(
            new ObservationSessionId(Guid.NewGuid()),
            new TargetId(Guid.NewGuid()),
            new ObservatoryId(Guid.NewGuid()),
            Guid.NewGuid(),
            DateTimeOffset.UtcNow);

        Assert.Equal(ObservationSessionStatus.Created, session.Status);
        Assert.NotEqual(Guid.Empty, session.ObservationPlanId);
    }

    [Fact]
    public void Create_WithEmptyTarget_ThrowsArgumentException()
    {
        Assert.Throws<ArgumentException>(() => ObservationSession.Create(
            new ObservationSessionId(Guid.NewGuid()),
            new TargetId(Guid.Empty),
            new ObservatoryId(Guid.NewGuid()),
            Guid.NewGuid(),
            DateTimeOffset.UtcNow));
    }
}
