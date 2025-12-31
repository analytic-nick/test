'use client';

import { useState, useEffect } from 'react';
import { useDebateStore } from '@/store/debate-store';
import { useDebateStream } from '@/hooks/useDebateStream';
import { Persona } from '@/types/debate';

export default function DebatePage() {
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [sessionId, setSessionId] = useState<string>('');
  
  const {
    question,
    setQuestion,
    selectedPersonas,
    selectPersona,
    deselectPersona,
    isDebating,
    responses,
    activeSpeaker,
    tensionLevel,
    startDebate: startDebateStore,
    reset
  } = useDebateStore();
  
  const { isConnected, error, startDebate } = useDebateStream(sessionId);
  
  useEffect(() => {
    // Generate session ID
    setSessionId(`session-${Date.now()}`);
    
    // Fetch personas
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/personas`)
      .then(res => res.json())
      .then(data => setPersonas(data.personas))
      .catch(err => console.error('Error fetching personas:', err));
  }, []);
  
  const handleStartDebate = () => {
    if (!question.trim() || selectedPersonas.length < 2) {
      alert('Please enter a question and select at least 2 personas');
      return;
    }
    
    startDebateStore();
    const personaIds = selectedPersonas.map(p => p.id);
    startDebate(question, personaIds, 'hybrid');
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
          Synthetic Focus Group
        </h1>
        
        {/* Connection Status */}
        <div className="mb-4 text-sm text-center">
          {isConnected ? (
            <span className="text-green-400">● Connected</span>
          ) : (
            <span className="text-yellow-400">○ Connecting...</span>
          )}
          {error && <span className="text-red-400 ml-4">Error: {error}</span>}
        </div>
        
        {!isDebating ? (
          <>
            {/* Question Input */}
            <div className="mb-8">
              <label className="block text-sm font-medium mb-2">Your Question</label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What do people think about..."
                className="w-full p-4 rounded-lg bg-slate-800 border border-slate-700 focus:border-purple-500 focus:outline-none resize-none"
                rows={3}
              />
            </div>
            
            {/* Persona Selection */}
            <div className="mb-8">
              <label className="block text-sm font-medium mb-4">
                Select Personas ({selectedPersonas.length}/6)
              </label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {personas.map(persona => {
                  const isSelected = selectedPersonas.find(p => p.id === persona.id);
                  return (
                    <button
                      key={persona.id}
                      onClick={() => isSelected ? deselectPersona(persona.id) : selectPersona(persona)}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        isSelected
                          ? 'border-purple-500 bg-purple-500/20'
                          : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                      }`}
                    >
                      <div className="font-semibold mb-1">{persona.name}</div>
                      <div className="text-xs text-slate-400">{persona.category}</div>
                    </button>
                  );
                })}
              </div>
            </div>
            
            {/* Start Button */}
            <div className="text-center">
              <button
                onClick={handleStartDebate}
                disabled={!isConnected || selectedPersonas.length < 2 || !question.trim()}
                className="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:from-purple-600 hover:to-blue-600 transition-all"
              >
                Start Focus Group
              </button>
            </div>
          </>
        ) : (
          <>
            {/* Debate View */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4">{question}</h2>
              
              {/* Tension Meter */}
              <div className="mb-6">
                <div className="flex justify-between text-sm mb-2">
                  <span>Debate Intensity</span>
                  <span>{tensionLevel}%</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 transition-all duration-500"
                    style={{ width: `${tensionLevel}%` }}
                  />
                </div>
              </div>
              
              {/* Responses */}
              <div className="space-y-4">
                {responses.map((response, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      activeSpeaker === response.persona_id
                        ? 'border-purple-500 bg-purple-500/10'
                        : 'border-slate-700 bg-slate-800'
                    }`}
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <div className="font-semibold">{response.persona_name}</div>
                      <div className="text-xs px-2 py-1 rounded-full bg-slate-700">
                        Wave {response.wave}
                      </div>
                      {response.sentiment && (
                        <div className={`text-xs px-2 py-1 rounded-full ${
                          response.sentiment === 'positive' ? 'bg-green-500/20 text-green-400' :
                          response.sentiment === 'negative' ? 'bg-red-500/20 text-red-400' :
                          'bg-slate-700 text-slate-400'
                        }`}>
                          {response.sentiment}
                        </div>
                      )}
                    </div>
                    <div className="text-slate-300">{response.text}</div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Reset Button */}
            <div className="text-center">
              <button
                onClick={reset}
                className="px-6 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-all"
              >
                Start New Debate
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
