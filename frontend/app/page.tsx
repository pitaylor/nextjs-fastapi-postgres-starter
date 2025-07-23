'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import ThreadList from '@/components/ThreadList';
import ChatArea from '@/components/ChatArea';
import { Thread, Message } from '@/types/chat';
import { getThreads, getMessages, sendMessage } from '@/services/chatApi';

export default function Home() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [threads, setThreads] = useState<Thread[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [threadsLoading, setThreadsLoading] = useState(true);
  
  // Get thread ID from URL
  const threadParam = searchParams.get('thread');
  const selectedThreadId = threadParam ? parseInt(threadParam) : null;

  useEffect(() => {
    loadThreads();
  }, []);

  useEffect(() => {
    if (selectedThreadId) {
      // Validate that the thread exists in our loaded threads
      const threadExists = threads.length > 0 && threads.some(thread => thread.id === selectedThreadId);
      if (threadExists) {
        loadMessages(selectedThreadId);
      } else if (threads.length > 0) {
        // Thread doesn't exist, redirect to home
        router.push('/');
      }
      // If threads haven't loaded yet, wait for them to load first
    } else {
      setMessages([]);
    }
  }, [selectedThreadId, threads, router]);

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

  const handleSelectThread = (threadId: number) => {
    router.push(`/?thread=${threadId}`);
  };

  const handleNewChat = () => {
    router.push('/');
    setMessages([]);
  };

  const handleSendMessage = async (content: string) => {
    setIsLoading(true);
    try {
      const result = await sendMessage(selectedThreadId, content);
      
      // If this was a new chat, update the threads list and navigate to new thread
      if (selectedThreadId === null) {
        await loadThreads();
        router.push(`/?thread=${result.thread.id}`);
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
