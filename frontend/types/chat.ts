export enum MessageRole {
  USER = "user",
  ASSISTANT = "assistant",
}

export interface Message {
  id: number;
  thread_id: number;
  content: string;
  role: MessageRole;
  sent_at: string;
}

export interface Thread {
  id: number;
  user_id: number;
  name: string;
}