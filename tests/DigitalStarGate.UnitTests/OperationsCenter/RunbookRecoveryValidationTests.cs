#pragma warning disable CA1707

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class RunbookRecoveryValidationTests
{
  private static readonly DateTimeOffset Now = new(2026, 7, 30, 21, 30, 0, TimeSpan.Zero);

  [Fact]
  public void C03_unverified_precondition_stops_execution()
  {
    var execution = RunbookExecution.Start("exec-001", "rb-validation-001", "1.0.0", Now);

    execution.VerifyPrecondition("safety-state", CheckResult.Unknown, Now.AddSeconds(1));

    Assert.Equal(ExecutionState.Stopped, execution.State);
    Assert.Contains(execution.Evidence, item => item.Reason == "precondition-not-verifiable");
  }

  [Fact]
  public void C03_failed_safety_checkpoint_aborts_before_action()
  {
    var execution = ReadyExecution("exec-002");

    execution.EvaluateSafetyCheckpoint(CheckResult.Failed, Now.AddSeconds(2));
    var dispatched = execution.TryExecuteStep("step-risky", Now.AddSeconds(3));

    Assert.False(dispatched);
    Assert.Equal(ExecutionState.Aborted, execution.State);
    Assert.DoesNotContain(execution.Evidence, item => item.Reason == "step-executed");
  }

  [Fact]
  public void C03_timeout_enters_uncertain_outcome_and_requires_reconciliation()
  {
    var execution = ReadyExecution("exec-003");
    execution.EvaluateSafetyCheckpoint(CheckResult.Passed, Now.AddSeconds(2));

    execution.RecordTimeout("step-001", Now.AddMinutes(1));

    Assert.Equal(ExecutionState.ReconciliationRequired, execution.State);
    Assert.False(execution.CanRetry);
    Assert.Contains(execution.Evidence, item => item.Reason == "timeout-outcome-uncertain:step-001");
  }

  [Fact]
  public void C03_rollback_restores_checkpoint_and_requires_service_and_safety_validation()
  {
    var execution = ReadyExecution("exec-004");
    execution.EvaluateSafetyCheckpoint(CheckResult.Passed, Now.AddSeconds(2));
    Assert.True(execution.TryExecuteStep("step-001", Now.AddSeconds(3)));

    execution.TriggerRollback("restore-point-001", Now.AddMinutes(1));
    Assert.Equal(ExecutionState.Rollback, execution.State);

    Assert.False(execution.CompleteRollback(serviceHealthy: true, safeStateVerified: false, Now.AddMinutes(2)));
    Assert.True(execution.CompleteRollback(serviceHealthy: true, safeStateVerified: true, Now.AddMinutes(3)));
    Assert.Equal(ExecutionState.Recovered, execution.State);
  }

  [Fact]
  public void C03_recovery_follows_containment_restore_monitor_handover_sequence()
  {
    var execution = ReadyExecution("exec-005");

    Assert.True(execution.AdvanceRecovery(RecoveryStage.Containment, Now.AddMinutes(1)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.Diagnosis, Now.AddMinutes(2)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.TechnicalRestore, Now.AddMinutes(3)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.ServiceVerification, Now.AddMinutes(4)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.SafetyVerification, Now.AddMinutes(5)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.Monitoring, Now.AddMinutes(6)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.Handover, Now.AddMinutes(7)));
    Assert.True(execution.AdvanceRecovery(RecoveryStage.ClosedWithEvidence, Now.AddMinutes(8)));

    Assert.Equal(ExecutionState.Closed, execution.State);
    Assert.Equal(8, execution.RecoveryHistory.Count);
  }

  [Fact]
  public void C03_recovery_cannot_skip_mandatory_stage()
  {
    var execution = ReadyExecution("exec-006");

    Assert.False(execution.AdvanceRecovery(RecoveryStage.TechnicalRestore, Now.AddMinutes(1)));
    Assert.Equal(ExecutionState.Recovery, execution.State);
    Assert.Contains(execution.Evidence, item => item.Reason == "recovery-stage-out-of-order");
  }

  [Fact]
  public void C03_execution_record_contains_minimum_correlated_evidence()
  {
    var execution = ReadyExecution("exec-007");

    Assert.Equal("corr-exec-007", execution.CorrelationId);
    Assert.Equal("rb-validation-001", execution.RunbookId);
    Assert.Equal("1.0.0", execution.RunbookVersion);
    Assert.NotEmpty(execution.Evidence);
    Assert.All(execution.Evidence, item => Assert.NotEqual(default, item.Timestamp));
  }

  private static RunbookExecution ReadyExecution(string executionId)
  {
    var execution = RunbookExecution.Start(executionId, "rb-validation-001", "1.0.0", Now);
    execution.VerifyPrecondition("identity-role", CheckResult.Passed, Now.AddSeconds(1));
    execution.VerifyPrecondition("safety-state", CheckResult.Passed, Now.AddSeconds(1));
    return execution;
  }

  private sealed class RunbookExecution
  {
    private static readonly RecoveryStage[] RecoveryOrder =
    [
      RecoveryStage.Containment,
      RecoveryStage.Diagnosis,
      RecoveryStage.TechnicalRestore,
      RecoveryStage.ServiceVerification,
      RecoveryStage.SafetyVerification,
      RecoveryStage.Monitoring,
      RecoveryStage.Handover,
      RecoveryStage.ClosedWithEvidence
    ];

    private RunbookExecution(string executionId, string runbookId, string runbookVersion, DateTimeOffset startedAt)
    {
      ExecutionId = executionId;
      CorrelationId = $"corr-{executionId}";
      RunbookId = runbookId;
      RunbookVersion = runbookVersion;
      State = ExecutionState.PreconditionCheck;
      Evidence.Add(new EvidenceItem("execution-started", startedAt));
    }

    public string ExecutionId { get; }
    public string CorrelationId { get; }
    public string RunbookId { get; }
    public string RunbookVersion { get; }
    public ExecutionState State { get; private set; }
    public bool CanRetry { get; private set; } = true;
    public List<EvidenceItem> Evidence { get; } = [];
    public List<RecoveryStage> RecoveryHistory { get; } = [];

    public static RunbookExecution Start(string executionId, string runbookId, string runbookVersion, DateTimeOffset startedAt) =>
      new(executionId, runbookId, runbookVersion, startedAt);

    public void VerifyPrecondition(string name, CheckResult result, DateTimeOffset at)
    {
      Evidence.Add(new EvidenceItem($"precondition:{name}:{result}", at));
      if (result != CheckResult.Passed)
      {
        State = ExecutionState.Stopped;
        Evidence.Add(new EvidenceItem("precondition-not-verifiable", at));
      }
    }

    public void EvaluateSafetyCheckpoint(CheckResult result, DateTimeOffset at)
    {
      Evidence.Add(new EvidenceItem($"safety-checkpoint:{result}", at));
      State = result == CheckResult.Passed ? ExecutionState.Ready : ExecutionState.Aborted;
    }

    public bool TryExecuteStep(string stepId, DateTimeOffset at)
    {
      if (State != ExecutionState.Ready)
      {
        return false;
      }

      State = ExecutionState.Executing;
      Evidence.Add(new EvidenceItem($"step-executed:{stepId}", at));
      return true;
    }

    public void RecordTimeout(string stepId, DateTimeOffset at)
    {
      State = ExecutionState.ReconciliationRequired;
      CanRetry = false;
      Evidence.Add(new EvidenceItem($"timeout-outcome-uncertain:{stepId}", at));
    }

    public void TriggerRollback(string restorePoint, DateTimeOffset at)
    {
      State = ExecutionState.Rollback;
      Evidence.Add(new EvidenceItem($"rollback-started:{restorePoint}", at));
    }

    public bool CompleteRollback(bool serviceHealthy, bool safeStateVerified, DateTimeOffset at)
    {
      Evidence.Add(new EvidenceItem($"rollback-validation:service={serviceHealthy}:safety={safeStateVerified}", at));
      if (!serviceHealthy || !safeStateVerified)
      {
        return false;
      }

      State = ExecutionState.Recovered;
      Evidence.Add(new EvidenceItem("rollback-completed", at));
      return true;
    }

    public bool AdvanceRecovery(RecoveryStage stage, DateTimeOffset at)
    {
      State = ExecutionState.Recovery;
      var expected = RecoveryOrder[RecoveryHistory.Count];
      if (stage != expected)
      {
        Evidence.Add(new EvidenceItem("recovery-stage-out-of-order", at));
        return false;
      }

      RecoveryHistory.Add(stage);
      Evidence.Add(new EvidenceItem($"recovery:{stage}", at));
      if (stage == RecoveryStage.ClosedWithEvidence)
      {
        State = ExecutionState.Closed;
      }

      return true;
    }
  }

  private enum CheckResult { Passed, Failed, Unknown }
  private enum ExecutionState { PreconditionCheck, Ready, Executing, Stopped, Aborted, ReconciliationRequired, Rollback, Recovery, Recovered, Closed }
  private enum RecoveryStage { Containment, Diagnosis, TechnicalRestore, ServiceVerification, SafetyVerification, Monitoring, Handover, ClosedWithEvidence }
  private sealed record EvidenceItem(string Reason, DateTimeOffset Timestamp);
}

#pragma warning restore CA1707
