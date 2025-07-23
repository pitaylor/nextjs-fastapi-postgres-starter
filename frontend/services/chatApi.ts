import { Thread, Message } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const getThreads = async (): Promise<Thread[]> => {
  const response = await fetch(`${API_BASE_URL}/threads`);
  if (!response.ok) {
    throw new Error('Failed to fetch threads');
  }
  return response.json();
};

export const getMessages = async (threadId: number): Promise<Message[]> => {
  const response = await fetch(`${API_BASE_URL}/threads/${threadId}/messages`);
  if (!response.ok) {
    throw new Error('Failed to fetch messages');
  }
  return response.json();
};

export const sendMessage = async (threadId: number | null, content: string): Promise<{ thread: Thread; message: Message }> => {
  const body = JSON.stringify({ content });
  const url = threadId ? `${API_BASE_URL}/messages?thread_id=${threadId}` : `${API_BASE_URL}/messages`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body,
  });
  
  if (!response.ok) {
    throw new Error('Failed to send message');
  }
  
  return response.json();
};