'use client';

import { useState, useEffect } from 'react';
import ThreadList from '@/components/ThreadList';
import ChatArea from '@/components/ChatArea';
import { Thread, Message } from '@/types/chat';
import { getThreads, getMessages, sendMessage } from '@/services/chatApi';

export default function Home() {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [selectedThreadId, setSelectedThreadId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadThreads();
  }, []);

  useEffect(() => {
    if (selectedThreadId) {
      loadMessages(selectedThreadId);
    } else {
      setMessages([]);
    }
  }, [selectedThreadId]);

  const loadThreads = async () => {
    try {
      const fetchedThreads = await getThreads();
      setThreads(fetchedThreads);
    } catch (error) {
      console.error('Failed to load threads:', error);
    }
  };

  const loadMessages = async (threadId: number) => {
    try {
      const fetchedMessages = await getMessages(threadId);
      setMessages(fetchedMessages);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleSelectThread = (threadId: number) => {
    setSelectedThreadId(threadId);
  };

  const handleNewChat = () => {
    setSelectedThreadId(null);
    setMessages([]);
  };

  const handleSendMessage = async (content: string) => {
    setIsLoading(true);
    try {
      const result = await sendMessage(selectedThreadId, content);
      
      // If this was a new chat, update the threads list and select the new thread
      if (selectedThreadId === null) {
        await loadThreads();
        setSelectedThreadId(result.thread.id);
      } else {
        // Reload messages for the current thread
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
        onSelectThread={handleSelectThread}
        onNewChat={handleNewChat}
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
