import { useState } from "react";
import {
  AlertTriangle,
  Bot,
  CheckCircle2,
  ClipboardCopy,
  FileText,
  Gavel,
  Landmark,
  Loader2,
  Network,
  ShieldCheck,
  UserCheck,
  XCircle,
} from "lucide-react";
import "./App.css";
import { startReview, submitHumanDecision } from "./api/reviewApi";
import type { ReviewCase } from "./types/review";

const sampleContract = `The supplier may process customer data. Liability is unlimited. Payment is due within 15 days. SLA penalties are not clearly defined. No Data Processing Agreement is attached. The supplier will provide cloud software services for a 24-month period. Termination rights require 90 days notice.`;

function getSeverityClass(severity: string) {
  const value = severity.toLowerCase();

  if (value.includes("critical")) return "severity critical";
  if (value.includes("high")) return "severity high";
  if (value.includes("medium")) return "severity medium";

  return "severity low";
}

function getAgentIcon(agentName: string) {
  const value = agentName.toLowerCase();

  if (value.includes("legal")) return <Gavel size={18} />;
  if (value.includes("finance")) return <Landmark size={18} />;
  if (value.includes("compliance")) return <ShieldCheck size={18} />;
  if (value.includes("operations")) return <Network size={18} />;
  if (value.includes("human")) return <UserCheck size={18} />;

  return <Bot size={18} />;
}

function App() {
  const [projectName, setProjectName] = useState("Cloud Software Supplier Review");
  const [supplierName, setSupplierName] = useState("Nexora Cloud Ltd");
  const [contractText, setContractText] = useState(sampleContract);
  const [review, setReview] = useState<ReviewCase | null>(null);
  const [visibleTimelineCount, setVisibleTimelineCount] = useState(0);
  const [isPlayingTimeline, setIsPlayingTimeline] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [decisionComment, setDecisionComment] = useState(
    "Approved only if the supplier adds a DPA, caps liability, and clarifies SLA penalties."
  );
  const [error, setError] = useState("");
  const [copySuccess, setCopySuccess] = useState(false);

  const playTimeline = (totalMessages: number) => {
    setVisibleTimelineCount(0);
    setIsPlayingTimeline(true);

    let index = 0;

    const interval = window.setInterval(() => {
      index += 1;
      setVisibleTimelineCount(index);

      if (index >= totalMessages) {
        window.clearInterval(interval);
        setIsPlayingTimeline(false);
      }
    }, 750);
  };

  const handleStartReview = async () => {
    try {
      setError("");
      setIsLoading(true);

      const result = await startReview({
        projectName,
        supplierName,
        contractText,
      });

      setReview(result);
      playTimeline(result.timeline.length);
    } catch (err) {
      console.error(err);
      setError("Unable to start the review. Please check that the .NET backend is running on http://localhost:5196.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDecision = async (decision: string) => {
    if (!review) return;

    try {
      setError("");
      setIsLoading(true);

      const updatedReview = await submitHumanDecision(review.id, {
        decision,
        comment: decisionComment,
      });

      setReview(updatedReview);
    } catch (err) {
      console.error(err);
      setError("Unable to submit the human decision. Please check the backend.");
    } finally {
      setIsLoading(false);
    }
  };

  const visibleTimeline = review
    ? review.timeline.slice(0, visibleTimelineCount)
    : [];

  const requiredConditions = review
    ? review.findings.map((finding) => finding.recommendation)
    : [];

  const buildAuditReportText = () => {
    if (!review) return "";

    const findingsText = review.findings
      .map(
        (finding) =>
          `- [${finding.severity}] ${finding.category} (${finding.agentName})\n  Finding: ${finding.finding}\n  Recommendation: ${finding.recommendation}`
      )
      .join("\n\n");

    const votesText = review.votes
      .map(
        (vote) =>
          `- ${vote.agentName}: ${vote.vote} (${vote.confidence}% confidence)\n  Reason: ${vote.reason}`
      )
      .join("\n\n");

    return `TenderGuard AI — Final Audit Decision Packet

  Review ID: ${review.id}
  Project: ${review.projectName}
  Supplier: ${review.supplierName}
  Status: ${review.status}
  Risk Score: ${review.riskScore}
  Risk Level: ${review.riskLevel}
  Audit Hash: ${review.auditHash || "Pending"}
  Integration Mode: ${review.integrationMode || "Local Review"}
  Featherless AI: ${review.aiProviderStatus?.featherless || "fallback-ready"}
  AI/ML API: ${review.aiProviderStatus?.aimlApi || "fallback-ready"}
  Human Decision: ${review.humanDecision}

  Final Recommendation:
  ${review.finalRecommendation}

  Required Conditions / Actions:
  ${requiredConditions.map((condition) => `- ${condition}`).join("\n")}

  Agent Findings:
  ${findingsText}

  Agent Votes:
  ${votesText}

  Generated by TenderGuard AI — Band-powered multi-agent procurement review room.`;
  };

  const handleCopyReport = async () => {
    if (!review) return;

    try {
      await navigator.clipboard.writeText(buildAuditReportText());
      setCopySuccess(true);

      window.setTimeout(() => {
        setCopySuccess(false);
      }, 1800);
    } catch (err) {
      console.error(err);
      setError("Unable to copy the audit report to clipboard.");
    }
  };

  return (
    <main className="tg-page">
      <section className="hero">
        <div className="hero-badge">
          <Bot size={16} />
          Band of Agents Hackathon
        </div>

        <h1>TenderGuard AI</h1>

        <p>
          A Band-powered multi-agent procurement and contract approval room
          where Legal, Finance, Compliance, and Operations agents collaborate,
          challenge each other, and prepare an audit-ready decision packet.
        </p>

        <div className="hero-stats">
          <div>
            <strong>5</strong>
            <span>Specialized Agents</span>
          </div>
          <div>
            <strong>Band</strong>
            <span>Collaboration Layer</span>
          </div>
          <div>
            <strong>Audit</strong>
            <span>Human Approval Ready</span>
          </div>
        </div>
      </section>

      <section className="layout">
        <aside className="panel input-panel">
          <div className="panel-title">
            <FileText size={20} />
            <div>
              <h2>Start Supplier Review</h2>
              <p>Paste a contract, proposal, or vendor document.</p>
            </div>
          </div>

          <label>
            Project name
            <input
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="Example: Cloud Software Supplier Review"
            />
          </label>

          <label>
            Supplier name
            <input
              value={supplierName}
              onChange={(e) => setSupplierName(e.target.value)}
              placeholder="Example: Nexora Cloud Ltd"
            />
          </label>

          <label>
            Contract / proposal text
            <textarea
              value={contractText}
              onChange={(e) => setContractText(e.target.value)}
              placeholder="Paste contract text here..."
            />
          </label>

          {error && <div className="error-box">{error}</div>}

          <button className="primary-btn" onClick={handleStartReview} disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="spin" size={18} />
                Agents are reviewing...
              </>
            ) : (
              <>
                <Bot size={18} />
                Start Multi-Agent Review
              </>
            )}
          </button>
        </aside>

        <section className="results">
          {!review ? (
            <div className="empty-state">
              <div className="orb">
                <Bot size={44} />
              </div>
              <h2>No review started yet</h2>
              <p>
                Start a review to see the agent collaboration timeline, risk
                findings, votes, and human approval workflow.
              </p>
            </div>
          ) : (
            <>
              <section className="summary-grid">
                <div className="summary-card wide">
                  <span>Status</span>
                  <strong>{review.status}</strong>
                  <p>{review.executiveSummary || review.finalRecommendation}</p>
                </div>

                <div className="summary-card risk">
                  <span>Risk Score</span>
                  <strong>{review.riskScore}</strong>
                  <p>{review.riskLevel} risk</p>
                </div>

                <div className="summary-card">
                  <span>Human Decision</span>
                  <strong>{review.humanDecision}</strong>
                  <p>Final manager approval state</p>
                </div>

                <div className="summary-card">
                  <span>Audit Hash</span>
                  <strong className="audit-code">{review.auditHash || "Pending"}</strong>
                  <p>Traceable review identifier</p>
                </div>

                <div className="summary-card">
                  <span>Integration Mode</span>
                  <strong className="integration-code">
                    {review.integrationMode || "Local Review"}
                  </strong>
                  <p>Current collaboration engine</p>
                </div>

                <div className="summary-card ai-provider-card">
                  <span>AI Providers</span>

                  <div className="provider-list">
                    <div>
                      <strong>Featherless</strong>
                      <em>{review.aiProviderStatus?.featherless || "fallback-ready"}</em>
                    </div>

                    <div>
                      <strong>AI/ML API</strong>
                      <em>{review.aiProviderStatus?.aimlApi || "fallback-ready"}</em>
                    </div>
                  </div>

                  <p>Partner model readiness</p>
                </div>
              </section>

              <section className="agent-room-grid">
                <article className="agent-room-card active">
                  <span>Orchestrator</span>
                  <strong>Coordinating</strong>
                  <p>Assigning tasks and preparing final decision packet.</p>
                </article>

                <article className="agent-room-card">
                  <span>Legal</span>
                  <strong>{visibleTimelineCount >= 2 ? "Completed" : "Waiting"}</strong>
                  <p>Reviewing liability, termination, and contractual exposure.</p>
                </article>

                <article className="agent-room-card">
                  <span>Finance</span>
                  <strong>{visibleTimelineCount >= 3 ? "Completed" : "Waiting"}</strong>
                  <p>Checking payment terms, penalties, and budget impact.</p>
                </article>

                <article className="agent-room-card">
                  <span>Compliance</span>
                  <strong>{visibleTimelineCount >= 4 ? "Escalated" : "Waiting"}</strong>
                  <p>Checking GDPR, DPA, policy, and high-stakes risks.</p>
                </article>

                <article className="agent-room-card">
                  <span>Operations</span>
                  <strong>{visibleTimelineCount >= 5 ? "Completed" : "Waiting"}</strong>
                  <p>Validating delivery feasibility, SLA, and execution risk.</p>
                </article>
              </section>

              <section className="panel">
                <div className="panel-title">
                  <Network size={20} />
                  <div>
                    <h2>Band Collaboration Timeline</h2>
                    <p>Visible agent-to-agent handoffs and shared context.</p>
                  </div>
                </div>

                <div className="timeline">
                  {visibleTimeline.map((item, index) => (
                    <div className="timeline-item" key={`${item.timestampUtc}-${index}`}>
                      <div className="agent-avatar">{getAgentIcon(item.fromAgent)}</div>

                      <div className="timeline-content">
                        <div className="timeline-header">
                          <strong>{item.fromAgent}</strong>
                          <span>{item.messageType}</span>
                        </div>

                        <p>{item.message}</p>

                        <small>
                          To: {item.toAgent} ·{" "}
                          {new Date(item.timestampUtc).toLocaleTimeString()}
                        </small>
                      </div>
                    </div>
                  ))}
                  {isPlayingTimeline && (
                    <div className="timeline-item">
                      <div className="agent-avatar typing-avatar">
                        <Loader2 className="spin" size={18} />
                      </div>

                      <div className="timeline-content typing-card">
                        <div className="timeline-header">
                          <strong>Band Room</strong>
                          <span>Live Coordination</span>
                        </div>

                        <p>Agents are exchanging context and preparing the next handoff...</p>

                        <small>Real-time multi-agent workflow simulation</small>
                      </div>
                    </div>
                  )}
                </div>
              </section>

              <section className="panel">
                <div className="panel-title">
                  <AlertTriangle size={20} />
                  <div>
                    <h2>Agent Findings</h2>
                    <p>Risk analysis from each specialized review agent.</p>
                  </div>
                </div>

                <div className="finding-grid">
                  {review.findings.map((finding, index) => (
                    <article className="finding-card" key={`${finding.agentName}-${index}`}>
                      <div className="finding-top">
                        <div>
                          <h3>{finding.category}</h3>
                          <p>{finding.agentName}</p>
                        </div>

                        <span className={getSeverityClass(finding.severity)}>
                          {finding.severity}
                        </span>
                      </div>

                      <p>{finding.finding}</p>

                      <div className="recommendation">
                        <strong>Recommendation</strong>
                        <span>{finding.recommendation}</span>
                      </div>
                    </article>
                  ))}
                </div>
              </section>

              <section className="panel">
                <div className="panel-title">
                  <ShieldCheck size={20} />
                  <div>
                    <h2>Agent Votes</h2>
                    <p>Each agent gives an independent decision and confidence.</p>
                  </div>
                </div>

                <div className="vote-grid">
                  {review.votes.map((vote, index) => (
                    <article className="vote-card" key={`${vote.agentName}-${index}`}>
                      <div className="vote-agent">
                        <div className="agent-avatar small">{getAgentIcon(vote.agentName)}</div>
                        <div>
                          <strong>{vote.agentName}</strong>
                          <span>{vote.vote}</span>
                        </div>
                      </div>

                      <div className="confidence-bar">
                        <div style={{ width: `${vote.confidence}%` }} />
                      </div>

                      <p>{vote.confidence}% confidence</p>
                      <small>{vote.reason}</small>
                    </article>
                  ))}
                </div>
              </section>

              <section className="panel decision-panel">
                <div className="panel-title">
                  <UserCheck size={20} />
                  <div>
                    <h2>Human Approval</h2>
                    <p>Enterprise workflows need a final responsible decision.</p>
                  </div>
                </div>

                <textarea
                  value={decisionComment}
                  onChange={(e) => setDecisionComment(e.target.value)}
                  placeholder="Decision comment..."
                />

                <div className="decision-actions">
                  <button onClick={() => handleDecision("Approved")} disabled={isLoading}>
                    <CheckCircle2 size={18} />
                    Approve
                  </button>

                  <button
                    onClick={() => handleDecision("Approved with conditions")}
                    disabled={isLoading}
                  >
                    <ShieldCheck size={18} />
                    Approve with conditions
                  </button>

                  <button
                    className="danger"
                    onClick={() => handleDecision("Rejected")}
                    disabled={isLoading}
                  >
                    <XCircle size={18} />
                    Reject
                  </button>
                </div>
              </section>
              <section className="panel audit-report-panel">
                <div className="panel-title audit-title-row">
                  <FileText size={20} />
                  <div>
                    <h2>Final Audit Decision Packet</h2>
                    <p>Enterprise-ready summary generated from multi-agent collaboration.</p>
                  </div>

                  <button className="copy-report-btn" onClick={handleCopyReport}>
                    <ClipboardCopy size={17} />
                    {copySuccess ? "Copied!" : "Copy Report"}
                  </button>
                </div>

                <div className="audit-report">
                  <div className="audit-report-header">
                    <div>
                      <span>Review Case</span>
                      <strong>{review.projectName}</strong>
                    </div>

                    <div>
                      <span>Supplier</span>
                      <strong>{review.supplierName}</strong>
                    </div>

                    <div>
                      <span>Audit Hash</span>
                      <strong className="audit-code">{review.auditHash || "Pending"}</strong>
                    </div>
                  </div>

                  <div className="audit-report-main">
                    <div className="audit-risk-block">
                      <span>Risk Score</span>
                      <strong>{review.riskScore}</strong>
                      <p>{review.riskLevel} risk level</p>
                    </div>

                    <div className="audit-recommendation-block">
                      <span>Final Recommendation</span>
                      <p>{review.finalRecommendation}</p>
                    </div>
                  </div>

                  <div className="audit-executive-summary">
                    <span>Executive Summary</span>
                    <p>{review.executiveSummary || review.finalRecommendation}</p>
                  </div>

                  <div className="audit-conditions">
                    <span>Required Conditions / Actions</span>

                    <ul>
                      {requiredConditions.map((condition, index) => (
                        <li key={`${condition}-${index}`}>{condition}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="audit-vote-summary">
                    <span>Agent Decision Summary</span>

                    <div className="audit-vote-list">
                      {review.votes.map((vote, index) => (
                        <div key={`${vote.agentName}-audit-${index}`}>
                          <strong>{vote.agentName}</strong>
                          <p>
                            {vote.vote} · {vote.confidence}% confidence
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="audit-human-final">
                    <span>Human Decision</span>
                    <strong>{review.humanDecision}</strong>
                  </div>
                </div>
              </section>
            </>
          )}
        </section>
      </section>
    </main>
  );
}

export default App;