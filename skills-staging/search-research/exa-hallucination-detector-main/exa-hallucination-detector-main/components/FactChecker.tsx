"use client";

import Link from "next/link";
import { useState, FormEvent, useRef, useEffect } from "react";
import ClaimsListResults from "./ClaimsListResult";
import LoadingMessages from "./ui/LoadingMessages";
import PreviewBox from "./PreviewBox";
import { ChevronDown, ChevronRight, ChevronUp } from "lucide-react";
import AnimatedGradientText from "./ui/animated-gradient-text";
import ShareButtons from "./ui/ShareButtons";
import { getAssetPath } from "@/lib/utils";

interface Claim {
    claim: string;
    original_text: string;
}

type FactCheckResponse = {
  claim: string;
  assessment: "True" | "False" | "Insufficient Information";
  summary: string;
  fixed_original_text: string;
  confidence_score: number;
};

export default function FactChecker() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [factCheckResults, setFactCheckResults] = useState<any[]>([]);
  const [articleContent, setArticleContent] = useState('');
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [showAllClaims, setShowAllClaims] = useState(true);

  // Create a ref for the loading or bottom section
  const loadingRef = useRef<HTMLDivElement>(null);

  // Function to scroll to the loading section
  const scrollToLoading = () => {
    loadingRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Watch for changes to `isGenerating` and scroll when it becomes `true`
  useEffect(() => {
    if (isGenerating) {
      scrollToLoading();
    }
  }, [isGenerating]);

  // Function to adjust textarea height
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = '150px';
      const scrollHeight = textarea.scrollHeight;
      textarea.style.height = `${Math.min(scrollHeight, 300)}px`;
    }
  };

  // Adjust height when content changes
  useEffect(() => {
    adjustTextareaHeight();
  }, [articleContent]);

  // Extract claims function
  const extractClaims = async (content: string) => {
    const response = await fetch(getAssetPath('/api/extractclaims'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    });
  
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to extract claims.');
    }
  
    const data = await response.json();
    return Array.isArray(data.claims) ? data.claims : JSON.parse(data.claims);
  };
  
  // ExaSearch function
  const exaSearch = async (claim: string) => {
    console.log(`Claim recieved in exa search: ${claim}`);

    const response = await fetch(getAssetPath('/api/exasearch'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ claim }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to fetch verification for claim.');
    }

    const data = await response.json();
    return data;
  };

  // Verify claims function
  const verifyClaim = async (claim: string, original_text: string, exasources: any) => {
    const response = await fetch(getAssetPath('/api/verifyclaims'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ claim, original_text, exasources }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to verify claim.');
    }

    const data = await response.json();
    console.log("VerifyClaim response:", data.claims);

    return data.claims as FactCheckResponse;
  };
   
  // Fact check function
  const factCheck = async (e: FormEvent) => {
    e.preventDefault();
  
    if (!articleContent) {
      setError("Please enter some content or try with sample blog.");
      return;
    }

    if (articleContent.length < 50) {
      setError("Too short. Please enter at least 50 characters.");
      return;
    }
  
    setIsGenerating(true);
    setError(null);
    setFactCheckResults([]);
  
    try {
      const claims = await extractClaims(articleContent);
      const finalResults = await Promise.all(
        claims.map(async ({ claim, original_text }: Claim) => {
          try {
            const exaSources = await exaSearch(claim);
            
            if (!exaSources?.results?.length) {
              return null;
            }
    
            const sourceUrls = exaSources.results.map((result: { url: any; }) => result.url);
            
            const verifiedClaim = await verifyClaim(claim, original_text, exaSources.results);
    
            return { ...verifiedClaim, original_text, url_sources: sourceUrls };
          } catch (error) {
            console.error(`Failed to verify claim: ${claim}`, error);
            return null;
          }
        })
      );
  
      setFactCheckResults(finalResults.filter(result => result !== null));
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unexpected error occurred.');
      setFactCheckResults([]);
    } finally {
      setIsGenerating(false);
    }
  };

  // Sample blog content
  const sampleBlog = `The Eiffel Tower, a remarkable iron lattice structure standing proudly in Paris, was originally built as a giant sundial in 1822, intended to cast shadows across the city to mark the hours. Designed by the renowned architect Gustave Eiffel, the tower stands 330 meters tall and once housed the city's first observatory.\n\nWhile it's famously known for hosting over 7 million visitors annually, it was initially disliked by Parisians. Interestingly, the Eiffel Tower was used as to guide ships along the Seine during cloudy nights.`;

  // Load sample content function
  const loadSampleContent = () => {
    setArticleContent(sampleBlog);
    setError(null);
  };

  return (
    <div className="flex flex-col min-h-screen z-0">

        {/* Badge positioned at the top */}
      <div className="w-full flex justify-center pt-10 opacity-0 animate-fade-up [animation-delay:200ms]">
        <Link href="https://exa.ai/" target="_blank">
          <AnimatedGradientText>
          <img 
            src={getAssetPath('/exaicon.png')} 
            alt="exa logo" 
            className="w-5 h-5 inline-block mr-2" 
          />
            <span className="inline animate-gradient bg-gradient-to-r from-[#254bf1] via-purple-600 to-[#254bf1] bg-[length:var(--bg-size)_100%] bg-clip-text text-transparent">
              Built on Exa - Search Engine for AI
            </span>
            <ChevronRight className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
          </AnimatedGradientText>
        </Link>
      </div>

      <main className="flex flex-col items-center justify-center flex-grow w-full max-w-6xl md:max-w-4xl p-6">
        <div className="text-left">
          <h1 className="md:text-6xl text-4xl pb-5 font-medium opacity-0 animate-fade-up [animation-delay:400ms]">
            Detect LLM 
            <span className="text-brand-default"> Hallucinations </span>
          </h1>

          <p className="text-gray-800 mb-12 opacity-0 animate-fade-up [animation-delay:600ms]">
            Verify your content with real web data.
          </p>
        </div>
    
        <form onSubmit={factCheck} className="space-y-6 w-full mb-10">
          <textarea
            ref={textareaRef}
            value={articleContent}
            onChange={(e) => setArticleContent(e.target.value)}
            placeholder="Enter Your Content"
            className="w-full bg-white p-3 border box-border outline-none rounded-none ring-2 ring-brand-default resize-none min-h-[150px] max-h-[250px] overflow-auto opacity-0 animate-fade-up [animation-delay:800ms] transition-[height] duration-200 ease-in-out"
          />

          <div className="pb-5">
            <button
              onClick={loadSampleContent}
              disabled={isGenerating}
              className={`px-3 py-2 border-2 border-brand-default text-brand-default font-semibold rounded-none hover:bg-brand-default hover:text-white transition-all opacity-0 animate-fade-up [animation-delay:1000ms] ${
                isGenerating ? 'cursor-not-allowed' : ''
              }`}
            >
              Try with a sample blog post
            </button>
          </div>

          <button
            type="submit"
            className={`w-full text-white mb-10 font-semibold px-2 py-2 rounded-none transition-opacity opacity-0 animate-fade-up [animation-delay:1200ms] min-h-[50px] ${
              isGenerating ? 'bg-gray-400' : 'bg-brand-default ring-2 ring-brand-default'
            } transition-colors`}
            disabled={isGenerating}
          >
            {isGenerating ? 'Detecting Hallucinations...' : 'Detect Hallucinations'}
          </button>
        </form>

        {isGenerating && (
            <div ref={loadingRef} className="w-full">
            <LoadingMessages isGenerating={isGenerating} />
            </div>
        )}

        {error && (
          <div className="mt-1 mb-14 p-3 bg-red-100 border border-red-400 animate-fade-up text-red-700 rounded-none">
            {error}
          </div>
        )}


       

        {factCheckResults.length > 0 && (
        <div className="space-y-14 mt-5 mb-32">
            <PreviewBox
            content={articleContent}
            claims={factCheckResults}
            />
            <div className="mt-4 pt-12 opacity-0 animate-fade-up [animation-delay:800ms]">
                <button
                onClick={() => setShowAllClaims(!showAllClaims)}
                className="flex items-center space-x-2 text-gray-700 hover:text-gray-900 font-medium"
                >
                {showAllClaims ? (
                    <>
                    <span>Hide Claims</span>
                    <ChevronUp size={20} />
                    </>
                ) : (
                    <>
                    <span>Show All Claims</span>
                    <ChevronDown size={20} />
                    </>
                )}
                </button>

                {/* Claims List */}
                {showAllClaims && (
                <div>
                    <ClaimsListResults results={factCheckResults} />
                </div>
                )}
            </div>
            <ShareButtons />
        </div>
        )}


      </main>
  
      <footer className="w-full py-6 px-8 mb-6 mt-auto opacity-0 animate-fade-up [animation-delay:1400ms]">
        <div className="max-w-md mx-auto">
          <p className="text-md text-center text-gray-600">
            <Link 
              href="https://dashboard.exa.ai" 
              target="_blank"
              className="underline cursor-pointer hover:text-gray-800"
            >
              Try Exa API
            </Link>
            <span className="mx-3">|</span>
            <Link 
              href="https://github.com/exa-labs/exa-hallucination-detector" 
              target="_blank"
              className="underline cursor-pointer hover:text-gray-800"
            >
              Project Code
            </Link>
            <span className="mx-3">|</span>
            <Link 
              href="https://exa.ai/demos" 
              target="_blank"
              className="underline cursor-pointer hover:text-gray-800"
            >
              See More Demo Apps
            </Link>
            <span className="mx-3">|</span>
            <Link 
              href="https://docs.exa.ai/examples/demo-hallucination-detector" 
              target="_blank"
              className="underline cursor-pointer hover:text-gray-800"
            >
              Tutorial
            </Link>
          </p>
        </div>
      </footer>
    </div>
  );
}