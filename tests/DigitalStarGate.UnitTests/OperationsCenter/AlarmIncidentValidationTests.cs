#pragma warning disable CA1707

namespace DigitalStarGate.UnitTests.OperationsCenter;

public sealed class AlarmIncidentValidationTests
{
  private static readonly DateTimeOffset Now = new(2026, 7, 30, 21, 0, 0, TimeSpan.Zero);

  [Fact]
  public void C02_acknowledgement_does_not_close_alarm()
  {
    var alarm = AlarmRecord.Open("alm-001", safetyRelevant: false, Now);

    alarm.Acknowledge("operator", "accepted", Now.AddMinutes(1));

    Assert.Equal(AlarmState.Acknowledged, alarm.State);
    Assert.Null(alarm.ClosedAt);
  }

  [Fact]
  public void C02_safety_relevant_alarm_cannot_be_suppressed()
  {
    var alarm = AlarmRecord.Open("alm-002", safetyRelevant: true, Now);

    var result = alarm.TrySuppress("maintenance-window", Now.AddMinutes(15));

    Assert.False(result);
    Assert.Equal(AlarmState.Open, alarm.State);
    Assert.Contains(alarm.Timeline, entry => entry.Reason == "safety-suppression-denied");
  }

  [Fact]
  public void C02_temporary_suppression_expires_and_reopens_alarm()
  {
    var alarm = AlarmRecord.Open("alm-003", safetyRelevant: false, Now);

    Assert.True(alarm.TrySuppress("approved-maintenance", Now.AddMinutes(5)));
    alarm.EvaluateSuppression(Now.AddMinutes(6));

    Assert.Equal(AlarmState.Open, alarm.State);
    Assert.Contains(alarm.Timeline, entry => entry.Reason == "suppression-expired");
  }

  [Fact]
  public void C02_related_alarms_are_correlated_without_losing_original_records()
  {
    var engine = new CorrelationEngine();
    var first = AlarmRecord.Open("alm-004", safetyRelevant: false, Now, serviceId: "dsoc", ciId: "telemetry");
    var second = AlarmRecord.Open("alm-005", safetyRelevant: false, Now.AddSeconds(10), serviceId: "dsoc", ciId: "telemetry");

    var group = engine.Correlate(first, second);

    Assert.Equal(2, group.AlarmIds.Count);
    Assert.Contains("alm-004", group.AlarmIds);
    Assert.Contains("alm-005", group.AlarmIds);
  }

  [Fact]
  public void C02_sev1_alarm_escalates_to_major_incident_and_safety_authority()
  {
    var alarm = AlarmRecord.Open("alm-006", safetyRelevant: true, Now, severity: Severity.Sev1);
    var incident = IncidentRecord.FromAlarm("inc-001", alarm, Now.AddMinutes(1));

    incident.Triage();

    Assert.Equal(IncidentState.MajorIncident, incident.State);
    Assert.Contains("SafetyAuthority", incident.EscalationTargets);
    Assert.Contains("IncidentCommander", incident.EscalationTargets);
  }

  [Fact]
  public void C02_incident_cannot_close_without_recovery_validation()
  {
    var alarm = AlarmRecord.Open("alm-007", safetyRelevant: false, Now, severity: Severity.Sev2);
    var incident = IncidentRecord.FromAlarm("inc-002", alarm, Now.AddMinutes(1));

    incident.Triage();
    incident.Assign();
    incident.Contain();
    incident.Restore();
    incident.Monitor();
    incident.Resolve();

    Assert.False(incident.TryClose());
    incident.ValidateRecovery(serviceHealthy: true, safeStateVerified: true);
    Assert.True(incident.TryClose());
    Assert.Equal(IncidentState.Closed, incident.State);
  }

  [Fact]
  public void C02_closed_incident_requires_post_incident_review_for_completion()
  {
    var alarm = AlarmRecord.Open("alm-008", safetyRelevant: false, Now, severity: Severity.Sev2);
    var incident = IncidentRecord.FromAlarm("inc-003", alarm, Now.AddMinutes(1));

    incident.Triage();
    incident.Assign();
    incident.Contain();
    incident.Restore();
    incident.Monitor();
    incident.Resolve();
    incident.ValidateRecovery(serviceHealthy: true, safeStateVerified: true);
    Assert.True(incident.TryClose());

    Assert.False(incident.IsComplete);
    incident.CompletePostIncidentReview("pir-001");
    Assert.True(incident.IsComplete);
  }

  private sealed class AlarmRecord
  {
    private AlarmRecord(string id, bool safetyRelevant, DateTimeOffset openedAt, string serviceId, string ciId, Severity severity)
    {
      Id = id;
      SafetyRelevant = safetyRelevant;
      ServiceId = serviceId;
      CiId = ciId;
      Severity = severity;
      State = AlarmState.Open;
      Timeline.Add(new TimelineEntry(AlarmState.Open.ToString(), "opened", openedAt));
    }

    public string Id { get; }
    public bool SafetyRelevant { get; }
    public string ServiceId { get; }
    public string CiId { get; }
    public Severity Severity { get; }
    public AlarmState State { get; private set; }
    public DateTimeOffset? ClosedAt { get; private set; }
    public DateTimeOffset? SuppressedUntil { get; private set; }
    public List<TimelineEntry> Timeline { get; } = [];

    public static AlarmRecord Open(
      string id,
      bool safetyRelevant,
      DateTimeOffset openedAt,
      string serviceId = "operations",
      string ciId = "unknown",
      Severity severity = Severity.Sev3) =>
      new(id, safetyRelevant, openedAt, serviceId, ciId, severity);

    public void Acknowledge(string actor, string reason, DateTimeOffset at)
    {
      State = AlarmState.Acknowledged;
      Timeline.Add(new TimelineEntry(State.ToString(), reason + ":" + actor, at));
    }

    public bool TrySuppress(string reason, DateTimeOffset until)
    {
      if (SafetyRelevant)
      {
        Timeline.Add(new TimelineEntry(State.ToString(), "safety-suppression-denied", Now));
        return false;
      }

      State = AlarmState.Suppressed;
      SuppressedUntil = until;
      Timeline.Add(new TimelineEntry(State.ToString(), reason, Now));
      return true;
    }

    public void EvaluateSuppression(DateTimeOffset at)
    {
      if (State == AlarmState.Suppressed && SuppressedUntil <= at)
      {
        State = AlarmState.Open;
        Timeline.Add(new TimelineEntry(State.ToString(), "suppression-expired", at));
      }
    }
  }

  private sealed class CorrelationEngine
  {
    public CorrelationGroup Correlate(params AlarmRecord[] alarms)
    {
      var first = alarms[0];
      var related = alarms.Where(alarm => alarm.ServiceId == first.ServiceId && alarm.CiId == first.CiId).ToArray();
      return new CorrelationGroup("corr-001", related.Select(alarm => alarm.Id).ToArray());
    }
  }

  private sealed class IncidentRecord
  {
    private IncidentRecord(string id, AlarmRecord alarm, DateTimeOffset detectedAt)
    {
      Id = id;
      LinkedAlarmId = alarm.Id;
      Severity = alarm.Severity;
      SafetyRelevant = alarm.SafetyRelevant;
      State = IncidentState.Logged;
      Timeline.Add(new IncidentTimelineEntry(State.ToString(), "logged", detectedAt));
    }

    public string Id { get; }
    public string LinkedAlarmId { get; }
    public Severity Severity { get; }
    public bool SafetyRelevant { get; }
    public IncidentState State { get; private set; }
    public bool RecoveryValidated { get; private set; }
    public string? PostIncidentReviewReference { get; private set; }
    public HashSet<string> EscalationTargets { get; } = new(StringComparer.Ordinal);
    public List<IncidentTimelineEntry> Timeline { get; } = [];
    public bool IsComplete => State == IncidentState.Closed && PostIncidentReviewReference is not null;

    public static IncidentRecord FromAlarm(string id, AlarmRecord alarm, DateTimeOffset detectedAt) => new(id, alarm, detectedAt);

    public void Triage()
    {
      if (Severity == Severity.Sev1 || SafetyRelevant)
      {
        State = IncidentState.MajorIncident;
        EscalationTargets.Add("SafetyAuthority");
        EscalationTargets.Add("IncidentCommander");
      }
      else
      {
        State = IncidentState.Triaged;
      }
    }

    public void Assign() => State = IncidentState.Assigned;
    public void Contain() => State = IncidentState.Containment;
    public void Restore() => State = IncidentState.Restoration;
    public void Monitor() => State = IncidentState.Monitoring;
    public void Resolve() => State = IncidentState.Resolved;

    public void ValidateRecovery(bool serviceHealthy, bool safeStateVerified) =>
      RecoveryValidated = serviceHealthy && safeStateVerified;

    public bool TryClose()
    {
      if (State != IncidentState.Resolved || !RecoveryValidated)
      {
        return false;
      }

      State = IncidentState.Closed;
      return true;
    }

    public void CompletePostIncidentReview(string reference) => PostIncidentReviewReference = reference;
  }

  private enum AlarmState { Open, Acknowledged, Suppressed, Escalated, Investigating, Contained, Recovery, Resolved, Closed }
  private enum IncidentState { Logged, Triaged, Assigned, Containment, Restoration, Monitoring, Resolved, Closed, MajorIncident }
  private enum Severity { Sev1, Sev2, Sev3, Sev4 }
  private sealed record TimelineEntry(string State, string Reason, DateTimeOffset Timestamp);
  private sealed record IncidentTimelineEntry(string State, string Reason, DateTimeOffset Timestamp);
  private sealed record CorrelationGroup(string CorrelationId, IReadOnlyCollection<string> AlarmIds);
}

#pragma warning restore CA1707
