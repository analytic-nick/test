import { create } from 'zustand';
import { Persona, DebateResponse, DebateSession } from '@/types/debate';

interface DebateState {
  // Session data
  session: DebateSession | null;
  question: string;
  selectedPersonas: Persona[];
  
  // Debate state
  isDebating: boolean;
  responses: DebateResponse[];
  currentWave: number;
  activeSpeaker: string | null;
  tensionLevel: number;
  
  // UI state
  showShareCard: boolean;
  shareCardData: any;
  
  // Actions
  setQuestion: (question: string) => void;
  selectPersona: (persona: Persona) => void;
  deselectPersona: (personaId: string) => void;
  setSession: (session: DebateSession) => void;
  startDebate: () => void;
  addResponse: (response: DebateResponse) => void;
  setActiveSpeaker: (personaId: string | null) => void;
  calculateTension: () => void;
  completeDebate: (summary: any) => void;
  reset: () => void;
}

export const useDebateStore = create<DebateState>((set, get) => ({
  session: null,
  question: '',
  selectedPersonas: [],
  isDebating: false,
  responses: [],
  currentWave: 1,
  activeSpeaker: null,
  tensionLevel: 0,
  showShareCard: false,
  shareCardData: null,
  
  setQuestion: (question) => set({ question }),
  
  selectPersona: (persona) => {
    const { selectedPersonas } = get();
    if (selectedPersonas.length < 6 && !selectedPersonas.find(p => p.id === persona.id)) {
      set({ selectedPersonas: [...selectedPersonas, persona] });
    }
  },
  
  deselectPersona: (personaId) => {
    set({ 
      selectedPersonas: get().selectedPersonas.filter(p => p.id !== personaId) 
    });
  },
  
  setSession: (session) => set({ session }),
  
  startDebate: () => set({ isDebating: true, responses: [] }),
  
  addResponse: (response) => {
    const { responses } = get();
    set({ 
      responses: [...responses, response],
      activeSpeaker: response.persona_id,
      currentWave: response.wave || 1
    });
    
    // Calculate tension after each response
    get().calculateTension();
  },
  
  setActiveSpeaker: (personaId) => set({ activeSpeaker: personaId }),
  
  calculateTension: () => {
    const { responses } = get();
    
    let tension = 0;
    
    // Count sentiment conflicts
    const sentiments = responses.map(r => r.sentiment).filter(Boolean);
    const uniqueSentiments = new Set(sentiments);
    tension += (uniqueSentiments.size - 1) * 20;
    
    // Count rebuttals
    const rebuttals = responses.filter(r => r.is_rebuttal);
    tension += rebuttals.length * 15;
    
    // Recent activity spikes tension
    const recentResponses = responses.slice(-3);
    if (recentResponses.length === 3) {
      tension += 20;
    }
    
    // Cap at 100
    tension = Math.min(100, tension);
    
    set({ tensionLevel: tension });
  },
  
  completeDebate: (summary) => {
    set({ 
      isDebating: false,
      showShareCard: true,
      shareCardData: summary,
      activeSpeaker: null
    });
  },
  
  reset: () => set({
    question: '',
    selectedPersonas: [],
    isDebating: false,
    responses: [],
    currentWave: 1,
    activeSpeaker: null,
    tensionLevel: 0,
    showShareCard: false,
    shareCardData: null
  })
}));
