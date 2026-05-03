import { motion } from "framer-motion";
import { useEffect, useState, useMemo } from "react";

const YouTubePlayButton = () => (
  <svg width="68" height="48" viewBox="0 0 68 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#FF0000"/>
    <path d="M 45,24 27,14 27,34" fill="#FFFFFF"/>
  </svg>
);

interface Video {
  id: string;
  url: string;
  title: string;
  author: string | null;
}

interface VideoDetails {
  title: string;
  viewCount: string;
  publishedAt: string;
  channelTitle: string;
}

interface YoutubeVideosDisplayProps {
  videos: Video[];
}

export default function YoutubeVideosDisplay({ videos }: YoutubeVideosDisplayProps) {
  const [videoDetails, setVideoDetails] = useState<Record<string, VideoDetails>>({});

  const getVideoId = (url: string) => {
    const match = url.match(/(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/user\/\S+|\/ytscreeningroom\?v=|\/sandalsResorts#\w\/\w\/.*\/))([^\/&\?]{10,12})/);
    return match?.[1] || null;
  };

  const validVideos = useMemo(() => {
    return videos.filter(video => getVideoId(video.url) !== null);
  }, [videos]);

  if (!validVideos || validVideos.length === 0) return null;

  useEffect(() => {
    const fetchVideoDetails = async () => {
      const videoIds = validVideos.map(video => getVideoId(video.url)).filter(Boolean);
      try {
        const response = await fetch(`/api/youtubevideodetails?ids=${videoIds.join(',')}`);
        if (response.ok) {
          const data = await response.json();
          setVideoDetails(data);
        }
      } catch (error) {
        console.error('Error fetching video details:', error);
      }
    };

    fetchVideoDetails();
  }, [validVideos]);

  const formatViewCount = (viewCount: string) => {
    const count = parseInt(viewCount);
    if (count >= 1000000) {
      return `${(count / 1000000).toFixed(1)}M views`;
    } else if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}K views`;
    }
    return `${count} views`;
  };

  const getRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMilliseconds = now.getTime() - date.getTime();
    const diffInSeconds = Math.floor(diffInMilliseconds / 1000);
    const diffInMinutes = Math.floor(diffInSeconds / 60);
    const diffInHours = Math.floor(diffInMinutes / 60);
    const diffInDays = Math.floor(diffInHours / 24);
    const diffInMonths = Math.floor(diffInDays / 30);
    const diffInYears = Math.floor(diffInDays / 365);

    if (diffInYears > 0) {
      return `${diffInYears} ${diffInYears === 1 ? 'year' : 'years'} ago`;
    } else if (diffInMonths > 0) {
      return `${diffInMonths} ${diffInMonths === 1 ? 'month' : 'months'} ago`;
    } else if (diffInDays > 0) {
      return `${diffInDays} ${diffInDays === 1 ? 'day' : 'days'} ago`;
    } else if (diffInHours > 0) {
      return `${diffInHours} ${diffInHours === 1 ? 'hour' : 'hours'} ago`;
    } else if (diffInMinutes > 0) {
      return `${diffInMinutes} ${diffInMinutes === 1 ? 'minute' : 'minutes'} ago`;
    } else {
      return 'Just now';
    }
  };

  return (
    <div className="w-full">
      <h2 className="text-2xl font-normal mb-6">YouTube Videos</h2>

      <div className="w-full overflow-x-auto py-6">
        <motion.div
          className="flex space-x-6 pb-6"
          drag="x"
          dragConstraints={{ left: -((validVideos.length * 400) - window.innerWidth), right: 0 }}
          dragElastic={0.3}
        >
          {validVideos.map((video, index) => {
            const videoId = getVideoId(video.url);
            const details = videoDetails[videoId!];

            return (
              <motion.a
                key={video.id}
                href={video.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-shrink-0 w-[350px] group bg-white rounded-none shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="relative aspect-video overflow-hidden">
                  <img
                    src={`https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`}
                    alt={details?.title || video.title}
                    className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                    onError={(e) => {
                      const imgElement = e.target as HTMLImageElement;
                      imgElement.src = `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`;
                    }}
                  />
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <YouTubePlayButton />
                  </div>
                </div>
                
                <div className="p-4 space-y-2">
                  <p className="text-base font-medium line-clamp-2 text-gray-900 transition-colors duration-300">
                    {details?.title || video.title}
                  </p>
                  {details && (
                    <>
                      <p className="text-sm text-gray-600 font-medium">
                        {details.channelTitle}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatViewCount(details.viewCount)} <span className="mx-1.5 text-gray-300">•</span> {getRelativeTime(details.publishedAt)}
                      </p>
                    </>
                  )}
                </div>
              </motion.a>
            );
          })}
        </motion.div>
      </div>
    </div>
  );
}