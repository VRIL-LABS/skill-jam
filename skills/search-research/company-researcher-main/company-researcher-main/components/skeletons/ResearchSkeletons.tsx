import { Skeleton } from "../ui/skeleton";

export const LinkedInSkeleton = () => (
  <div className="space-y-4 animate-pulse min-h-[200px] rounded-lg p-6">
    <div className="flex items-center space-x-4">
      <Skeleton className="h-16 w-16 rounded-full" />
      <div className="space-y-2">
        <Skeleton className="h-5 w-[250px]" />
        <Skeleton className="h-4 w-[200px]" />
      </div>
    </div>
    <div className="space-y-3 mt-4">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-[90%]" />
      <Skeleton className="h-4 w-[80%]" />
    </div>
  </div>
);

export const YouTubeSkeleton = () => (
  <div className="space-y-6 min-h-[400px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[200px]" />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => (
        <div key={i} className="rounded-lg overflow-hidden">
          <Skeleton className="h-48 w-full" />
          <div className="p-4 space-y-2">
            <Skeleton className="h-5 w-full" />
            <Skeleton className="h-4 w-2/3" />
            <div className="flex items-center space-x-2 mt-2">
              <Skeleton className="h-4 w-20" />
              <Skeleton className="h-4 w-16" />
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const TikTokSkeleton = () => (
  <div className="space-y-6 min-h-[350px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[150px]" />
    </div>
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="rounded-lg overflow-hidden">
          <Skeleton className="h-64 w-full" />
          <div className="p-3 space-y-2">
            <Skeleton className="h-4 w-[80%]" />
            <Skeleton className="h-4 w-[60%]" />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const GitHubSkeleton = () => (
  <div className="space-y-6 min-h-[180px] rounded-lg p-6">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[180px]" />
    </div>
    <div className="space-y-4">
      <div className="space-y-2">
        <Skeleton className="h-5 w-full" />
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <Skeleton className="h-8 w-full rounded-md" />
        <Skeleton className="h-8 w-full rounded-md" />
      </div>
    </div>
  </div>
);

export const RedditSkeleton = () => (
  <div className="space-y-6 min-h-[300px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[150px]" />
    </div>
    {[1, 2, 3].map((i) => (
      <div key={i} className="p-4 rounded-lg space-y-3">
        <div className="flex items-start space-x-3">
          <Skeleton className="h-10 w-10 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-5 w-3/4" />
            <Skeleton className="h-4 w-1/4" />
          </div>
        </div>
        <Skeleton className="h-16 w-full" />
        <div className="flex space-x-4">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-4 w-16" />
        </div>
      </div>
    ))}
  </div>
);

export const TwitterSkeleton = () => (
  <div className="space-y-6 min-h-[450px]">
    <div className="rounded-lg p-6 space-y-4">
      <div className="flex items-center space-x-4">
        <Skeleton className="h-12 w-12 rounded-full" />
        <div className="space-y-2">
          <Skeleton className="h-5 w-[200px]" />
          <Skeleton className="h-4 w-[150px]" />
        </div>
      </div>
      <div className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-[90%]" />
      </div>
      <div className="flex space-x-6">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-5 w-24" />
      </div>
    </div>
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="p-4 rounded-lg space-y-3">
          <div className="flex items-center space-x-3">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="space-y-1 flex-1">
              <Skeleton className="h-4 w-[180px]" />
              <Skeleton className="h-4 w-[120px]" />
            </div>
          </div>
          <Skeleton className="h-16 w-full" />
          <div className="flex space-x-6">
            <Skeleton className="h-4 w-16" />
            <Skeleton className="h-4 w-16" />
            <Skeleton className="h-4 w-16" />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const CompetitorsSkeleton = () => (
  <div className="space-y-6 min-h-[300px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[200px]" />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => (
        <div key={i} className="p-5 rounded-lg space-y-3">
          <div className="flex items-center space-x-3">
            <Skeleton className="h-12 w-12 rounded-lg" />
            <Skeleton className="h-5 w-3/4" />
          </div>
          <Skeleton className="h-16 w-full" />
          <div className="flex items-center space-x-2">
            <Skeleton className="h-4 w-4 rounded-full" />
            <Skeleton className="h-4 w-24" />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const NewsSkeleton = () => (
  <div className="space-y-6 min-h-[250px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[150px]" />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => (
        <div key={i} className="rounded-lg overflow-hidden">
          <Skeleton className="h-40 w-full" />
          <div className="p-4 space-y-2">
            <Skeleton className="h-5 w-[90%]" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const FoundersSkeleton = () => (
  <div className="space-y-6 min-h-[200px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[180px]" />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => (
        <div key={i} className="p-4 rounded-lg flex items-center space-x-4">
          <Skeleton className="h-16 w-16 rounded-full" />
          <div className="space-y-2">
            <Skeleton className="h-5 w-[150px]" />
            <Skeleton className="h-4 w-[100px]" />
            <Skeleton className="h-4 w-[120px]" />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const WikipediaSkeleton = () => (
  <div className="space-y-6 min-h-[180px] rounded-lg p-6">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[200px]" />
    </div>
    <div className="space-y-3">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-[85%]" />
    </div>
  </div>
);

export const FinancialSkeleton = () => (
  <div className="space-y-6 min-h-[250px]">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[220px]" />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => (
        <div key={i} className="p-5 rounded-lg space-y-3">
          <Skeleton className="h-5 w-1/2" />
          <Skeleton className="h-8 w-3/4" />
          <div className="flex items-center space-x-2">
            <Skeleton className="h-4 w-4 rounded-full" />
            <Skeleton className="h-4 w-20" />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const FundingSkeleton = () => (
  <div className="space-y-6 min-h-[150px] rounded-lg p-6">
    <div className="space-y-4">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-[90%]" />
        <Skeleton className="h-4 w-[80%]" />
    </div>
  </div>
);

export const CompanySummarySkeleton = () => (
  <div className="space-y-6 min-h-[200px] rounded-lg p-6">
    <div className="flex items-center">
      <Skeleton className="h-7 w-[200px]" />
    </div>
    <div className="space-y-3">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-[90%]" />
      <Skeleton className="h-4 w-[85%]" />
    </div>
  </div>
); 