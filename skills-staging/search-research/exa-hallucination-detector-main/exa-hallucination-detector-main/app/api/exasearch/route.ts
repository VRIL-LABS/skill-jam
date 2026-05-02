// app/api/exasearch/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Exa from "exa-js";

const exa = new Exa(process.env.EXA_API_KEY as string);

export async function POST(req: NextRequest) {
  try {
    const { claim } = await req.json();
    if (!claim) {
      return NextResponse.json({ error: 'Claim is required' }, { status: 400 });
    }

    // Use Exa to search for content related to the claim
    const result = await exa.searchAndContents(
      `${claim} \n\nHere is a web page to help verify this content:`,
      {
        type: "auto",
        numResults: 3,
        livecrawl: 'always',
        text: true,
      }
    );

    // Extract only url and text from each result and reverse the order
    const simplifiedResults = result.results.map((item: any) => ({
      text: item.text,
      url: item.url
    })).reverse();

    return NextResponse.json({ results: simplifiedResults });
  } catch (error) {
    return NextResponse.json({ error: `Failed to perform search | ${error}` }, { status: 500 });
  }
}