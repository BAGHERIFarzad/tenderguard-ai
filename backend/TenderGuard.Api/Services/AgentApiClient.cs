using System.Text.Json;
using TenderGuard.Api.Models;

namespace TenderGuard.Api.Services;

public class AgentApiClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<AgentApiClient> _logger;

    public AgentApiClient(HttpClient httpClient, ILogger<AgentApiClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<AgentApiReviewResult?> RunAgentReviewAsync(StartReviewRequest request)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync("/agent-review", request);

            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning(
                    "Agent API returned non-success status code: {StatusCode}",
                    response.StatusCode
                );

                return null;
            }

            var jsonOptions = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            var result = await response.Content.ReadFromJsonAsync<AgentApiReviewResult>(jsonOptions);

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to call Python Agent API.");
            return null;
        }
    }
}