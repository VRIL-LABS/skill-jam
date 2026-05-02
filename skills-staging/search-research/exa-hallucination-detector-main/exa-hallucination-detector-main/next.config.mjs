/** @type {import('next').NextConfig} */

const nextConfig = {
    basePath: "/hallucination-detector",
    experimental: {
      serverActions: {
        allowedOrigins: ["demo.exa.ai"],
        allowedForwardedHosts: ["demo.exa.ai"],
      },
    },
  };
  
export default nextConfig;