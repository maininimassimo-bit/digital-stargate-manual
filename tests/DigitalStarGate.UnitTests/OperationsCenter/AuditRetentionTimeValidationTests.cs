#pragma warning disable CA1707

using System.Security.Cryptography;
using System.Text;

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class AuditRetentionTimeValidationTests
{
  [Fact]
  public void C07_audit_record_requires_actor_source_outcome_and_correlation()
  {
    var record = AuditRecord.Create(
      sequence: 1,
      actor: "operator-01",
      source: "operations-console",
      target: "session-001",
      outcome: "denied",
      correlationId: "corr-001",
      occurredAtUtc: new DateTimeOffset(2026, 7, 30, 20, 0, 0, TimeSpan.Zero));

    Assert.True(record.IsComplete);
  }

  [Fact]
  public void C07_missing_required_audit_field_is_rejected()
  {
    Assert.Throws<ArgumentException>(() => AuditRecord.Create(
      sequence: 1,
      actor: "",
      source: "operations-console",
      target: "session-001",
      outcome: "denied",
      correlationId: "corr-001",
      occurredAtUtc: new DateTimeOffset(2026, 7, 30, 20, 0, 0, TimeSpan.Zero)));
  }

  [Fact]
  public void C07_append_only_chain_detects_tampering()
  {
    var ledger = new AuditLedger();
    ledger.Append("operator-01", "console", "command-001", "requested", "corr-001", AtMinute(0));
    ledger.Append("approver-01", "authorization", "command-001", "denied", "corr-001", AtMinute(1));

    Assert.True(ledger.VerifyIntegrity());

    ledger.ReplaceForTest(1, ledger.Records[1] with { Outcome = "approved" });

    Assert.False(ledger.VerifyIntegrity());
  }

  [Fact]
  public void C07_non_monotonic_or_duplicate_time_is_rejected()
  {
    var ledger = new AuditLedger();
    ledger.Append("operator-01", "console", "command-001", "requested", "corr-001", AtMinute(2));

    Assert.Throws<InvalidOperationException>(() =>
      ledger.Append("operator-01", "console", "command-001", "retried", "corr-001", AtMinute(1)));

    Assert.Throws<InvalidOperationException>(() =>
      ledger.Append("operator-01", "console", "command-001", "retried", "corr-001", AtMinute(2)));
  }

  [Fact]
  public void C07_untrusted_clock_source_is_rejected()
  {
    var clock = new ClockEvidence("local-unsynchronized", trusted: false, maximumObservedSkew: TimeSpan.FromSeconds(4));

    Assert.False(TimeIntegrityPolicy.IsAccepted(clock));
  }

  [Fact]
  public void C07_excessive_clock_skew_is_rejected_without_operational_threshold_claim()
  {
    var candidatePolicy = new TimeIntegrityPolicy(TimeSpan.FromSeconds(2));
    var clock = new ClockEvidence("simulated-trusted-source", trusted: true, maximumObservedSkew: TimeSpan.FromSeconds(3));

    Assert.False(candidatePolicy.Accepts(clock));
  }

  [Fact]
  public void C07_retention_prevents_early_deletion_and_legal_hold_prevents_expiry_deletion()
  {
    var policy = new RetentionPolicy(TimeSpan.FromDays(30));
    var record = RetainedAuditRecord.Create("audit-001", AtMinute(0));

    Assert.False(policy.CanDelete(record, AtDay(10)));
    Assert.True(policy.CanDelete(record, AtDay(31)));

    record = record with { LegalHold = true };

    Assert.False(policy.CanDelete(record, AtDay(365)));
  }

  [Fact]
  public void C07_retention_decision_produces_evidence()
  {
    var policy = new RetentionPolicy(TimeSpan.FromDays(30));
    var record = RetainedAuditRecord.Create("audit-002", AtMinute(0));

    var decision = policy.EvaluateDeletion(record, AtDay(12));

    Assert.False(decision.Allowed);
    Assert.Equal("retention-period-active", decision.Reason);
    Assert.Equal("audit-002", decision.RecordId);
  }

  private static DateTimeOffset AtMinute(int minute) =>
    new(2026, 7, 30, 20, minute, 0, TimeSpan.Zero);

  private static DateTimeOffset AtDay(int day) =>
    new DateTimeOffset(2026, 7, 30, 20, 0, 0, TimeSpan.Zero).AddDays(day);

  private sealed class AuditLedger
  {
    private readonly List<AuditRecord> records = [];

    public IReadOnlyList<AuditRecord> Records => records;

    public void Append(
      string actor,
      string source,
      string target,
      string outcome,
      string correlationId,
      DateTimeOffset occurredAtUtc)
    {
      if (records.Count > 0 && occurredAtUtc <= records[^1].OccurredAtUtc)
      {
        throw new InvalidOperationException("Audit time must be strictly monotonic in this simulated ledger.");
      }

      var previousHash = records.Count == 0 ? "GENESIS" : records[^1].Hash;
      var record = AuditRecord.Create(
        records.Count + 1,
        actor,
        source,
        target,
        outcome,
        correlationId,
        occurredAtUtc,
        previousHash);
      records.Add(record);
    }

    public bool VerifyIntegrity()
    {
      var previousHash = "GENESIS";

      foreach (var record in records)
      {
        if (!string.Equals(record.PreviousHash, previousHash, StringComparison.Ordinal) ||
            !string.Equals(record.Hash, AuditRecord.ComputeHash(record with { Hash = string.Empty }), StringComparison.Ordinal))
        {
          return false;
        }

        previousHash = record.Hash;
      }

      return true;
    }

    public void ReplaceForTest(int index, AuditRecord record) => records[index] = record;
  }

  private sealed record AuditRecord(
    int Sequence,
    string Actor,
    string Source,
    string Target,
    string Outcome,
    string CorrelationId,
    DateTimeOffset OccurredAtUtc,
    string PreviousHash,
    string Hash)
  {
    public bool IsComplete =>
      Sequence > 0 &&
      !string.IsNullOrWhiteSpace(Actor) &&
      !string.IsNullOrWhiteSpace(Source) &&
      !string.IsNullOrWhiteSpace(Target) &&
      !string.IsNullOrWhiteSpace(Outcome) &&
      !string.IsNullOrWhiteSpace(CorrelationId) &&
      OccurredAtUtc.Offset == TimeSpan.Zero;

    public static AuditRecord Create(
      int sequence,
      string actor,
      string source,
      string target,
      string outcome,
      string correlationId,
      DateTimeOffset occurredAtUtc,
      string previousHash = "GENESIS")
    {
      if (sequence <= 0 ||
          string.IsNullOrWhiteSpace(actor) ||
          string.IsNullOrWhiteSpace(source) ||
          string.IsNullOrWhiteSpace(target) ||
          string.IsNullOrWhiteSpace(outcome) ||
          string.IsNullOrWhiteSpace(correlationId) ||
          occurredAtUtc.Offset != TimeSpan.Zero)
      {
        throw new ArgumentException("Audit record is incomplete or does not use UTC.");
      }

      var unsigned = new AuditRecord(sequence, actor, source, target, outcome, correlationId, occurredAtUtc, previousHash, string.Empty);
      return unsigned with { Hash = ComputeHash(unsigned) };
    }

    public static string ComputeHash(AuditRecord record)
    {
      var payload = string.Join('|',
        record.Sequence,
        record.Actor,
        record.Source,
        record.Target,
        record.Outcome,
        record.CorrelationId,
        record.OccurredAtUtc.ToString("O"),
        record.PreviousHash);
      return Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(payload)));
    }
  }

  private sealed record ClockEvidence(string Source, bool Trusted, TimeSpan MaximumObservedSkew);

  private sealed class TimeIntegrityPolicy
  {
    private readonly TimeSpan maximumAllowedSkew;

    public TimeIntegrityPolicy(TimeSpan maximumAllowedSkew)
    {
      this.maximumAllowedSkew = maximumAllowedSkew;
    }

    public bool Accepts(ClockEvidence evidence) =>
      evidence.Trusted && evidence.MaximumObservedSkew <= maximumAllowedSkew;

    public static bool IsAccepted(ClockEvidence evidence) => evidence.Trusted;
  }

  private sealed record RetainedAuditRecord(string RecordId, DateTimeOffset CreatedAtUtc, bool LegalHold)
  {
    public static RetainedAuditRecord Create(string recordId, DateTimeOffset createdAtUtc) =>
      new(recordId, createdAtUtc, LegalHold: false);
  }

  private sealed record RetentionDecision(string RecordId, bool Allowed, string Reason);

  private sealed class RetentionPolicy
  {
    private readonly TimeSpan retentionPeriod;

    public RetentionPolicy(TimeSpan retentionPeriod)
    {
      this.retentionPeriod = retentionPeriod;
    }

    public bool CanDelete(RetainedAuditRecord record, DateTimeOffset evaluatedAtUtc) =>
      EvaluateDeletion(record, evaluatedAtUtc).Allowed;

    public RetentionDecision EvaluateDeletion(RetainedAuditRecord record, DateTimeOffset evaluatedAtUtc)
    {
      if (record.LegalHold)
      {
        return new RetentionDecision(record.RecordId, Allowed: false, "legal-hold-active");
      }

      if (evaluatedAtUtc < record.CreatedAtUtc + retentionPeriod)
      {
        return new RetentionDecision(record.RecordId, Allowed: false, "retention-period-active");
      }

      return new RetentionDecision(record.RecordId, Allowed: true, "retention-satisfied");
    }
  }
}

#pragma warning restore CA1707
