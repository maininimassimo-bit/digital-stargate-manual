using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Ai;

public sealed record AiRequestContext(CorrelationId CorrelationId, CausationId? CausationId, string Capability, string ModelReference);
public sealed record AiResultReference(Guid ResultId, string Capability, string Status, DateTimeOffset CreatedAt, CorrelationId CorrelationId);
