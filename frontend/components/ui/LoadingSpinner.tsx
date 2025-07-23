'use client';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  centered?: boolean;
  className?: string;
}

export default function LoadingSpinner({ 
  size = 'medium', 
  centered = false,
  className = ''
}: LoadingSpinnerProps) {
  const sizeClasses = {
    small: 'w-2 h-2',
    medium: 'w-4 h-4',
    large: 'w-6 h-6'
  };

  const containerClasses = centered 
    ? 'flex items-center justify-center h-full'
    : 'flex items-center';

  return (
    <div className={`${containerClasses} ${className}`}>
      <div className={`flex items-center text-gray-400`}>
        <div className="flex items-center space-x-1">
          <div className={`${sizeClasses[size]} bg-gray-400 rounded-full animate-bounce`}></div>
          <div className={`${sizeClasses[size]} bg-gray-400 rounded-full animate-bounce`} style={{ animationDelay: '0.1s' }}></div>
          <div className={`${sizeClasses[size]} bg-gray-400 rounded-full animate-bounce`} style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
}