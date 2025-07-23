'use client';

import { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import ChatArea from './ChatArea';
import { Thread, Message } from '@/types/chat';
import { getThreads, getMessages, sendMessage } from '@/services/chatApi';

interface ChatContainerProps {
  selectedThreadId: number | null;
  onThreadSelect: (threadId: number) => void;
  onNewChat: () => void;
}

export default function ChatContainer({ selectedThreadId, onThreadSelect, onNewChat }: ChatContainerProps) {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [threadsLoading, setThreadsLoading] = useState(true);

  useEffect(() => {
    loadThreads();
  }, []);

  useEffect(() => {
    if (selectedThreadId) {
      const threadExists = threads.length > 0 && threads.some(thread => thread.id === selectedThreadId);
      if (threadExists) {
        loadMessages(selectedThreadId);
      } else if (threads.length > 0) {
        onNewChat();
      }
    } else {
      setMessages([]);
    }
  }, [selectedThreadId, threads, onNewChat]);

  const loadThreads = async () => {
    try {
      setThreadsLoading(true);
      const fetchedThreads = await getThreads();
      setThreads(fetchedThreads);
    } catch (error) {
      console.error('Failed to load threads:', error);
    } finally {
      setThreadsLoading(false);
    }
  };

  const loadMessages = async (threadId: number) => {
    try {
      setIsLoading(true);
      const fetchedMessages = await getMessages(threadId);
      setMessages(fetchedMessages);
    } catch (error) {
      console.error('Failed to load messages:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    setIsLoading(true);
    try {
      const result = await sendMessage(selectedThreadId, content);
      
      if (selectedThreadId === null) {
        await loadThreads();
        onThreadSelect(result.thread.id);
      } else {
        await loadMessages(selectedThreadId);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900">
      <ThreadList
        threads={threads}
        selectedThreadId={selectedThreadId}
        onSelectThread={onThreadSelect}
        onNewChat={onNewChat}
        isLoading={threadsLoading}
      />
      <ChatArea
        messages={messages}
        selectedThreadId={selectedThreadId}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}