import React from 'react';

interface CrunchbaseDisplayProps {
  data: {
    url: string;
    title: string;
  };
}

export default function CrunchbaseDisplay({ data }: CrunchbaseDisplayProps) {
  if (!data || !data.url) return null;

  // Extract organization name from title
  const orgName = data.title.split(' - ')[0];

  return (
    <div>
      <a 
        href={data.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block hover:no-underline"
      >
        <div className="bg-white p-6 rounded-lg border hover:shadow-md transition-all duration-200">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 flex items-center justify-center">
              <img
                src="https://images.crunchbase.com/image/upload/c_pad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_2/unj63uuxb8ooxctihr1w"
                alt="Crunchbase Logo"
                className="w-full h-full object-contain"
              />
            </div>

            <div className="flex flex-col">
              <span className="text-xl font-medium text-gray-900">
                {orgName}
              </span>
              <span className="text-sm text-gray-500">
                on Crunchbase
              </span>
            </div>
          </div>
        </div>
      </a>
    </div>
  );
} 