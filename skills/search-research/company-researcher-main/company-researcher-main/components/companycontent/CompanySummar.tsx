import React from 'react';

interface SummaryItem {
  heading: string;
  text: string;
}

interface CompanySummaryProps {
  summary: SummaryItem[];
}

const CompanySummary: React.FC<CompanySummaryProps> = ({ summary }) => {
  return (
    <div className="w-full space-y-4">
      
      <div className="bg-white border shadow-sm p-4 sm:p-8 mt-2">
        <div className="space-y-6">
          {summary.map((item, index) => (
            <div key={index} className="space-y-2">
              <div className="flex items-start gap-2 sm:gap-3">
                <span className="text-xl sm:text-2xl flex-shrink-0">{item.heading.split(' ')[0]}</span>
                <div className="space-y-2 sm:space-y-3 pt-1 w-full">
                  <p className="font-semibold text-base sm:text-lg">
                    {item.heading.split(' ').slice(1).join(' ')}
                  </p>
                  <p className="text-gray-700 leading-relaxed text-sm sm:text-base">
                    {item.text}
                  </p>
                </div>
              </div>
              
              {index < summary.length - 1 && (
                <div className="pt-4 sm:pt-6">
                  <div className="border-t border-gray-100"></div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CompanySummary;