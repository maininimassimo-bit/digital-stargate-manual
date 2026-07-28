using DigitalStarGate.Application;
using DigitalStarGate.Application.ObservationSessions;
using DigitalStarGate.Contracts.Commands;
using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Contracts.Queries;
using DigitalStarGate.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddApplication();
builder.Services.AddInfrastructure();
builder.Services.AddHealthChecks();
builder.Services.AddProblemDetails();

var app = builder.Build();

app.MapPost(
    "/api/v1/observation-sessions",
    async (
        CreateObservationSession command,
        CreateObservationSessionHandler handler,
        CancellationToken cancellationToken) =>
    {
        try
        {
            var session = await handler.HandleAsync(command, cancellationToken);
            return Results.Created($"/api/v1/observation-sessions/{session.Id.Value}", session);
        }
        catch (ArgumentException exception)
        {
            return Results.Problem(
                title: "Richiesta non valida",
                detail: exception.Message,
                statusCode: StatusCodes.Status400BadRequest,
                extensions: new Dictionary<string, object?>
                {
                    ["errorCode"] = "observation-session.validation"
                });
        }
    });

app.MapGet(
    "/api/v1/observation-sessions/{id:guid}",
    async (
        Guid id,
        GetObservationSessionHandler handler,
        CancellationToken cancellationToken) =>
    {
        var session = await handler.HandleAsync(
            new GetObservationSession(new ObservationSessionId(id)),
            cancellationToken);

        return session is null ? Results.NotFound() : Results.Ok(session);
    });

app.MapHealthChecks("/health");

app.Run();

public partial class Program;
