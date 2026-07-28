using DigitalStarGate.Contracts.Dto;
using DigitalStarGate.Contracts.Queries;

namespace DigitalStarGate.Application.ObservationSessions;

public sealed class GetObservationSessionHandler(IObservationSessionRepository repository)
{
    public async Task<ObservationSessionDto?> HandleAsync(
        GetObservationSession query,
        CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(query);

        if (query.SessionId.Value == Guid.Empty)
        {
            throw new ArgumentException("L'identificativo della sessione è obbligatorio.", nameof(query));
        }

        var session = await repository.GetAsync(query.SessionId, cancellationToken);
        return session is null ? null : ObservationSessionMapper.ToDto(session);
    }
}
