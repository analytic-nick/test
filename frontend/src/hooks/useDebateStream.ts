import { useEffect, useRef, useState } from 'react';
import { useDebateStore } from '@/store/debate-store';
import { DebateResponse } from '@/types/debate';

export function useDebateStream(sessionId: string) {
  const ws = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { addResponse, completeDebate, setActiveSpeaker } = useDebateStore();
  
  useEffect(() => {
    if (!sessionId) return;
    
    // Connect to WebSocket
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws/debate/${sessionId}`;
    console.log('Connecting to WebSocket:', wsUrl);
    
    ws.current = new WebSocket(wsUrl);
    
    ws.current.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      setError(null);
    };
    
    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log('WebSocket message:', message);
      
      switch (message.type) {
        case 'debate_response':
          const response: DebateResponse = message.data;
          if (!response.is_complete) {
            addResponse(response);
          } else {
            setActiveSpeaker(null);
          }
          break;
          
        case 'debate_complete':
          completeDebate(message.data);
          setActiveSpeaker(null);
          break;
          
        case 'error':
          setError(message.message);
          console.error('WebSocket error:', message.message);
          break;
      }
    };
    
    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Connection error');
    };
    
    ws.current.onclose = () => {
      console.log('WebSocket closed');
      setIsConnected(false);
    };
    
    // Cleanup
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [sessionId]);
  
  const startDebate = (question: string, personaIds: string[], mode: string = 'hybrid') => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      console.log('Starting debate:', { question, personaIds, mode });
      ws.current.send(JSON.stringify({
        action: 'start',
        question,
        persona_ids: personaIds,
        mode
      }));
    } else {
      console.error('WebSocket not connected');
      setError('Not connected to server');
    }
  };
  
  return {
    isConnected,
    error,
    startDebate
  };
}
