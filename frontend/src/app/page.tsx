'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-purple-900/20 to-slate-950 text-white">
      <div className="max-w-6xl mx-auto px-8 py-20">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            Synthetic Focus Group
          </h1>
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Get instant feedback from AI personas representing different demographics, 
            professions, and personalities. Watch them debate your ideas in real-time.
          </p>
          <Link
            href="/debate"
            className="inline-block px-8 py-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg font-semibold text-lg hover:from-purple-600 hover:to-blue-600 transition-all hover:scale-105"
          >
            Start a Focus Group
          </Link>
        </div>
        
        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          <div className="p-6 rounded-lg bg-slate-800/50 border border-slate-700">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold mb-2">Instant Feedback</h3>
            <p className="text-slate-400">
              No waiting days for survey responses. Get diverse perspectives in 30 seconds.
            </p>
          </div>
          
          <div className="p-6 rounded-lg bg-slate-800/50 border border-slate-700">
            <div className="text-3xl mb-4">🎭</div>
            <h3 className="text-xl font-semibold mb-2">Diverse Personas</h3>
            <p className="text-slate-400">
              From Gen Z teens to corporate VPs, get feedback from 8+ unique perspectives.
            </p>
          </div>
          
          <div className="p-6 rounded-lg bg-slate-800/50 border border-slate-700">
            <div className="text-3xl mb-4">💬</div>
            <h3 className="text-xl font-semibold mb-2">Live Debates</h3>
            <p className="text-slate-400">
              Watch AI personas interact, disagree, and build on each other's ideas.
            </p>
          </div>
        </div>
        
        {/* How It Works */}
        <div className="text-center mb-20">
          <h2 className="text-3xl font-bold mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-purple-500 text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                1
              </div>
              <h4 className="font-semibold mb-2">Ask a Question</h4>
              <p className="text-sm text-slate-400">
                "Should I launch this product?"
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-purple-500 text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                2
              </div>
              <h4 className="font-semibold mb-2">Pick Personas</h4>
              <p className="text-sm text-slate-400">
                Choose 2-6 different perspectives
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-purple-500 text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                3
              </div>
              <h4 className="font-semibold mb-2">Watch Debate</h4>
              <p className="text-sm text-slate-400">
                See them discuss in real-time
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-purple-500 text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                4
              </div>
              <h4 className="font-semibold mb-2">Get Insights</h4>
              <p className="text-sm text-slate-400">
                Review summary and share
              </p>
            </div>
          </div>
        </div>
        
        {/* CTA */}
        <div className="text-center bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-xl p-12 border border-purple-500/30">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-slate-300 mb-8">
            Test your ideas with AI-powered focus groups. Free forever.
          </p>
          <Link
            href="/debate"
            className="inline-block px-8 py-4 bg-white text-purple-600 rounded-lg font-semibold text-lg hover:bg-slate-100 transition-all"
          >
            Launch Focus Group
          </Link>
        </div>
      </div>
    </div>
  );
}
