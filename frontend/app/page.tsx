'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import ChatContainer from '@/components/chat/ChatContainer';

export default function Home() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const threadParam = searchParams.get('thread');
  const selectedThreadId = threadParam ? parseInt(threadParam) : null;

  const handleSelectThread = (threadId: number) => {
    router.push(`/?thread=${threadId}`);
  };

  const handleNewChat = () => {
    router.push('/');
  };

  return (
    <ChatContainer
      selectedThreadId={selectedThreadId}
      onThreadSelect={handleSelectThread}
      onNewChat={handleNewChat}
    />
  );
}
