export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  agentName?: string;
  content: string;
  timestamp: Date;
}

export interface DiagramData {
  elements: any[];
  appState: any;
  files: any;
}

export interface AgentAction {
  type: 'update_diagram' | 'send_message';
  payload: any;
} 