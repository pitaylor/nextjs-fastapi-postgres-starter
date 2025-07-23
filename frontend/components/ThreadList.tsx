'use client';

import { Thread } from '@/types/chat';
import LoadingSpinner from './LoadingSpinner';

interface ThreadListProps {
  threads: Thread[];
  selectedThreadId: number | null;
  onSelectThread: (threadId: number) => void;
  onNewChat: () => void;
  isLoading: boolean;
}

export default function ThreadList({ threads, selectedThreadId, onSelectThread, onNewChat, isLoading }: ThreadListProps) {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 flex flex-col h-screen">
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={onNewChat}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          + New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        <div className="p-2">
          {isLoading ? (
            <LoadingSpinner className="py-8" centered />
          ) : (
            threads.map((thread) => (
              <button
                key={thread.id}
                onClick={() => onSelectThread(thread.id)}
                className={`w-full text-left p-3 rounded-lg mb-1 transition-colors truncate ${
                  selectedThreadId === thread.id
                    ? 'bg-gray-800'
                    : 'hover:bg-gray-800 text-gray-300'
                }`}
              >
                <div className="font-medium truncate">{thread.name}</div>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
}