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
    public async Task CreateThenGetReturnsPersistedObservationSession()
    {
        var token = TestContext.Current.CancellationToken;

        var command = new CreateObservationSession(
            new TargetId(Guid.NewGuid()),
            new ObservatoryId(Guid.NewGuid()),
            new CorrelationId(Guid.NewGuid()));

        var createResponse = await client.PostAsJsonAsync(
            "/api/v1/observation-sessions",
            command,
            token);

        Assert.Equal(HttpStatusCode.Created, createResponse.StatusCode);

        var created = await createResponse.Content.ReadFromJsonAsync<ObservationSessionDto>(token);
        Assert.NotNull(created);

        var getResponse = await client.GetAsync(
            $"/api/v1/observation-sessions/{created!.Id.Value}",
            token);

        Assert.Equal(HttpStatusCode.OK, getResponse.StatusCode);

        var retrieved = await getResponse.Content.ReadFromJsonAsync<ObservationSessionDto>(token);

        Assert.Equal(created, retrieved);
    }

    [Fact]
    public async Task HealthReturnsSuccess()
    {
        var response = await client.GetAsync(
            "/health",
            TestContext.Current.CancellationToken);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}