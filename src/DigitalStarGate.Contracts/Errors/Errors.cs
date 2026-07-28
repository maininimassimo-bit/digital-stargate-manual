namespace DigitalStarGate.Contracts.Errors;

public enum ErrorCategory
{
  Validation,
  Business,
  Infrastructure,
  Security
}

public sealed record ErrorCode(string Value);

public sealed record ValidationError(ErrorCode Code, string Field, string Message);

public sealed record BusinessError(ErrorCode Code, string Message);

public sealed record InfrastructureError(ErrorCode Code, string Message, bool IsTransient);

public sealed record SecurityError(ErrorCode Code, string Message);

public sealed record ProblemDetailsContract(
  string Type,
  string Title,
  int Status,
  string? Detail,
  string? Instance,
  ErrorCode ErrorCode,
  ErrorCategory Category,
  IReadOnlyList<ValidationError>? Errors,
  string? CorrelationId);
