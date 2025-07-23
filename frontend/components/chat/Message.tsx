'use client';

import { Message as MessageType, MessageRole } from '@/types/chat';

interface MessageProps {
  message: MessageType;
}

export default function Message({ message }: MessageProps) {
  const formattedDate = new Date(message.sent_at + 'Z').toLocaleString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    month: 'short',
    day: 'numeric'
  });

  return (
    <div className={`flex ${message.role === MessageRole.USER ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-3xl px-4 py-2 rounded-lg ${
          message.role === MessageRole.USER
            ? 'bg-blue-600 text-white'
            : 'bg-gray-700 text-gray-100'
        }`}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>
        <div className={`text-xs mt-1 ${message.role === MessageRole.USER ? 'text-blue-200' : 'text-gray-400'}`}>
          {formattedDate}
        </div>
      </div>
    </div>
  );
}