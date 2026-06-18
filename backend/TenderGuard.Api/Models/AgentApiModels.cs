using System.Text.Json.Serialization;

namespace TenderGuard.Api.Models;

public class AgentApiReviewResult
{
    public string ProjectName { get; set; } = string.Empty;
    public string SupplierName { get; set; } = string.Empty;
    public string ContractText { get; set; } = string.Empty;
    public int RiskScore { get; set; }
    public string RiskLevel { get; set; } = string.Empty;
    public string IntegrationMode { get; set; } = string.Empty;
    public string RoomMode { get; set; } = string.Empty;
    public List<AgentApiMessage> Timeline { get; set; } = new();
    public List<AgentApiFinding> Findings { get; set; } = new();
    public List<AgentApiVote> Votes { get; set; } = new();
    public string FinalRecommendation { get; set; } = string.Empty;
    public string ExecutiveSummary { get; set; } = string.Empty;
    public AiProviderStatus AiProviderStatus { get; set; } = new();
}

public class AgentApiMessage
{
    [JsonPropertyName("from_agent")]
    public string FromAgent { get; set; } = string.Empty;

    [JsonPropertyName("to_agent")]
    public string ToAgent { get; set; } = string.Empty;

    public string Message { get; set; } = string.Empty;

    [JsonPropertyName("message_type")]
    public string MessageType { get; set; } = string.Empty;

    [JsonPropertyName("timestamp_utc")]
    public DateTime TimestampUtc { get; set; }
}

public class AgentApiFinding
{
    [JsonPropertyName("agent_name")]
    public string AgentName { get; set; } = string.Empty;

    public string Category { get; set; } = string.Empty;
    public string Severity { get; set; } = string.Empty;
    public string Finding { get; set; } = string.Empty;
    public string Recommendation { get; set; } = string.Empty;
}

public class AgentApiVote
{
    [JsonPropertyName("agent_name")]
    public string AgentName { get; set; } = string.Empty;

    public string Vote { get; set; } = string.Empty;
    public int Confidence { get; set; }
    public string Reason { get; set; } = string.Empty;
}

public class AiProviderStatus
{
    public string Featherless { get; set; } = string.Empty;
    public string AimlApi { get; set; } = string.Empty;
}