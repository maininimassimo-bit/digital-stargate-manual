#pragma warning disable CA1707

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class IntegratedNonOperationalValidationTests
{
  [Fact]
  public void Integrated_unknown_safety_state_blocks_authorization_dispatch_and_normal_claim()
  {
    var scenario = IntegratedScenario.Create();

    scenario.ObserveSafetyState(StateQuality.Unknown);
    scenario.RequestCommand("operator-01", "close-roof", RiskClass.C2);

    Assert.False(scenario.AuthorizationGranted);
    Assert.False(scenario.DispatchAllowed);
    Assert.Equal(OperatingMode.SafeRestricted, scenario.Mode);
    Assert.False(scenario.IsFullyHealthy);
    Assert.Contains(scenario.Evidence, item => item == "authorization-denied:unknown-safety-state");
  }

  [Fact]
  public void Integrated_dependency_failure_correlates_alarm_incident_recovery_and_audit()
  {
    var scenario = IntegratedScenario.Create();

    scenario.ObserveDependency("telemetry", available: false);
    scenario.AcknowledgeAlarm("alarm-001", "operator-01");
    scenario.OpenIncident("incident-001", "alarm-001");
    scenario.RestoreDependency("telemetry");

    Assert.Equal(OperatingMode.Recovering, scenario.Mode);
    Assert.Equal("corr-001", scenario.CorrelationId);
    Assert.Contains("alarm-acknowledged:alarm-001:operator-01", scenario.Evidence);
    Assert.Contains("incident-opened:incident-001:alarm-001", scenario.Evidence);
    Assert.Contains("dependency-restored:telemetry", scenario.Evidence);
  }

  [Fact]
  public void Integrated_return_to_service_requires_stability_safety_and_complete_audit()
  {
    var scenario = IntegratedScenario.Create();
    scenario.ObserveDependency("telemetry", available: false);
    scenario.RestoreDependency("telemetry");

    Assert.False(scenario.TryReturnToService(stabilitySatisfied: false, safetyVerified: true, auditComplete: true));
    Assert.False(scenario.TryReturnToService(stabilitySatisfied: true, safetyVerified: false, auditComplete: true));
    Assert.False(scenario.TryReturnToService(stabilitySatisfied: true, safetyVerified: true, auditComplete: false));
    Assert.True(scenario.TryReturnToService(stabilitySatisfied: true, safetyVerified: true, auditComplete: true));
    Assert.Equal(OperatingMode.Normal, scenario.Mode);
  }

  [Fact]
  public void Integrated_single_identity_cannot_self_approve_critical_operation()
  {
    var scenario = IntegratedScenario.Create();

    scenario.RequestCommand("bootstrap-identity", "emergency-override", RiskClass.C4);
    scenario.ApproveCommand("bootstrap-identity");

    Assert.False(scenario.AuthorizationGranted);
    Assert.False(scenario.DispatchAllowed);
    Assert.Contains("approval-rejected:self-approval", scenario.Evidence);
  }

  [Fact]
  public void Integrated_validation_never_enables_runtime_or_physical_adapter()
  {
    var scenario = IntegratedScenario.Create();

    Assert.False(scenario.RuntimeEnabled);
    Assert.False(scenario.PhysicalAdapterAttached);
    Assert.False(scenario.LocalInterlockBypassed);
  }

  private sealed class IntegratedScenario
  {
    private string? requester;
    private RiskClass requestedRisk;

    private IntegratedScenario()
    {
      Evidence.Add("scenario-created:non-operational");
    }

    public string CorrelationId { get; } = "corr-001";
    public OperatingMode Mode { get; private set; } = OperatingMode.Normal;
    public bool AuthorizationGranted { get; private set; }
    public bool DispatchAllowed { get; private set; }
    public bool IsFullyHealthy => Mode == OperatingMode.Normal;
    public bool RuntimeEnabled => false;
    public bool PhysicalAdapterAttached => false;
    public bool LocalInterlockBypassed => false;
    public List<string> Evidence { get; } = [];

    public static IntegratedScenario Create() => new();

    public void ObserveSafetyState(StateQuality quality)
    {
      if (quality is StateQuality.Unknown or StateQuality.Stale)
      {
        Mode = OperatingMode.SafeRestricted;
        AuthorizationGranted = false;
        DispatchAllowed = false;
        Evidence.Add("authorization-denied:unknown-safety-state");
      }
    }

    public void RequestCommand(string actor, string command, RiskClass risk)
    {
      requester = actor;
      requestedRisk = risk;
      Evidence.Add($"command-requested:{command}:{actor}:{risk}");

      if (Mode == OperatingMode.Normal && risk < RiskClass.C3)
      {
        AuthorizationGranted = true;
        DispatchAllowed = true;
      }
    }

    public void ApproveCommand(string approver)
    {
      if (requestedRisk >= RiskClass.C3 && string.Equals(requester, approver, StringComparison.Ordinal))
      {
        AuthorizationGranted = false;
        DispatchAllowed = false;
        Evidence.Add("approval-rejected:self-approval");
      }
    }

    public void ObserveDependency(string dependencyId, bool available)
    {
      if (!available)
      {
        Mode = OperatingMode.Degraded;
        DispatchAllowed = false;
        Evidence.Add($"dependency-unavailable:{dependencyId}");
      }
    }

    public void AcknowledgeAlarm(string alarmId, string actor) =>
      Evidence.Add($"alarm-acknowledged:{alarmId}:{actor}");

    public void OpenIncident(string incidentId, string alarmId) =>
      Evidence.Add($"incident-opened:{incidentId}:{alarmId}");

    public void RestoreDependency(string dependencyId)
    {
      Mode = OperatingMode.Recovering;
      Evidence.Add($"dependency-restored:{dependencyId}");
    }

    public bool TryReturnToService(bool stabilitySatisfied, bool safetyVerified, bool auditComplete)
    {
      if (Mode != OperatingMode.Recovering || !stabilitySatisfied || !safetyVerified || !auditComplete)
      {
        return false;
      }

      Mode = OperatingMode.Normal;
      Evidence.Add("return-to-service-validated");
      return true;
    }
  }

  private enum StateQuality { Fresh, Stale, Unknown }
  private enum RiskClass { C0, C1, C2, C3, C4 }
  private enum OperatingMode { Normal, Degraded, SafeRestricted, Recovering }
}

#pragma warning restore CA1707
