'use client';

import { useRef, useEffect } from 'react';
import { Message as MessageType } from '@/types/chat';
import Message from './Message';
import InputArea from './InputArea';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

interface ChatAreaProps {
  messages: MessageType[];
  selectedThreadId: number | null;
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

export default function ChatArea({ messages, selectedThreadId, onSendMessage, isLoading }: ChatAreaProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 flex flex-col h-screen bg-gray-800">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && selectedThreadId === null ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <h2 className="text-2xl font-semibold mb-2 text-white">Welcome to ChatBot</h2>
              <p>Start a conversation by typing a message below.</p>
            </div>
          </div>
        ) : messages.length === 0 && selectedThreadId !== null && isLoading ? (
          <LoadingSpinner text="Loading messages..." centered />
        ) : (
          messages.map((message) => (
            <Message key={message.id} message={message} />
          ))
        )}
        {isLoading && messages.length > 0 && (
          <div className="flex justify-start">
            <div className="max-w-3xl px-4 py-2 rounded-lg bg-gray-700 text-gray-100">
              <LoadingSpinner size="small" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <InputArea onSendMessage={onSendMessage} isLoading={isLoading} />
    </div>
  );
}