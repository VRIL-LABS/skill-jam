import React from 'react';

interface TracxnDisplayProps {
  data: {
    url: string;
    title: string;
  };
}

export default function TracxnDisplay({ data }: TracxnDisplayProps) {
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
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMnv4-Pp4T35SPVgb1FUWBN2qmAgiWCELfFQ&s"
                alt="Tracxn Logo"
                className="w-full h-full object-contain"
              />
            </div>

            <div className="flex flex-col">
              <span className="text-xl font-medium text-gray-900">
                {orgName}
              </span>
              <span className="text-sm text-gray-500">
                on Tracxn
              </span>
            </div>
          </div>
        </div>
      </a>
    </div>
  );
} 