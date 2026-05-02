import React from 'react';

interface TikTokDisplayProps {
  data: {
    url: string;
    title: string;
  };
}

export default function TikTokDisplay({ data }: TikTokDisplayProps) {
  if (!data || !data.url) return null;

  // Extract username from URL
  const username = data.url.split('/@')[1]?.split('?')[0]?.split('/')[0];
  if (!username) return null;

  return (
    <div>
      <a 
        href={data.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block"
      >
        <div className="bg-white p-6 rounded-none border hover:shadow-md transition-all duration-200">
          <div className="flex items-center gap-4">
            
            {/* TikTok Icon */}
            <div className="p-3 bg-gray-50 rounded-full">
              <svg 
                className="w-6 h-6 text-black" 
                viewBox="0 0 24 24" 
                fill="currentColor"
              >
                <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.43v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
              </svg>
            </div>

            <div className="flex flex-col">
              <span className="text-sm text-gray-500">TikTok Profile</span>
              <span className="text-xl transition-colors">
                @{username}
              </span>
            </div>
          </div>
        </div>
      </a>
    </div>
  );
}