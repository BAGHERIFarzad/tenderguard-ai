namespace TenderGuard.Api.Models;

public class StartReviewRequest
{
    public string ProjectName { get; set; } = string.Empty;
    public string SupplierName { get; set; } = string.Empty;
    public string ContractText { get; set; } = string.Empty;
}

public class ReviewCase
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string ProjectName { get; set; } = string.Empty;
    public string SupplierName { get; set; } = string.Empty;
    public string ContractText { get; set; } = string.Empty;
    public string Status { get; set; } = "In Review";
    public int RiskScore { get; set; }
    public string RiskLevel { get; set; } = "Pending";
    public string AuditHash { get; set; } = string.Empty;
    public string IntegrationMode { get; set; } = "Local C# Fallback";
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;

    public List<AgentMessage> Timeline { get; set; } = new();
    public List<AgentFinding> Findings { get; set; } = new();
    public List<AgentVote> Votes { get; set; } = new();

    public string FinalRecommendation { get; set; } = string.Empty;
    public string ExecutiveSummary { get; set; } = string.Empty;
    public string HumanDecision { get; set; } = "Pending";
    public ReviewAiProviderStatus AiProviderStatus { get; set; } = new();
}

public class AgentMessage
{
    public DateTime TimestampUtc { get; set; } = DateTime.UtcNow;
    public string FromAgent { get; set; } = string.Empty;
    public string ToAgent { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string MessageType { get; set; } = "Coordination";
}

public class AgentFinding
{
    public string AgentName { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string Severity { get; set; } = string.Empty;
    public string Finding { get; set; } = string.Empty;
    public string Recommendation { get; set; } = string.Empty;
}

public class AgentVote
{
    public string AgentName { get; set; } = string.Empty;
    public string Vote { get; set; } = string.Empty;
    public int Confidence { get; set; }
    public string Reason { get; set; } = string.Empty;
}

public class HumanDecisionRequest
{
    public string Decision { get; set; } = string.Empty;
    public string Comment { get; set; } = string.Empty;
}

public class ReviewAiProviderStatus
{
    public string Featherless { get; set; } = "fallback-ready";
    public string AimlApi { get; set; } = "fallback-ready";
}