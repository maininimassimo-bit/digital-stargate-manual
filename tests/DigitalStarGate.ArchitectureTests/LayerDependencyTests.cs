using DigitalStarGate.Domain.ObservationSessions;

namespace DigitalStarGate.ArchitectureTests;

public sealed class LayerDependencyTests
{
    [Fact]
    public void DomainDoesNotReferenceOuterLayers()
    {
        var references = typeof(ObservationSession).Assembly
            .GetReferencedAssemblies()
            .Select(assembly => assembly.Name)
            .ToArray();

        Assert.DoesNotContain("DigitalStarGate.Application", references);
        Assert.DoesNotContain("DigitalStarGate.Infrastructure", references);
        Assert.DoesNotContain("DigitalStarGate.Api", references);
    }
}