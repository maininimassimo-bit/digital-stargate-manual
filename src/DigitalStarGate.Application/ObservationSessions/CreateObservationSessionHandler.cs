using DigitalStarGate.Contracts.Commands;
using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Contracts.Dto;
using DigitalStarGate.Contracts.Events;
using DigitalStarGate.Domain.ObservationSessions;
using Microsoft.Extensions.Logging;

namespace DigitalStarGate.Application.ObservationSessions;

public sealed class CreateObservationSessionHandler(
    IObservationSessionRepository repository,
    IPlatformEventPublisher eventPublisher,
    TimeProvider timeProvider,
    ILogger<CreateObservationSessionHandler> logger)
{
    public async Task<ObservationSessionDto> HandleAsync(
        CreateObservationSession command,
        CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(command);
        Validate(command);

        var createdAt = timeProvider.GetUtcNow();
        var session = ObservationSession.Create(
            new ObservationSessionId(Guid.NewGuid()),
            command.TargetId,
            command.ObservatoryId,
            Guid.NewGuid(),
            createdAt);

        await repository.AddAsync(session, cancellationToken);

        await eventPublisher.PublishAsync(
            new SessionCreated(
                Guid.NewGuid(),
                createdAt,
                command.CorrelationId,
                null,
                "1.0.0",
                session.Id,
                session.TargetId,
                session.ObservatoryId),
            cancellationToken);

        logger.LogInformation(
            "Observation Session {ObservationSessionId} creata per Target {TargetId} con CorrelationId {CorrelationId}",
            session.Id.Value,
            session.TargetId.Value,
            command.CorrelationId.Value);

        return ObservationSessionMapper.ToDto(session);
    }

    private static void Validate(CreateObservationSession command)
    {
        if (command.TargetId.Value == Guid.Empty)
        {
            throw new ArgumentException("Il Target è obbligatorio.", nameof(command));
        }

        if (command.ObservatoryId.Value == Guid.Empty)
        {
            throw new ArgumentException("L'osservatorio è obbligatorio.", nameof(command));
        }

        if (command.CorrelationId.Value == Guid.Empty)
        {
            throw new ArgumentException("Il CorrelationId è obbligatorio.", nameof(command));
        }
    }
}
