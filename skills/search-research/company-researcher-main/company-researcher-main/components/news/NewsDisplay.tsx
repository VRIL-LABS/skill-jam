import React from 'react';
import { motion } from 'framer-motion';

interface NewsItem {
  url: string;
  title: string;
  image: string;
}

interface NewsDisplayProps {
  news: NewsItem[];
}

const NewsDisplay: React.FC<NewsDisplayProps> = ({ news }) => {
  // Helper function to extract domain from URL
  const extractDomain = (url: string) => {
    try {
      const domain = new URL(url).hostname.replace('www.', '');
      return domain;
    } catch {
      return url;
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-normal mb-6">Latest News</h2>

      <div className="w-full overflow-x-auto py-6">
        <motion.div
          className="flex space-x-6 pb-6"
          drag="x"
          dragConstraints={{ left: -((news.length * 280) - window.innerWidth), right: 0 }}
          dragElastic={0.3}
        >
          {news.map((item, index) => (
            <motion.a
              key={index}
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-shrink-0 w-60 md:w-72 bg-white border rounded-none shadow-sm overflow-hidden transition-all hover:scale-105 hover:shadow-md"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="relative h-32 md:h-40 w-full">
                {item.image ? (
                  <img
                    src={item.image}
                    alt={item.title}
                    className="object-cover w-full h-full"
                    onError={(e) => {
                      const imgElement = e.target as HTMLImageElement;
                      imgElement.onerror = null;
                      // Instead of loading a placeholder image, show a div with background color
                      imgElement.style.display = 'none';
                      imgElement.parentElement!.classList.add('bg-blue-100');
                      imgElement.parentElement!.innerHTML = `
                        <div class="flex items-center justify-center h-full text-gray-500 p-3 group-hover:text-brand-default">
                          ${item.title.slice(0, 50)}${item.title.length > 50 ? '...' : ''}
                        </div>
                      `;
                    }}
                  />
                ) : (
                  <div className="flex items-center justify-center h-full bg-gray-100 text-gray-500">
                    <span className="px-4 text-center">
                      {item.title.slice(0, 50)}${item.title.length > 50 ? '...' : ''}
                    </span>
                  </div>
                )}
              </div>
              <div className="p-5">
                <p className="text-normal line-clamp-2 mb-2">
                  {item.title}
                </p>
                <div className="text-sm text-gray-500 transition-colors">
                  {extractDomain(item.url)}
                </div>
              </div>
            </motion.a>
          ))}
        </motion.div>
      </div>

    </div>
  );
};

export default NewsDisplay;