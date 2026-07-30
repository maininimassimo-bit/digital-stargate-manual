#pragma warning disable CA1707

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class DegradedDependencyValidationTests
{
  [Fact]
  public void C06_required_dependency_failure_enters_degraded_mode()
  {
    var service = ServiceState.Create("operations-center");

    service.ObserveDependency("telemetry", DependencyCriticality.Required, DependencyStatus.Unavailable);

    Assert.Equal(OperatingMode.Degraded, service.Mode);
    Assert.Contains("telemetry", service.UnavailableDependencies);
  }

  [Fact]
  public void C06_safety_dependency_failure_forces_safe_restriction()
  {
    var service = ServiceState.Create("operations-center");

    service.ObserveDependency("safety-state", DependencyCriticality.SafetyCritical, DependencyStatus.Stale);

    Assert.Equal(OperatingMode.SafeRestricted, service.Mode);
    Assert.False(service.CommandDispatchAllowed);
  }

  [Fact]
  public void C06_optional_dependency_failure_does_not_claim_full_health()
  {
    var service = ServiceState.Create("operations-center");

    service.ObserveDependency("reporting", DependencyCriticality.Optional, DependencyStatus.Unavailable);

    Assert.Equal(OperatingMode.Degraded, service.Mode);
    Assert.False(service.IsFullyHealthy);
  }

  [Fact]
  public void C06_unknown_dependency_outcome_is_not_treated_as_available()
  {
    var service = ServiceState.Create("operations-center");

    service.ObserveDependency("identity", DependencyCriticality.Required, DependencyStatus.Unknown);

    Assert.Equal(OperatingMode.Degraded, service.Mode);
    Assert.Contains("identity", service.UncertainDependencies);
  }

  [Fact]
  public void C06_recovery_requires_stability_window_before_normal_mode()
  {
    var service = ServiceState.Create("operations-center");
    service.ObserveDependency("telemetry", DependencyCriticality.Required, DependencyStatus.Unavailable);

    service.ObserveDependency("telemetry", DependencyCriticality.Required, DependencyStatus.Available);

    Assert.Equal(OperatingMode.Recovering, service.Mode);
    Assert.False(service.TryReturnToNormal(stabilityWindowSatisfied: false, safetyVerified: true));
    Assert.True(service.TryReturnToNormal(stabilityWindowSatisfied: true, safetyVerified: true));
    Assert.Equal(OperatingMode.Normal, service.Mode);
  }

  [Fact]
  public void C06_return_to_service_requires_independent_safety_verification()
  {
    var service = ServiceState.Create("operations-center");
    service.ObserveDependency("safety-state", DependencyCriticality.SafetyCritical, DependencyStatus.Unavailable);
    service.ObserveDependency("safety-state", DependencyCriticality.SafetyCritical, DependencyStatus.Available);

    Assert.False(service.TryReturnToNormal(stabilityWindowSatisfied: true, safetyVerified: false));
    Assert.NotEqual(OperatingMode.Normal, service.Mode);
  }

  [Fact]
  public void C06_mode_transitions_are_recorded_as_evidence()
  {
    var service = ServiceState.Create("operations-center");

    service.ObserveDependency("telemetry", DependencyCriticality.Required, DependencyStatus.Unavailable);
    service.ObserveDependency("telemetry", DependencyCriticality.Required, DependencyStatus.Available);

    Assert.Contains(service.Evidence, item => item.Mode == OperatingMode.Degraded && item.Reason == "dependency-unavailable:telemetry");
    Assert.Contains(service.Evidence, item => item.Mode == OperatingMode.Recovering && item.Reason == "dependencies-restored");
  }

  private sealed class ServiceState
  {
    private readonly Dictionary<string, DependencyObservation> dependencies = new(StringComparer.Ordinal);

    private ServiceState(string serviceId)
    {
      ServiceId = serviceId;
      Mode = OperatingMode.Normal;
      Evidence.Add(new ModeEvidence(Mode, "initialized"));
    }

    public string ServiceId { get; }
    public OperatingMode Mode { get; private set; }
    public bool CommandDispatchAllowed => Mode == OperatingMode.Normal;
    public bool IsFullyHealthy => Mode == OperatingMode.Normal && dependencies.Values.All(item => item.Status == DependencyStatus.Available);
    public IReadOnlyCollection<string> UnavailableDependencies => dependencies.Where(item => item.Value.Status == DependencyStatus.Unavailable).Select(item => item.Key).ToArray();
    public IReadOnlyCollection<string> UncertainDependencies => dependencies.Where(item => item.Value.Status is DependencyStatus.Unknown or DependencyStatus.Stale).Select(item => item.Key).ToArray();
    public List<ModeEvidence> Evidence { get; } = [];

    public static ServiceState Create(string serviceId) => new(serviceId);

    public void ObserveDependency(string dependencyId, DependencyCriticality criticality, DependencyStatus status)
    {
      dependencies[dependencyId] = new DependencyObservation(criticality, status);

      if (status == DependencyStatus.Available)
      {
        if (dependencies.Values.All(item => item.Status == DependencyStatus.Available) && Mode != OperatingMode.Normal)
        {
          TransitionTo(OperatingMode.Recovering, "dependencies-restored");
        }

        return;
      }

      if (criticality == DependencyCriticality.SafetyCritical)
      {
        TransitionTo(OperatingMode.SafeRestricted, $"safety-dependency-{status.ToString().ToLowerInvariant()}:{dependencyId}");
        return;
      }

      var reason = status == DependencyStatus.Unavailable
        ? $"dependency-unavailable:{dependencyId}"
        : $"dependency-uncertain:{dependencyId}";
      TransitionTo(OperatingMode.Degraded, reason);
    }

    public bool TryReturnToNormal(bool stabilityWindowSatisfied, bool safetyVerified)
    {
      if (Mode != OperatingMode.Recovering || !stabilityWindowSatisfied || !safetyVerified)
      {
        return false;
      }

      TransitionTo(OperatingMode.Normal, "return-to-service-validated");
      return true;
    }

    private void TransitionTo(OperatingMode mode, string reason)
    {
      Mode = mode;
      Evidence.Add(new ModeEvidence(mode, reason));
    }
  }

  private enum DependencyCriticality { Optional, Required, SafetyCritical }
  private enum DependencyStatus { Available, Unavailable, Stale, Unknown }
  private enum OperatingMode { Normal, Degraded, SafeRestricted, Recovering }
  private sealed record DependencyObservation(DependencyCriticality Criticality, DependencyStatus Status);
  private sealed record ModeEvidence(OperatingMode Mode, string Reason);
}

#pragma warning restore CA1707
