// components/twitter/TwitterProfileDisplay.tsx
import { Calendar, Users, TwitterIcon, UserPlus } from "lucide-react";

interface ExtractedInfo {
  bio?: string;
  name?: string;
  created_at?: string;
  followers_count?: string;
  friends_count?: string;
  statuses_count?: string;
  username?: string;
}

const extractInfoFromText = (text: string): ExtractedInfo => {
  const info: ExtractedInfo = {};
  
  // Extract bio
  const bioMatch = text.match(/^(.*?)(?=\| (?:profile_url:|name:|created_at:))/);
  if (bioMatch) {
    info.bio = bioMatch[1].trim();
  }
  
  const extractBeforeDoubleSpace = (str: string): string => {
    const parts = str.split('  ');
    return parts[0].trim();
  };

  const extractYear = (dateStr: string): string => {
    const match = dateStr.match(/20\d{2}/);
    return match ? match[0] : dateStr;
  };

  const regexPatterns: Record<keyof Omit<ExtractedInfo, 'bio' | 'username'>, RegExp> = {
    name: /\| name:\s*([^|]+)/,
    created_at: /\| created_at:\s*([^|]+)/,
    followers_count: /\| followers_count:\s*([^|]+)/,
    friends_count: /\| friends_count:\s*([^|]+)/,
    statuses_count: /\| statuses_count:\s*(\d+(?:,\d+)*)/,
  };

  // Extract and process each field
  Object.entries(regexPatterns).forEach(([key, pattern]) => {
    const match = text.match(pattern);
    if (match) {
      let value = match[1].trim();
      
      // Apply special processing based on field
      if (key === 'location' || key === 'statuses_count') {
        value = extractBeforeDoubleSpace(value);
      } else if (key === 'created_at') {
        value = extractYear(value);
      }
      
      info[key as keyof ExtractedInfo] = value;
    }
  });

  return info;
};

const formatNumber = (numStr: string): string => {
  const num = parseInt(numStr.replace(/,/g, ''));
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
  }
  return numStr;
};

interface ProfileDisplayProps {
  rawText: string;
  username?: string;
}

export default function ProfileDisplay({ rawText, username }: ProfileDisplayProps) {
  const extractedInfo = extractInfoFromText(rawText);
  const { name, followers_count, friends_count, statuses_count, created_at, bio } = extractedInfo;

  return (
    <div className="w-full bg-white border shadow-sm rounded-none overflow-hidden">
      {/* Header Banner */}
      <div className="h-32 bg-gradient-to-br from-[#4C9EEB] via-[#1DA1F2] to-[#4C9EEB]"></div>
      
      <div className="px-6">
        {/* Name and Username */}
        <div className="pt-4">
          {name && (
            <h1 className="text-xl font-bold text-gray-900">{name}</h1>
          )}
          {username && (
            <h2 className="text-gray-500">@{username}</h2>
          )}
        </div>

        {/* Bio */}
        {bio && (
          <p className="mt-4 text-gray-800 leading-relaxed">{bio}</p>
        )}

        {/* Stats Grid */}
        <div className="mt-4 flex flex-wrap gap-6">
          {followers_count && (
            <div className="flex items-center gap-1.5 text-gray-700">
              <Users className="w-4 h-4" />
              <span className="font-medium">{formatNumber(followers_count)}</span>
              <span className="text-gray-500">Followers</span>
            </div>
          )}
          {friends_count && (
            <div className="flex items-center gap-1.5 text-gray-700">
              <UserPlus className="w-4 h-4" />
              <span className="font-medium">{formatNumber(friends_count)}</span>
              <span className="text-gray-500">Following</span>
            </div>
          )}
          {statuses_count && (
            <div className="flex items-center gap-1.5 text-gray-700">
              <TwitterIcon className="w-4 h-4" />
              <span className="font-medium">{formatNumber(statuses_count)}</span>
              <span className="text-gray-500">Tweets</span>
            </div>
          )}
          {created_at && (
          <div className="flex items-center gap-1.5 text-gray-700">
            <Calendar className="w-4 h-4" />
            <span className="text-gray-500">Joined <span className="text-gray-700">{created_at}</span> </span>
          </div>
          )}
        </div>

        {/* X Profile Link */}
        {username && (
          <div className="flex justify-start mt-4 mb-4">
            <a
              href={`https://x.com/${username}`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-1.5 rounded-full border border-gray-300 text-sm font-medium hover:bg-gray-50 transition-colors"
            >
              View on X / Twitter
            </a>
          </div>
        )}

      </div>
    </div>
  );
}
