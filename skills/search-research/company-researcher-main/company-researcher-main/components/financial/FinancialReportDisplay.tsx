import React from 'react';
import { motion } from 'framer-motion';
import { FileText, ArrowUpRight } from 'lucide-react';

interface FinancialReport {
  id: string;
  url: string;
  title: string;
  author: string | null;
}

interface FinancialReportDisplayProps {
  report: FinancialReport[];
}

export default function FinancialReportDisplay({ report }: FinancialReportDisplayProps) {
  if (!report || report.length === 0) return null;

  // Helper function to clean up SEC filing titles
  const cleanTitle = (title: string) => {
    // Remove file extensions and common prefixes
    return title
      .replace(/\.(htm|html)$/, '')
      .replace(/^Form /, '')
      .replace(/-\d{8}$/, '')
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };

  return (
    <div className="mt-24">
      <h2 className="text-2xl font-normal mb-6">Company 10K Financials</h2>

      <div className="w-full overflow-x-auto py-6">
        <motion.div
          className="flex space-x-6 pb-6"
          drag="x"
          dragConstraints={{ left: -((report.length * 320) - window.innerWidth), right: 0 }}
          dragElastic={0.3}
        >
          {report.map((item, index) => (
            <motion.a
              key={item.id}
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-shrink-0 w-[300px] bg-white border rounded-lg hover:shadow-md transition-all duration-200 group"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="p-6 flex flex-col h-full">
                {/* Icon and Type */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <div className="p-2 bg-blue-50 rounded-lg group-hover:bg-blue-100 transition-colors">
                      <FileText className="w-5 h-5 text-blue-600" />
                    </div>
                    <span className="text-sm font-normal text-gray-600">
                      SEC Filing
                    </span>
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600 transition-colors" />
                </div>

                {/* Title */}
                <h3 className="text-xl font-normal transition-colors mb-2">
                  {cleanTitle(item.title)}
                </h3>
              </div>
            </motion.a>
          ))}
        </motion.div>
      </div>
    </div>
  );
}