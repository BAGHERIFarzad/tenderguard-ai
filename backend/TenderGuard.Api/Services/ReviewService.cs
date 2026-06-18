using System.Security.Cryptography;
using System.Text;
using TenderGuard.Api.Models;

namespace TenderGuard.Api.Services;

public class ReviewService
{
    private static readonly List<ReviewCase> _reviews = new();

    private readonly AgentApiClient _agentApiClient;

    public ReviewService(AgentApiClient agentApiClient)
    {
        _agentApiClient = agentApiClient;
    }

    public async Task<ReviewCase> StartReviewAsync(StartReviewRequest request)
    {
        var agentResult = await _agentApiClient.RunAgentReviewAsync(request);

        if (agentResult != null)
        {
            var reviewFromAgents = BuildReviewFromAgentApi(request, agentResult);
            _reviews.Add(reviewFromAgents);
            return reviewFromAgents;
        }

        var fallbackReview = StartFallbackReview(request);
        _reviews.Add(fallbackReview);
        return fallbackReview;
    }

    public List<ReviewCase> GetAllReviews()
    {
        return _reviews.OrderByDescending(r => r.CreatedAtUtc).ToList();
    }

    public ReviewCase? GetReview(Guid id)
    {
        return _reviews.FirstOrDefault(r => r.Id == id);
    }

    public ReviewCase? AddHumanDecision(Guid id, HumanDecisionRequest request)
    {
        var review = GetReview(id);

        if (review == null)
        {
            return null;
        }

        review.HumanDecision = request.Decision;
        review.Status = "Completed";

        review.Timeline.Add(new AgentMessage
        {
            FromAgent = "Human Manager",
            ToAgent = "@OrchestratorAgent",
            Message = $"Decision: {request.Decision}. Comment: {request.Comment}",
            MessageType = "Human Decision"
        });

        return review;
    }

    private static ReviewCase BuildReviewFromAgentApi(
        StartReviewRequest request,
        AgentApiReviewResult agentResult
    )
    {
        var review = new ReviewCase
        {
            ProjectName = agentResult.ProjectName,
            SupplierName = agentResult.SupplierName,
            ContractText = agentResult.ContractText,
            Status = "Human Approval Required",
            RiskScore = agentResult.RiskScore,
            RiskLevel = agentResult.RiskLevel,
            IntegrationMode = string.IsNullOrWhiteSpace(agentResult.IntegrationMode)
                ? "Python Agent API"
                : agentResult.IntegrationMode,
            AiProviderStatus = new ReviewAiProviderStatus
            {
                Featherless = agentResult.AiProviderStatus?.Featherless ?? "fallback-ready",
                AimlApi = agentResult.AiProviderStatus?.AimlApi ?? "fallback-ready"
            },
            FinalRecommendation = agentResult.FinalRecommendation,
            ExecutiveSummary = agentResult.ExecutiveSummary,
            HumanDecision = "Pending"
        };

        review.AuditHash = GenerateAuditHash(review);

        review.Timeline = agentResult.Timeline.Select(message => new AgentMessage
        {
            TimestampUtc = message.TimestampUtc,
            FromAgent = message.FromAgent,
            ToAgent = message.ToAgent,
            Message = message.Message,
            MessageType = message.MessageType
        }).ToList();

        review.Findings = agentResult.Findings.Select(finding => new AgentFinding
        {
            AgentName = finding.AgentName,
            Category = finding.Category,
            Severity = finding.Severity,
            Finding = finding.Finding,
            Recommendation = finding.Recommendation
        }).ToList();

        review.Votes = agentResult.Votes.Select(vote => new AgentVote
        {
            AgentName = vote.AgentName,
            Vote = vote.Vote,
            Confidence = vote.Confidence,
            Reason = vote.Reason
        }).ToList();

        review.Timeline.Add(new AgentMessage
        {
            FromAgent = "TenderGuard .NET Backend",
            ToAgent = "@HumanManager",
            Message = $"Python multi-agent review received via {review.IntegrationMode}, normalized, assigned audit hash, and prepared for human approval.",
            MessageType = "Backend Coordination"
        });

        return review;
    }

    private static ReviewCase StartFallbackReview(StartReviewRequest request)
    {
        var text = request.ContractText.ToLowerInvariant();

        var review = new ReviewCase
        {
            ProjectName = request.ProjectName,
            SupplierName = request.SupplierName,
            ContractText = request.ContractText,
            Status = "Human Approval Required",
            IntegrationMode = "Local C# Fallback"
        };

        review.AuditHash = GenerateAuditHash(review);

        AddOrchestratorStart(review);

        var score = 20;

        if (text.Contains("unlimited liability") || text.Contains("liability is unlimited"))
        {
            score += 22;

            review.Timeline.Add(new AgentMessage
            {
                FromAgent = "Legal Agent",
                ToAgent = "@FinanceAgent",
                Message = "Unlimited liability exposure found. Please evaluate financial impact.",
                MessageType = "Agent Handoff"
            });

            review.Findings.Add(new AgentFinding
            {
                AgentName = "Legal Agent",
                Category = "Contract Liability",
                Severity = "High",
                Finding = "The contract includes unlimited liability language without a clear liability cap.",
                Recommendation = "Add a liability cap equal to 12 months of service fees."
            });
        }

        if (text.Contains("no data processing agreement") || text.Contains("no dpa"))
        {
            score += 28;

            review.Timeline.Add(new AgentMessage
            {
                FromAgent = "Compliance Agent",
                ToAgent = "@OrchestratorAgent",
                Message = "GDPR risk detected. Data Processing Agreement is missing. Human approval required.",
                MessageType = "Escalation"
            });

            review.Findings.Add(new AgentFinding
            {
                AgentName = "Compliance Agent",
                Category = "GDPR / Data Protection",
                Severity = "Critical",
                Finding = "The supplier may process personal data, but no Data Processing Agreement is attached.",
                Recommendation = "Block final approval until a DPA is added."
            });
        }

        if (text.Contains("payment is due within 15 days") || text.Contains("15 days"))
        {
            score += 12;

            review.Timeline.Add(new AgentMessage
            {
                FromAgent = "Finance Agent",
                ToAgent = "@LegalAgent",
                Message = "Payment terms are aggressive. Please verify whether penalties and liability terms increase financial exposure.",
                MessageType = "Risk Review"
            });

            review.Findings.Add(new AgentFinding
            {
                AgentName = "Finance Agent",
                Category = "Payment Terms",
                Severity = "Medium",
                Finding = "The payment deadline is short and may create cash-flow pressure.",
                Recommendation = "Negotiate payment due within 30 days instead of 15 days."
            });
        }

        if (text.Contains("sla penalties are not clearly defined") || text.Contains("sla"))
        {
            score += 14;

            review.Timeline.Add(new AgentMessage
            {
                FromAgent = "Operations Agent",
                ToAgent = "@OrchestratorAgent",
                Message = "Delivery is feasible, but SLA penalties and operational guarantees must be clarified.",
                MessageType = "Operational Review"
            });

            review.Findings.Add(new AgentFinding
            {
                AgentName = "Operations Agent",
                Category = "Delivery / SLA",
                Severity = "Medium",
                Finding = "SLA penalties are vague and may create ambiguity during service incidents.",
                Recommendation = "Clarify SLA metrics, uptime obligations, response times, and penalty conditions."
            });
        }

        if (!review.Findings.Any())
        {
            score = 35;

            review.Findings.Add(new AgentFinding
            {
                AgentName = "Orchestrator Agent",
                Category = "General Review",
                Severity = "Low",
                Finding = "No major risk keywords were detected in the submitted text.",
                Recommendation = "Proceed with normal human review."
            });
        }

        review.RiskScore = Math.Min(score, 100);
        review.RiskLevel = GetRiskLevel(review.RiskScore);
        review.FinalRecommendation = BuildFinalRecommendation(review);
        review.Votes = BuildAgentVotes(review);

        review.Timeline.Add(new AgentMessage
        {
            FromAgent = "Orchestrator Agent",
            ToAgent = "@AllAgents",
            Message = "All agent reviews completed. Final decision packet is ready for human approval.",
            MessageType = "Coordination"
        });

        review.Timeline.Add(new AgentMessage
        {
            FromAgent = "TenderGuard .NET Backend",
            ToAgent = "@HumanManager",
            Message = "Python Agent API was unavailable, so fallback C# review logic was used.",
            MessageType = "Fallback Mode"
        });

        return review;
    }

    private static void AddOrchestratorStart(ReviewCase review)
    {
        review.Timeline.Add(new AgentMessage
        {
            FromAgent = "Orchestrator Agent",
            ToAgent = "@LegalAgent @FinanceAgent @ComplianceAgent @OperationsAgent",
            Message = "New supplier review started. Please analyze legal, financial, compliance, and operational risks.",
            MessageType = "Task Assignment"
        });
    }

    private static string GetRiskLevel(int score)
    {
        if (score >= 80) return "High";
        if (score >= 55) return "Medium";
        return "Low";
    }

    private static string BuildFinalRecommendation(ReviewCase review)
    {
        var hasCritical = review.Findings.Any(f =>
            f.Severity.Equals("Critical", StringComparison.OrdinalIgnoreCase)
        );

        var hasHigh = review.Findings.Any(f =>
            f.Severity.Equals("High", StringComparison.OrdinalIgnoreCase)
        );

        if (hasCritical)
        {
            return "Do not approve as-is. Human approval is required after critical issues are corrected, especially compliance and data protection requirements.";
        }

        if (hasHigh)
        {
            return "Approve only with conditions. High-risk contract terms must be amended before signature.";
        }

        if (review.RiskScore >= 55)
        {
            return "Proceed with caution. Medium-risk items should be clarified before final approval.";
        }

        return "Low-risk review. The contract can proceed to normal approval.";
    }

    private static List<AgentVote> BuildAgentVotes(ReviewCase review)
    {
        var votes = new List<AgentVote>();

        var legalRisk = review.Findings.Any(f => f.AgentName.Contains("Legal"));
        var financeRisk = review.Findings.Any(f => f.AgentName.Contains("Finance"));
        var complianceCritical = review.Findings.Any(f =>
            f.AgentName.Contains("Compliance") &&
            f.Severity.Equals("Critical", StringComparison.OrdinalIgnoreCase)
        );
        var operationsRisk = review.Findings.Any(f => f.AgentName.Contains("Operations"));

        votes.Add(new AgentVote
        {
            AgentName = "Legal Agent",
            Vote = legalRisk ? "Approve with conditions" : "Approve",
            Confidence = legalRisk ? 84 : 76,
            Reason = legalRisk
                ? "Legal risks can be reduced with contract amendments."
                : "No major legal blockers detected."
        });

        votes.Add(new AgentVote
        {
            AgentName = "Finance Agent",
            Vote = financeRisk ? "Approve with conditions" : "Approve",
            Confidence = financeRisk ? 78 : 74,
            Reason = financeRisk
                ? "Financial exposure should be reduced before signature."
                : "No major finance blocker detected."
        });

        votes.Add(new AgentVote
        {
            AgentName = "Compliance Agent",
            Vote = complianceCritical ? "Reject until fixed" : "Approve",
            Confidence = complianceCritical ? 93 : 80,
            Reason = complianceCritical
                ? "Missing DPA creates a serious compliance issue."
                : "No critical compliance blocker detected."
        });

        votes.Add(new AgentVote
        {
            AgentName = "Operations Agent",
            Vote = operationsRisk ? "Approve with conditions" : "Approve",
            Confidence = operationsRisk ? 88 : 77,
            Reason = operationsRisk
                ? "Operational conditions must be clarified."
                : "Delivery appears feasible."
        });

        return votes;
    }

    private static string GenerateAuditHash(ReviewCase review)
    {
        var raw = $"{review.Id}-{review.ProjectName}-{review.SupplierName}-{review.CreatedAtUtc:O}";
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(raw));
        var hash = Convert.ToHexString(bytes)[..10];

        return $"TG-{DateTime.UtcNow:yyyyMMdd}-{hash}";
    }
}