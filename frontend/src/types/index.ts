// API Response Types
export interface ChatResponse {
  response: string;
  session_id: string;
  is_from_kb: boolean;
  ticket_created: boolean;
  ticket_id?: number;
  chat_ended: boolean;
}

export interface ChatRequest {
  message: string;
  user_contact: string;
  session_id?: string;
}

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  isFromKB?: boolean;
  ticketCreated?: boolean;
  ticketId?: number;
}

export interface Ticket {
  id: number;
  session_id: string;
  user_question: string;
  user_contact: string;
  status: 'open' | 'in_progress' | 'closed';
  ai_attempted_response: string;
  created_at: string;
}

export interface KnowledgeBase {
  qa_pairs: Array<{
    question: string;
    answer: string;
  }>;
}

export interface ChatHistory {
  session_id: string;
  messages: Array<{
    id: number;
    content: string;
    sender: 'user' | 'ai';
    timestamp: string;
  }>;
}