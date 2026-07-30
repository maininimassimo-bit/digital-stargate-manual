#pragma warning disable CA1707
using System.Collections.Concurrent;

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class AuthorizationSecurityValidationTests
{
  private static readonly DateTimeOffset Now = new(2026, 7, 30, 20, 0, 0, TimeSpan.Zero);

  [Fact]
  public void C01_authorized_C1_command_is_executed_once_with_complete_audit()
  {
    var harness = Harness.Create(Now);
    var result = harness.Execute(Request("cmd-001", CommandClass.C1, "operator", "approver", TelemetryState.Fresh));

    Assert.True(result.Allowed);
    Assert.Equal(1, harness.Dispatcher.ExecutionCount("cmd-001"));

    var entry = Assert.Single(harness.Audit.Entries);
    Assert.Equal("operator", entry.Actor);
    Assert.Equal(Role.Operator, entry.ActorRole);
    Assert.Equal("corr-cmd-001", entry.CorrelationId);
    Assert.Equal("sha256:cmd-001", entry.PayloadHash);
    Assert.Equal("policy-v2", entry.PolicyVersion);
    Assert.Equal("not-required", entry.SafetyDecision);
    Assert.Equal("operator>approver", entry.ApprovalChain);
    Assert.Equal("executed", entry.Outcome);
  }

  [Fact]
  public void C01_C3_command_without_distinct_approver_is_denied()
  {
    var harness = Harness.Create(Now);
    var result = harness.Execute(Request("cmd-002", CommandClass.C3, "operator", "operator", TelemetryState.Fresh));

    Assert.False(result.Allowed);
    Assert.Equal("four-eyes-required", result.Reason);
    Assert.Equal(0, harness.Dispatcher.ExecutionCount("cmd-002"));
  }

  [Fact]
  public void C01_expired_authorization_is_denied()
  {
    var harness = Harness.Create(Now);
    var request = Request("cmd-003", CommandClass.C2, "operator", "approver", TelemetryState.Fresh) with
    {
      AuthorizationExpiresAt = Now.AddSeconds(-1)
    };

    var result = harness.Execute(request);

    Assert.False(result.Allowed);
    Assert.Equal("authorization-expired", result.Reason);
  }

  [Theory]
  [InlineData(TelemetryState.Stale)]
  [InlineData(TelemetryState.Unknown)]
  [InlineData(TelemetryState.Conflicting)]
  public void C01_non_fresh_telemetry_denies_safety_relevant_commands(TelemetryState telemetry)
  {
    var harness = Harness.Create(Now);
    var result = harness.Execute(Request("cmd-telemetry-" + telemetry, CommandClass.C3, "operator", "approver", telemetry));

    Assert.False(result.Allowed);
    Assert.Equal("telemetry-not-trustworthy", result.Reason);
  }

  [Fact]
  public void C01_safety_authority_denial_has_precedence()
  {
    var harness = Harness.Create(Now, safetyAllows: false);
    var result = harness.Execute(Request("cmd-004", CommandClass.C4, "operator", "approver", TelemetryState.Fresh));

    Assert.False(result.Allowed);
    Assert.Equal("safety-denied", result.Reason);
    Assert.Equal("deny", Assert.Single(harness.Audit.Entries).SafetyDecision);
    Assert.Equal(0, harness.Dispatcher.ExecutionCount("cmd-004"));
  }

  [Fact]
  public void C01_timeout_retry_reconciles_without_duplicate_execution()
  {
    var harness = Harness.Create(Now);
    harness.Dispatcher.TimeoutAfterExecutionOnce("cmd-005");
    var request = Request("cmd-005", CommandClass.C2, "operator", "approver", TelemetryState.Fresh);

    var first = harness.Execute(request);
    var retry = harness.Execute(request);

    Assert.False(first.Allowed);
    Assert.Equal("dispatch-timeout-reconciliation-required", first.Reason);
    Assert.True(retry.Allowed);
    Assert.True(retry.IdempotentReplay);
    Assert.Equal(1, harness.Dispatcher.ExecutionCount("cmd-005"));
    Assert.Contains(harness.Audit.Entries, entry => entry.Outcome == "reconciled");
  }

  [Fact]
  public void C01_privilege_revoked_between_approval_and_execution_is_denied()
  {
    var harness = Harness.Create(Now);
    harness.BeforeDispatch = () => harness.Identity.Revoke("operator");

    var result = harness.Execute(Request("cmd-006", CommandClass.C3, "operator", "approver", TelemetryState.Fresh));

    Assert.False(result.Allowed);
    Assert.Equal("requester-revoked-before-dispatch", result.Reason);
    Assert.Equal(0, harness.Dispatcher.ExecutionCount("cmd-006"));
  }

  [Fact]
  public void C01_user_without_role_is_denied_and_security_event_is_emitted()
  {
    var harness = Harness.Create(Now);
    var result = harness.Execute(Request("cmd-007", CommandClass.C1, "unknown-user", "approver", TelemetryState.Fresh));

    Assert.False(result.Allowed);
    Assert.Equal("requester-not-authorized", result.Reason);
    Assert.Contains(harness.SecurityEvents, item => item.Code == "SEC-UNAUTHORIZED-COMMAND" && item.Principal == "unknown-user");
  }

  [Fact]
  public void C05_privileged_access_requires_distinct_approver_and_is_time_bound()
  {
    var controller = new BreakGlassController(Now);

    Assert.Throws<InvalidOperationException>(() =>
      controller.Grant("maintainer", "maintainer", "maintenance", Now.AddMinutes(15), "approved-change"));

    var grant = controller.Grant("maintainer", "security-approver", "maintenance", Now.AddMinutes(15), "approved-change");

    Assert.True(controller.IsAuthorized(grant.Token, "maintenance", Now.AddMinutes(5)));
    Assert.False(controller.IsAuthorized(grant.Token, "command-execution", Now.AddMinutes(5)));
    Assert.Equal("security-approver", grant.Approver);
    Assert.Contains(controller.Notifications, item => item.Token == grant.Token && item.Event == "grant-created");
  }

  [Fact]
  public void C05_break_glass_requires_reason_and_can_be_revoked()
  {
    var controller = new BreakGlassController(Now);
    Assert.Throws<ArgumentException>(() =>
      controller.Grant("security-admin", "security-approver", "diagnostics", Now.AddMinutes(10), string.Empty));

    var grant = controller.Grant("security-admin", "security-approver", "diagnostics", Now.AddMinutes(10), "identity-provider-outage");
    controller.Revoke(grant.Token, "incident-contained", Now.AddMinutes(2));

    Assert.False(controller.IsAuthorized(grant.Token, "diagnostics", Now.AddMinutes(3)));
    Assert.Contains(controller.Audit, entry => entry.Action == "revoked" && entry.Token == grant.Token);
    Assert.Contains(controller.Notifications, item => item.Token == grant.Token && item.Event == "grant-revoked");
  }

  [Fact]
  public void C05_expiry_creates_automatic_revocation_record()
  {
    var controller = new BreakGlassController(Now);
    var grant = controller.Grant("maintainer", "security-approver", "maintenance", Now.AddMinutes(10), "approved-change");

    Assert.False(controller.IsAuthorized(grant.Token, "maintenance", Now.AddMinutes(11)));
    Assert.Contains(controller.Audit, item => item.Token == grant.Token && item.Action == "auto-revoked-expired");
    Assert.Contains(controller.Notifications, item => item.Token == grant.Token && item.Event == "grant-expired");
  }

  [Fact]
  public void C05_reuse_after_revocation_emits_security_event()
  {
    var controller = new BreakGlassController(Now);
    var grant = controller.Grant("maintainer", "security-approver", "maintenance", Now.AddMinutes(10), "approved-change");
    controller.Revoke(grant.Token, "incident-contained", Now.AddMinutes(2));

    Assert.False(controller.IsAuthorized(grant.Token, "maintenance", Now.AddMinutes(3)));
    Assert.Contains(controller.SecurityEvents, item => item.Code == "SEC-REVOKED-TOKEN-REUSE" && item.Principal == "maintainer");
  }

  [Fact]
  public void C05_post_review_is_required_before_break_glass_closure()
  {
    var controller = new BreakGlassController(Now);
    var grant = controller.Grant("maintainer", "security-approver", "maintenance", Now.AddMinutes(10), "approved-change");
    controller.Revoke(grant.Token, "work-completed", Now.AddMinutes(4));

    Assert.False(controller.CanClose(grant.Token));

    controller.CompletePostReview(grant.Token, "independent-reviewer", "no-anomalies", Now.AddMinutes(8));

    Assert.True(controller.CanClose(grant.Token));
    Assert.Contains(controller.Audit, item => item.Token == grant.Token && item.Action == "post-review-completed");
  }

  [Fact]
  public void C05_security_authority_cannot_declare_safe_state_or_gain_command_authority()
  {
    var harness = Harness.Create(Now);
    var result = harness.Execute(Request("cmd-008", CommandClass.C1, "security-admin", "approver", TelemetryState.Fresh));

    Assert.False(result.Allowed);
    Assert.Equal("requester-not-authorized", result.Reason);
    Assert.False(harness.Identity.CanDeclareSafeState("security-admin"));
  }

  [Fact]
  public void C05_auditor_is_read_only()
  {
    var harness = Harness.Create(Now);
    var result = harness.Execute(Request("cmd-009", CommandClass.C1, "auditor", "approver", TelemetryState.Fresh));

    Assert.False(result.Allowed);
    Assert.True(harness.Identity.CanReadAudit("auditor"));
  }

  private static CommandRequest Request(
    string id,
    CommandClass commandClass,
    string requester,
    string approver,
    TelemetryState telemetry) =>
    new(
      id,
      "corr-" + id,
      "sha256:" + id,
      commandClass,
      requester,
      approver,
      telemetry,
      Now.AddMinutes(5),
      "policy-v2");

  private sealed class Harness
  {
    private Harness(DateTimeOffset now, bool safetyAllows)
    {
      Now = now;
      Identity = new IdentityStub();
      Identity.Assign("operator", Role.Operator);
      Identity.Assign("approver", Role.SeniorOperator);
      Identity.Assign("security-admin", Role.SecurityAuthority);
      Identity.Assign("safety-authority", Role.SafetyAuthority);
      Identity.Assign("auditor", Role.Auditor);
      SafetyAllows = safetyAllows;
    }

    public DateTimeOffset Now { get; }
    public IdentityStub Identity { get; }
    public FakeCommandDispatcher Dispatcher { get; } = new();
    public AppendOnlyAuditSink Audit { get; } = new();
    public IdempotencyStore Idempotency { get; } = new();
    public List<SecurityEvent> SecurityEvents { get; } = [];
    public Action? BeforeDispatch { get; set; }
    private bool SafetyAllows { get; }

    public static Harness Create(DateTimeOffset now, bool safetyAllows = true) => new(now, safetyAllows);

    public Decision Execute(CommandRequest request)
    {
      Decision decision;
      var safetyDecision = request.Class == CommandClass.C4 ? (SafetyAllows ? "permit" : "deny") : "not-required";

      if (!Identity.CanRequestCommand(request.Requester))
      {
        decision = Decision.Deny("requester-not-authorized");
        SecurityEvents.Add(new SecurityEvent("SEC-UNAUTHORIZED-COMMAND", request.Requester, request.CorrelationId, Now));
      }
      else if (request.AuthorizationExpiresAt <= Now)
      {
        decision = Decision.Deny("authorization-expired");
      }
      else if (request.Class is CommandClass.C3 or CommandClass.C4 && request.Requester == request.Approver)
      {
        decision = Decision.Deny("four-eyes-required");
      }
      else if (request.Class is CommandClass.C3 or CommandClass.C4 && !Identity.CanApproveCommand(request.Approver))
      {
        decision = Decision.Deny("approver-not-authorized");
      }
      else if (request.Class is CommandClass.C3 or CommandClass.C4 && request.Telemetry != TelemetryState.Fresh)
      {
        decision = Decision.Deny("telemetry-not-trustworthy");
      }
      else if (!SafetyAllows)
      {
        decision = Decision.Deny("safety-denied");
      }
      else if (!Idempotency.TryBegin(request.CommandId))
      {
        decision = Decision.AllowReplay();
      }
      else
      {
        BeforeDispatch?.Invoke();
        if (!Identity.CanRequestCommand(request.Requester))
        {
          decision = Decision.Deny("requester-revoked-before-dispatch");
        }
        else
        {
          var dispatch = Dispatcher.Execute(request.CommandId);
          decision = dispatch == DispatchOutcome.TimeoutAfterExecution
            ? Decision.Deny("dispatch-timeout-reconciliation-required")
            : Decision.Allow();
        }
      }

      var outcome = decision.IdempotentReplay
        ? "reconciled"
        : decision.Allowed
          ? "executed"
          : "denied";

      Audit.Append(new AuditEntry(
        request.CommandId,
        request.CorrelationId,
        request.PayloadHash,
        request.Requester,
        Identity.RoleOf(request.Requester),
        request.Approver,
        request.Class,
        request.PolicyVersion,
        safetyDecision,
        request.Requester + ">" + request.Approver,
        outcome,
        decision.Reason,
        Now));

      return decision;
    }
  }

  private sealed class IdentityStub
  {
    private readonly Dictionary<string, Role> assignments = new(StringComparer.Ordinal);
    private readonly HashSet<string> revoked = new(StringComparer.Ordinal);

    public void Assign(string principal, Role role) => assignments[principal] = role;
    public void Revoke(string principal) => revoked.Add(principal);
    public Role RoleOf(string principal) => assignments.TryGetValue(principal, out var role) ? role : Role.None;

    public bool CanRequestCommand(string principal) =>
      !revoked.Contains(principal) &&
      assignments.TryGetValue(principal, out var role) &&
      role is Role.Operator or Role.SeniorOperator;

    public bool CanApproveCommand(string principal) =>
      !revoked.Contains(principal) &&
      assignments.TryGetValue(principal, out var role) &&
      role == Role.SeniorOperator;

    public bool CanDeclareSafeState(string principal) =>
      assignments.TryGetValue(principal, out var role) && role == Role.SafetyAuthority;

    public bool CanReadAudit(string principal) =>
      assignments.TryGetValue(principal, out var role) && role == Role.Auditor;
  }

  private sealed class FakeCommandDispatcher
  {
    private readonly ConcurrentDictionary<string, int> executions = new(StringComparer.Ordinal);
    private readonly HashSet<string> timeoutOnce = new(StringComparer.Ordinal);

    public void TimeoutAfterExecutionOnce(string commandId) => timeoutOnce.Add(commandId);

    public DispatchOutcome Execute(string commandId)
    {
      executions.AddOrUpdate(commandId, 1, (_, count) => count + 1);
      return timeoutOnce.Remove(commandId) ? DispatchOutcome.TimeoutAfterExecution : DispatchOutcome.Executed;
    }

    public int ExecutionCount(string commandId) => executions.TryGetValue(commandId, out var count) ? count : 0;
  }

  private sealed class IdempotencyStore
  {
    private readonly HashSet<string> commandIds = new(StringComparer.Ordinal);
    public bool TryBegin(string commandId) => commandIds.Add(commandId);
  }

  private sealed class AppendOnlyAuditSink
  {
    private readonly List<AuditEntry> entries = [];
    public IReadOnlyList<AuditEntry> Entries => entries;
    public void Append(AuditEntry entry) => entries.Add(entry);
  }

  private sealed class BreakGlassController(DateTimeOffset issuedAt)
  {
    private readonly Dictionary<string, BreakGlassGrant> grants = new(StringComparer.Ordinal);
    private readonly List<BreakGlassAudit> audit = [];
    private readonly List<NotificationRecord> notifications = [];
    private readonly List<SecurityEvent> securityEvents = [];
    private readonly HashSet<string> postReviewed = new(StringComparer.Ordinal);

    public IReadOnlyList<BreakGlassAudit> Audit => audit;
    public IReadOnlyList<NotificationRecord> Notifications => notifications;
    public IReadOnlyList<SecurityEvent> SecurityEvents => securityEvents;

    public BreakGlassGrant Grant(
      string principal,
      string approver,
      string scope,
      DateTimeOffset expiresAt,
      string reason)
    {
      if (string.IsNullOrWhiteSpace(reason))
      {
        throw new ArgumentException("Break-glass reason is required.", nameof(reason));
      }

      if (principal == approver)
      {
        throw new InvalidOperationException("Break-glass requester and approver must be distinct.");
      }

      ArgumentOutOfRangeException.ThrowIfLessThanOrEqual(expiresAt, issuedAt);

      var token = Guid.NewGuid().ToString("N");
      var grant = new BreakGlassGrant(token, principal, approver, scope, reason, issuedAt, expiresAt, false);
      grants[token] = grant;
      audit.Add(new BreakGlassAudit(token, "granted", approver, issuedAt));
      notifications.Add(new NotificationRecord(token, "grant-created", issuedAt));
      return grant;
    }

    public bool IsAuthorized(string token, string scope, DateTimeOffset at)
    {
      if (!grants.TryGetValue(token, out var grant))
      {
        return false;
      }

      if (grant.Revoked)
      {
        securityEvents.Add(new SecurityEvent("SEC-REVOKED-TOKEN-REUSE", grant.Principal, token, at));
        return false;
      }

      if (at >= grant.ExpiresAt)
      {
        grants[token] = grant with { Revoked = true };
        audit.Add(new BreakGlassAudit(token, "auto-revoked-expired", "system", at));
        notifications.Add(new NotificationRecord(token, "grant-expired", at));
        return false;
      }

      return grant.Scope == scope && at >= grant.IssuedAt;
    }

    public void Revoke(string token, string reason, DateTimeOffset at)
    {
      if (!grants.TryGetValue(token, out var grant))
      {
        return;
      }

      grants[token] = grant with { Revoked = true };
      audit.Add(new BreakGlassAudit(token, "revoked", reason, at));
      notifications.Add(new NotificationRecord(token, "grant-revoked", at));
    }

    public void CompletePostReview(string token, string reviewer, string outcome, DateTimeOffset at)
    {
      if (!grants.ContainsKey(token))
      {
        throw new InvalidOperationException("Unknown break-glass token.");
      }

      postReviewed.Add(token);
      audit.Add(new BreakGlassAudit(token, "post-review-completed", reviewer + ":" + outcome, at));
    }

    public bool CanClose(string token) =>
      grants.TryGetValue(token, out var grant) &&
      grant.Revoked &&
      postReviewed.Contains(token) &&
      notifications.Any(item => item.Token == token && item.Event == "grant-created") &&
      notifications.Any(item => item.Token == token && item.Event is "grant-revoked" or "grant-expired");
  }

  private enum DispatchOutcome { Executed, TimeoutAfterExecution }
  private enum CommandClass { C1, C2, C3, C4 }
  public enum TelemetryState { Fresh, Stale, Unknown, Conflicting }
  private enum Role { None, Operator, SeniorOperator, SafetyAuthority, SecurityAuthority, Auditor }

  private sealed record CommandRequest(
    string CommandId,
    string CorrelationId,
    string PayloadHash,
    CommandClass Class,
    string Requester,
    string Approver,
    TelemetryState Telemetry,
    DateTimeOffset AuthorizationExpiresAt,
    string PolicyVersion);

  private sealed record Decision(bool Allowed, string Reason, bool IdempotentReplay)
  {
    public static Decision Allow() => new(true, "allowed", false);
    public static Decision AllowReplay() => new(true, "idempotent-replay", true);
    public static Decision Deny(string reason) => new(false, reason, false);
  }

  private sealed record AuditEntry(
    string CommandId,
    string CorrelationId,
    string PayloadHash,
    string Actor,
    Role ActorRole,
    string Approver,
    CommandClass CommandClass,
    string PolicyVersion,
    string SafetyDecision,
    string ApprovalChain,
    string Outcome,
    string Reason,
    DateTimeOffset Timestamp);

  private sealed record BreakGlassGrant(
    string Token,
    string Principal,
    string Approver,
    string Scope,
    string Reason,
    DateTimeOffset IssuedAt,
    DateTimeOffset ExpiresAt,
    bool Revoked);

  private sealed record BreakGlassAudit(string Token, string Action, string Detail, DateTimeOffset Timestamp);
  private sealed record NotificationRecord(string Token, string Event, DateTimeOffset Timestamp);
  private sealed record SecurityEvent(string Code, string Principal, string CorrelationId, DateTimeOffset Timestamp);
}
#pragma warning restore CA1707
