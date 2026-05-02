import FactChecker from '../components/FactChecker';

export default function Home() {
  return (
    <main className="flex relative min-h-screen flex-col items-center justify-center md:p-4">

      {/* background grid design texture code */}
      <div className="absolute inset-0 -z-0 h-full w-full bg-[radial-gradient(#80808060_1px,transparent_1px)] [background-size:30px_30px]"></div>

      <FactChecker />
    </main>
  );
}