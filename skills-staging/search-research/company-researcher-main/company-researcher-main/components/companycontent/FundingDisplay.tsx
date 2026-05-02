import { ArrowUpRight } from 'lucide-react';

interface FundingDisplayProps {
  fundingData: {
    summary: string;
    url: string;
    favicon?: string;
  };
}

export default function FundingDisplay({ fundingData }: FundingDisplayProps) {
  if (fundingData.summary.startsWith("NO")) {
    return null;
  }

  return (
    <div className="w-full">
    <h2 className="text-2xl font-normal mb-8">Funding</h2>
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <div className="prose max-w-none mb-4">
          {fundingData.summary}
        </div>
        <div className="flex items-center gap-3 text-sm text-gray-600">
          {fundingData.favicon && (
            <img 
              src={fundingData.favicon} 
              alt="Source favicon" 
              className="w-4 h-4"
            />
          )}
          <a 
            href={fundingData.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-1 font-semibold hover:text-brand-default transition-colors"
          >
            Source
            <ArrowUpRight className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
} 