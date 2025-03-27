import React, { useState } from 'react';
import { Box, Paper, TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { ExcalidrawCanvas } from './components/ExcalidrawCanvas';
import { ChatHistory } from './components/ChatHistory';
import { ChatMessage, DiagramData } from './types';
import { apiService } from './services/api';

import { Excalidraw } from '@excalidraw/excalidraw';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: '1',
    role: 'agent',
    content: 'Hello! I can help you create diagrams. Please describe what you would like to visualize, such as "Create a bubble sort diagram" or "Design a system architecture".',
    timestamp: new Date(),
    agentName: 'Planner'
  }]);
  const [inputValue, setInputValue] = useState('');
  const [diagramData, setDiagramData] = useState<DiagramData>({
    elements: [],
    appState: {
      viewBackgroundColor: "#AFEEEE"
    },
    files: {}
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the API to generate the diagram
      const response = await apiService.generateDiagram({
        prompt: inputValue,
        messageId: userMessage.id
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: response.content,
        timestamp: new Date(),
        agentName: 'Planner'
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update diagram if one was generated
      if (response.diagramData) {
        setDiagramData(response.diagramData);
      }
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: 'Sorry, I encountered an error while generating the diagram.',
        timestamp: new Date(),
        agentName: 'Planner'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleDiagramChange = (data: DiagramData) => {
    setDiagramData(data);
    console.log('Diagram updated:', data);
  };

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex',
      overflow: 'hidden',
      bgcolor: '#ffffff'
    }}>
      {/* Left Panel - Chat */}
      <Box sx={{ 
        width: '350px', 
        minWidth: '350px',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        borderRight: '1px solid rgba(0, 0, 0, 0.08)'
      }}>
        <Paper 
          sx={{ 
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            borderRadius: 0,
            bgcolor: '#f8f9fa'
          }}
          elevation={0}
        >
          <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
            <ChatHistory messages={messages} />
          </Box>
          <Box sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.08)' }}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                multiline
                maxRows={4}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Describe what you want to create..."
                variant="outlined"
                size="small"
                disabled={isLoading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    bgcolor: '#ffffff',
                    '& fieldset': {
                      borderColor: 'rgba(0, 0, 0, 0.12)'
                    }
                  }
                }}
              />
              <IconButton 
                onClick={handleSend}
                color="primary"
                disabled={isLoading}
                sx={{ alignSelf: 'flex-end' }}
              >
                <SendIcon />
              </IconButton>
            </Box>
          </Box>
        </Paper>
      </Box>

      {/* Right Panel - Canvas */}
      <Box sx={{ 
        flexGrow: 1,
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2
      }}>
        <Box sx={{
          width: '1000px',
          height: '750px',
          position: 'relative',
          borderRadius: '12px',
          overflow: 'hidden'
        }}>
          <ExcalidrawCanvas
            diagramData={diagramData}
            onChange={handleDiagramChange}
          />
        </Box>
      </Box>
    </Box>
  );
}

export default App;
