using System.Collections.Concurrent;

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class AuthorizationSecurityValidationTests
{
    private static readonly DateTimeOffset Now = new(2026, 7, 30, 19, 30, 0, TimeSpan.Zero);

    [Fact]
    public void C01_authorized_C1_command_is_executed_once_and_audited()
    {
        var harness = Harness.Create(Now);
        var result = harness.Execute(Request("cmd-001", CommandClass.C1, "operator", "operator", TelemetryState.Fresh));

        Assert.True(result.Allowed);
        Assert.Equal(1, harness.Dispatcher.ExecutionCount("cmd-001"));
        Assert.Contains(harness.Audit.Entries, entry => entry.CommandId == "cmd-001" && entry.Outcome == "executed");
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
        Assert.Equal(0, harness.Dispatcher.ExecutionCount("cmd-004"));
    }

    [Fact]
    public void C01_duplicate_and_retry_do_not_execute_twice()
    {
        var harness = Harness.Create(Now);
        var request = Request("cmd-005", CommandClass.C2, "operator", "approver", TelemetryState.Fresh);

        var first = harness.Execute(request);
        var retry = harness.Execute(request);

        Assert.True(first.Allowed);
        Assert.True(retry.Allowed);
        Assert.True(retry.IdempotentReplay);
        Assert.Equal(1, harness.Dispatcher.ExecutionCount("cmd-005"));
    }

    [Fact]
    public void C01_privilege_revoked_before_execution_is_denied()
    {
        var harness = Harness.Create(Now);
        harness.Identity.Revoke("operator");

        var result = harness.Execute(Request("cmd-006", CommandClass.C2, "operator", "approver", TelemetryState.Fresh));

        Assert.False(result.Allowed);
        Assert.Equal("requester-not-authorized", result.Reason);
    }

    [Fact]
    public void C05_privileged_access_is_time_bound_and_out_of_scope_is_denied()
    {
        var controller = new BreakGlassController(Now);
        var grant = controller.Grant("maintainer", "maintenance", Now.AddMinutes(15), "approved-change");

        Assert.True(controller.IsAuthorized(grant.Token, "maintenance", Now.AddMinutes(5)));
        Assert.False(controller.IsAuthorized(grant.Token, "command-execution", Now.AddMinutes(5)));
        Assert.False(controller.IsAuthorized(grant.Token, "maintenance", Now.AddMinutes(16)));
    }

    [Fact]
    public void C05_break_glass_requires_reason_and_can_be_revoked()
    {
        var controller = new BreakGlassController(Now);
        Assert.Throws<ArgumentException>(() => controller.Grant("security-admin", "diagnostics", Now.AddMinutes(10), string.Empty));

        var grant = controller.Grant("security-admin", "diagnostics", Now.AddMinutes(10), "identity-provider-outage");
        controller.Revoke(grant.Token, "incident-contained");

        Assert.False(controller.IsAuthorized(grant.Token, "diagnostics", Now.AddMinutes(2)));
        Assert.Contains(controller.Audit, entry => entry.Action == "revoked" && entry.Token == grant.Token);
    }

    [Fact]
    public void C05_security_authority_cannot_declare_safe_state_or_gain_command_authority()
    {
        var harness = Harness.Create(Now);
        var result = harness.Execute(Request("cmd-007", CommandClass.C1, "security-admin", "approver", TelemetryState.Fresh));

        Assert.False(result.Allowed);
        Assert.Equal("requester-not-authorized", result.Reason);
        Assert.False(harness.Identity.CanDeclareSafeState("security-admin"));
    }

    [Fact]
    public void C05_auditor_is_read_only()
    {
        var harness = Harness.Create(Now);
        var result = harness.Execute(Request("cmd-008", CommandClass.C1, "auditor", "approver", TelemetryState.Fresh));

        Assert.False(result.Allowed);
        Assert.True(harness.Identity.CanReadAudit("auditor"));
    }

    private static CommandRequest Request(
        string id,
        CommandClass commandClass,
        string requester,
        string approver,
        TelemetryState telemetry) =>
        new(id, commandClass, requester, approver, telemetry, Now.AddMinutes(5), "policy-v1");

    private sealed class Harness
    {
        private Harness(DateTimeOffset now, bool safetyAllows)
        {
            Now = now;
            Identity = new IdentityStub();
            Identity.Assign("operator", Role.Operator);
            Identity.Assign("approver", Role.SeniorOperator);
            Identity.Assign("security-admin", Role.SecurityAuthority);
            Identity.Assign("auditor", Role.Auditor);
            SafetyAllows = safetyAllows;
        }

        public DateTimeOffset Now { get; }
        public IdentityStub Identity { get; }
        public FakeCommandDispatcher Dispatcher { get; } = new();
        public AppendOnlyAuditSink Audit { get; } = new();
        public IdempotencyStore Idempotency { get; } = new();
        private bool SafetyAllows { get; }

        public static Harness Create(DateTimeOffset now, bool safetyAllows = true) => new(now, safetyAllows);

        public Decision Execute(CommandRequest request)
        {
            Decision decision;

            if (!Identity.CanRequestCommand(request.Requester))
            {
                decision = Decision.Deny("requester-not-authorized");
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
                Dispatcher.Execute(request.CommandId);
                decision = Decision.Allow();
            }

            Audit.Append(new AuditEntry(
                request.CommandId,
                request.Requester,
                request.Approver,
                request.PolicyVersion,
                decision.Allowed ? "executed" : "denied",
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

        public void Execute(string commandId) => executions.AddOrUpdate(commandId, 1, (_, count) => count + 1);
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

        public IReadOnlyList<BreakGlassAudit> Audit => audit;

        public BreakGlassGrant Grant(string principal, string scope, DateTimeOffset expiresAt, string reason)
        {
            if (string.IsNullOrWhiteSpace(reason))
            {
                throw new ArgumentException("Break-glass reason is required.", nameof(reason));
            }

            if (expiresAt <= issuedAt)
            {
                throw new ArgumentOutOfRangeException(nameof(expiresAt));
            }

            var token = Guid.NewGuid().ToString("N");
            var grant = new BreakGlassGrant(token, principal, scope, issuedAt, expiresAt, false);
            grants[token] = grant;
            audit.Add(new BreakGlassAudit(token, "granted", issuedAt));
            return grant;
        }

        public bool IsAuthorized(string token, string scope, DateTimeOffset at) =>
            grants.TryGetValue(token, out var grant) &&
            !grant.Revoked &&
            grant.Scope == scope &&
            at >= grant.IssuedAt &&
            at < grant.ExpiresAt;

        public void Revoke(string token, string reason)
        {
            if (!grants.TryGetValue(token, out var grant))
            {
                return;
            }

            grants[token] = grant with { Revoked = true };
            audit.Add(new BreakGlassAudit(token, "revoked", issuedAt));
        }
    }

    private enum CommandClass { C1, C2, C3, C4 }
    public enum TelemetryState { Fresh, Stale, Unknown, Conflicting }
    private enum Role { Operator, SeniorOperator, SafetyAuthority, SecurityAuthority, Auditor }

    private sealed record CommandRequest(
        string CommandId,
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
        string Requester,
        string Approver,
        string PolicyVersion,
        string Outcome,
        string Reason,
        DateTimeOffset Timestamp);

    private sealed record BreakGlassGrant(
        string Token,
        string Principal,
        string Scope,
        DateTimeOffset IssuedAt,
        DateTimeOffset ExpiresAt,
        bool Revoked);

    private sealed record BreakGlassAudit(string Token, string Action, DateTimeOffset Timestamp);
}
