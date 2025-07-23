import { Thread, Message, MessageRole } from '@/types/chat';

// Mock data
const mockThreads: Thread[] = [
  { id: 1, user_id: 1, name: "Python Help" },
  { id: 2, user_id: 1, name: "Web Development" },
  { id: 3, user_id: 1, name: "Data Science Questions" },
];

const mockMessages: Record<number, Message[]> = {
  1: [
    {
      id: 1,
      thread_id: 1,
      content: "Hello! Can you help me with Python?",
      role: MessageRole.USER,
      sent_at: "2024-01-20T10:00:00Z"
    },
    {
      id: 2,
      thread_id: 1,
      content: "Of course! I'd be happy to help you with Python. What specific topic would you like to learn about?",
      role: MessageRole.ASSISTANT,
      sent_at: "2024-01-20T10:00:30Z"
    },
    {
      id: 3,
      thread_id: 1,
      content: "I'm trying to understand list comprehensions.",
      role: MessageRole.USER,
      sent_at: "2024-01-20T10:01:00Z"
    },
    {
      id: 4,
      thread_id: 1,
      content: "List comprehensions are a concise way to create lists in Python. They follow this syntax: [expression for item in iterable if condition]. For example: squares = [x**2 for x in range(10)] creates a list of squares from 0 to 81.",
      role: MessageRole.ASSISTANT,
      sent_at: "2024-01-20T10:01:30Z"
    }
  ],
  2: [
    {
      id: 5,
      thread_id: 2,
      content: "What's the best way to learn React?",
      role: MessageRole.USER,
      sent_at: "2024-01-20T11:00:00Z"
    },
    {
      id: 6,
      thread_id: 2,
      content: "Great question! I'd recommend starting with the official React documentation and building small projects. Begin with understanding components, props, and state management.",
      role: MessageRole.ASSISTANT,
      sent_at: "2024-01-20T11:00:30Z"
    }
  ],
  3: []
};

// Mock API functions
export const getThreads = async (): Promise<Thread[]> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockThreads;
};

export const getMessages = async (threadId: number): Promise<Message[]> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockMessages[threadId] || [];
};

export const sendMessage = async (threadId: number | null, content: string): Promise<{ thread: Thread; message: Message }> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  let thread: Thread;
  
  if (threadId === null) {
    // Create new thread
    const newThreadId = Math.max(...mockThreads.map(t => t.id)) + 1;
    thread = {
      id: newThreadId,
      user_id: 1,
      name: content.slice(0, 30) + (content.length > 30 ? "..." : "")
    };
    mockThreads.push(thread);
    mockMessages[newThreadId] = [];
  } else {
    thread = mockThreads.find(t => t.id === threadId)!;
  }
  
  // Add user message
  const userMessage: Message = {
    id: Date.now(),
    thread_id: thread.id,
    content,
    role: MessageRole.USER,
    sent_at: new Date().toISOString()
  };
  
  mockMessages[thread.id].push(userMessage);
  
  // Add mock assistant response
  const assistantMessage: Message = {
    id: Date.now() + 1,
    thread_id: thread.id,
    content: "I understand you're asking about: \"" + content + "\". This is a mock response from the assistant.",
    role: MessageRole.ASSISTANT,
    sent_at: new Date().toISOString()
  };
  
  mockMessages[thread.id].push(assistantMessage);
  
  return { thread, message: assistantMessage };
};