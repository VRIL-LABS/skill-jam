// app/api/scraperecenttweets/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Exa from "exa-js";

export const maxDuration = 60;

const exa = new Exa(process.env.EXA_API_KEY as string);

export async function POST(req: NextRequest) {
  try {
    const { username } = await req.json();

    if (!username) {
      return NextResponse.json({ error: 'username is required' }, { status: 400 });
    }

    const result = await exa.searchAndContents(
        `from:${username}`,
        {
          type: "keyword",
          livecrawl: "always",
          includeDomains: ["twitter.com"],
          category: "tweet",
          startPublishedDate: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString(),
          endPublishedDate: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
          includeText: [username],
        }
      )

    return NextResponse.json({ results: result.results });
  } catch (error) {
    return NextResponse.json({ error: `Failed to perform search | ${error}` }, { status: 500 });
  }
}