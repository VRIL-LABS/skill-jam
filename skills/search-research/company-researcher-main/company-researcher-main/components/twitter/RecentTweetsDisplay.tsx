import { TwitterIcon, ChevronDown, ChevronUp } from "lucide-react";
import { Tweet } from "react-tweet";
import { motion } from "framer-motion";
import { useState } from "react";

interface Tweet {
  id: string;
  url: string;
  title: string;
  author: string | null;
}

interface RecentTweetsDisplayProps {
  tweets: Tweet[];
}

export default function RecentTweetsDisplay({ tweets }: RecentTweetsDisplayProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!tweets || tweets.length === 0) return null;

  const validTweets = tweets.filter(tweet => {
    const statusMatch = tweet.url.match(/\/status\/(\d+)/);
    return statusMatch && statusMatch[1];
  });

  if (validTweets.length === 0) return null;

  return (
    <div className="w-full">
      <div className="w-full overflow-x-auto py-6">
        <motion.div
          className="flex space-x-6 pb-6"
          drag="x"
          dragConstraints={{ left: -((validTweets.length * 400) - window.innerWidth), right: 0 }}
          dragElastic={0.3}
        >
          {validTweets.map((tweet, index) => (
            <motion.div
              key={tweet.id}
              className="flex-shrink-0 w-[350px] relative"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              data-theme="light"
            >
              <div className={`${isExpanded ? '' : 'max-h-[500px] overflow-hidden'}`}>
                <Tweet 
                  id={tweet.url.match(/\/status\/(\d+)/)?.[1] || ''} 
                />
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
      <div className="flex justify-start mt-4 pl-2">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-sm text-gray-600 hover:text-gray-800 transition-colors flex items-center gap-2"
        >
          {isExpanded ? (
            <>
              Show less <ChevronUp className="w-4 h-4" />
            </>
          ) : (
            <>
              Show full tweets <ChevronDown className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
} 