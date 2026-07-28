# Coding Standards

## General rules

- Prefer clear, explicit and maintainable implementations.
- Keep functions and modules focused on one responsibility.
- Validate external input and fail with actionable diagnostics.
- Use structured logging rather than unstructured console output.
- Keep environment-specific values outside source code.
- Preserve backward compatibility for published interfaces unless a versioned breaking change is approved.

## Automation code

Automation logic must be idempotent where practical, enforce timeouts, expose state transitions and avoid silent retries without limits.

## Error handling

Errors must include context, severity, correlation identifiers where available and a recommended operator action. Safety-related failures default to the safest achievable state.
