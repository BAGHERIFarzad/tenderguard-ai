import axios from "axios";
import type {
  HumanDecisionRequest,
  ReviewCase,
  StartReviewRequest,
} from "../types/review";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5196/api";

export const startReview = async (
  request: StartReviewRequest
): Promise<ReviewCase> => {
  const response = await axios.post<ReviewCase>(
    `${API_BASE_URL}/Reviews/start`,
    request
  );

  return response.data;
};

export const submitHumanDecision = async (
  reviewId: string,
  request: HumanDecisionRequest
): Promise<ReviewCase> => {
  const response = await axios.post<ReviewCase>(
    `${API_BASE_URL}/Reviews/${reviewId}/human-decision`,
    request
  );

  return response.data;
};
