export type SentimentType = 'positive' | 'negative' | 'neutral' | 'mixed';
export type DebateMode = 'sequential' | 'parallel' | 'hybrid';
export type SessionStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface Persona {
  id: string;
  name: string;
  slug: string;
  category: string;
  description: string;
  avatar_url: string;
  speaking_style: string;
  is_premium: boolean;
}

export interface PersonaCategory {
  demographic: Persona[];
  professional: Persona[];
  personality: Persona[];
}

export interface DebateResponse {
  session_id: string;
  persona_id: string;
  persona_name: string;
  text: string;
  wave: number;
  sentiment?: SentimentType;
  confidence_score?: number;
  is_rebuttal: boolean;
  is_complete: boolean;
  timestamp: string;
}

export interface DebateSession {
  id: string;
  session_key: string;
  question: string;
  selected_persona_ids: string[];
  status: SessionStatus;
  created_at: string;
}

export interface SentimentBreakdown {
  positive: number;
  negative: number;
  neutral: number;
  mixed: number;
}

export interface DebateSummary {
  session_id: string;
  summary_text: string;
  sentiment_breakdown: SentimentBreakdown;
  key_insights: string[];
  consensus_points: string[];
  most_controversial_take: string;
  share_url: string;
}

export interface TrendingQuestion {
  question: string;
  category?: string;
  run_count: number;
  trending_score: number;
}

export interface WSMessage {
  type: 'debate_response' | 'debate_complete' | 'error';
  data?: any;
  message?: string;
}
