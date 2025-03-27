export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
  agentName?: string;
}

export interface DiagramData {
  elements: any[];
  appState: {
    viewBackgroundColor: string;
    [key: string]: any;
  };
  files: Record<string, any>;
}

export interface DiagramRequest {
  prompt: string;
  messageId: string;
  conversationId?: string;
}

export interface DiagramResponse {
  messageId: string;
  diagramData: DiagramData;
  explanation: string;
  status: 'success' | 'error';
  error?: string;
}

export interface AgentResponse {
  messageId: string;
  content: string;
  diagramData?: DiagramData;
  status: 'success' | 'error';
  error?: string;
} 