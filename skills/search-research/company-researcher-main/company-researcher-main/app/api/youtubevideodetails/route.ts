import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const videoIds = searchParams.get('ids');

  if (!videoIds) {
    return NextResponse.json({ error: 'Video IDs are required' }, { status: 400 });
  }

  try {
    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=${videoIds}&key=${process.env.YOUTUBE_API_KEY}`,
      { next: { revalidate: 3600 } } // Cache for 1 hour
    );

    const data = await response.json();
    
    const formattedData: Record<string, any> = {};
    
    data.items.forEach((item: any) => {
      formattedData[item.id] = {
        title: item.snippet.title,
        viewCount: item.statistics.viewCount,
        publishedAt: item.snippet.publishedAt,
        channelTitle: item.snippet.channelTitle,
      };
    });

    return NextResponse.json(formattedData);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch video details' }, { status: 500 });
  }
}