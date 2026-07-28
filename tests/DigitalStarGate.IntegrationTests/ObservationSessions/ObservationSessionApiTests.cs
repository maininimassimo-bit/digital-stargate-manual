using System.Net;
using System.Net.Http.Json;
using DigitalStarGate.Contracts.Commands;
using DigitalStarGate.Contracts.Common;
using DigitalStarGate.Contracts.Dto;
using Microsoft.AspNetCore.Mvc.Testing;

namespace DigitalStarGate.IntegrationTests.ObservationSessions;

public sealed class ObservationSessionApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient client;

    public ObservationSessionApiTests(WebApplicationFactory<Program> factory)
    {
        client = factory.CreateClient();
    }

    [Fact]
    public async Task CreateThenGet_ReturnsPersistedObservationSession()
    {
        var command = new CreateObservationSession(
            new TargetId(Guid.NewGuid()),
            new ObservatoryId(Guid.NewGuid()),
            new CorrelationId(Guid.NewGuid()));

        var createResponse = await client.PostAsJsonAsync(
            "/api/v1/observation-sessions",
            command);

        Assert.Equal(HttpStatusCode.Created, createResponse.StatusCode);
        var created = await createResponse.Content.ReadFromJsonAsync<ObservationSessionDto>();
        Assert.NotNull(created);

        var getResponse = await client.GetAsync($"/api/v1/observation-sessions/{created.Id.Value}");
        Assert.Equal(HttpStatusCode.OK, getResponse.StatusCode);

        var retrieved = await getResponse.Content.ReadFromJsonAsync<ObservationSessionDto>();
        Assert.Equal(created, retrieved);
    }

    [Fact]
    public async Task Health_ReturnsSuccess()
    {
        var response = await client.GetAsync("/health");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
