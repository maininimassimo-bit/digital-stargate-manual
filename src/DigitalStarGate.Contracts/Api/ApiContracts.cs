using DigitalStarGate.Contracts.Common;

namespace DigitalStarGate.Contracts.Api;

public sealed record ApiVersion(int Major, int Minor);
public sealed record PageRequest(int Page, int PageSize);
public sealed record PageResult<T>(IReadOnlyList<T> Items, int Page, int PageSize, long TotalCount);
public sealed record RequestContext(CorrelationId CorrelationId, CausationId? CausationId, string? UserId, string ApiVersion);
