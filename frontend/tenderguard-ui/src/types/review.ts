export interface StartReviewRequest {
  projectName: string;
  supplierName: string;
  contractText: string;
}

export interface AgentMessage {
  timestampUtc: string;
  fromAgent: string;
  toAgent: string;
  message: string;
  messageType: string;
}

export interface AgentFinding {
  agentName: string;
  category: string;
  severity: string;
  finding: string;
  recommendation: string;
}

export interface AgentVote {
  agentName: string;
  vote: string;
  confidence: number;
  reason: string;
}

export interface ReviewCase {
  id: string;
  projectName: string;
  supplierName: string;
  contractText: string;
  status: string;
  riskScore: number;
  riskLevel: string;
  auditHash: string;
  integrationMode: string;
  executiveSummary: string;
  aiProviderStatus: AiProviderStatus;
  createdAtUtc: string;
  timeline: AgentMessage[];
  findings: AgentFinding[];
  votes: AgentVote[];
  finalRecommendation: string;
  humanDecision: string;
}

export interface HumanDecisionRequest {
  decision: string;
  comment: string;
}

export interface AiProviderStatus {
  featherless: string;
  aimlApi: string;
}