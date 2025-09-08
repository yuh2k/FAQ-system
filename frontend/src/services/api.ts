import axios from 'axios';
import { ChatRequest, ChatResponse, Ticket, KnowledgeBase, ChatHistory } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const sendMessage = async (chatRequest: ChatRequest): Promise<ChatResponse> => {
  const response = await api.post('/chat', chatRequest);
  return response.data;
};

export const getChatHistory = async (sessionId: string): Promise<ChatHistory> => {
  const response = await api.get(`/chat/history/${sessionId}`);
  return response.data;
};

// Tickets API
export const getTickets = async (): Promise<Ticket[]> => {
  const response = await api.get('/tickets');
  return response.data;
};

export const getTicket = async (ticketId: number): Promise<Ticket> => {
  const response = await api.get(`/tickets/${ticketId}`);
  return response.data;
};

export const updateTicketStatus = async (
  ticketId: number, 
  status: 'open' | 'in_progress' | 'closed'
): Promise<{ message: string }> => {
  const response = await api.put(`/tickets/${ticketId}/status?status=${status}`);
  return response.data;
};

// Knowledge Base API
export const getKnowledgeBase = async (): Promise<KnowledgeBase> => {
  const response = await api.get('/knowledge-base');
  return response.data;
};

// Config API
export const getAvailableKnowledgeBases = async (): Promise<{ available_kbs: string[] }> => {
  const response = await api.get('/config/knowledge-bases');
  return response.data;
};

export const switchKnowledgeBase = async (kbName: string): Promise<{ message: string }> => {
  const response = await api.post(`/config/switch-kb/${kbName}`);
  return response.data;
};

export const reloadConfig = async (): Promise<{ message: string }> => {
  const response = await api.post('/config/reload');
  return response.data;
};

// Health check
export const healthCheck = async (): Promise<{ message: string; version: string }> => {
  const response = await api.get('/');
  return response.data;
};