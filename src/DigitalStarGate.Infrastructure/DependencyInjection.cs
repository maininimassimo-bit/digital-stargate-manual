using DigitalStarGate.Application.ObservationSessions;
using DigitalStarGate.Infrastructure.Events;
using DigitalStarGate.Infrastructure.ObservationSessions;
using Microsoft.Extensions.DependencyInjection;

namespace DigitalStarGate.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services)
    {
        services.AddSingleton<IObservationSessionRepository, InMemoryObservationSessionRepository>();
        services.AddSingleton<InMemoryPlatformEventPublisher>();
        services.AddSingleton<IPlatformEventPublisher>(provider => provider.GetRequiredService<InMemoryPlatformEventPublisher>());
        return services;
    }
}
