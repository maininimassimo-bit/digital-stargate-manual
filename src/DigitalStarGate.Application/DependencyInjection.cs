using DigitalStarGate.Application.ObservationSessions;
using Microsoft.Extensions.DependencyInjection;

namespace DigitalStarGate.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddSingleton(TimeProvider.System);
        services.AddScoped<CreateObservationSessionHandler>();
        services.AddScoped<GetObservationSessionHandler>();
        return services;
    }
}
