import React, { useEffect, useRef } from 'react';
import { Box, Paper, Typography, Avatar } from '@mui/material';
import { ChatMessage } from '../types';

interface ChatHistoryProps {
  messages: ChatMessage[];
}

export const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Paper 
      sx={{ 
        height: '100%', 
        overflow: 'auto',
        display: 'flex',
        flexDirection: 'column',
        p: 2
      }}
    >
      {messages.map((message) => (
        <Box
          key={message.id}
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            mb: 2,
            flexDirection: message.role === 'user' ? 'row-reverse' : 'row'
          }}
        >
          <Avatar 
            sx={{ 
              bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main',
              mr: message.role === 'user' ? 0 : 1,
              ml: message.role === 'user' ? 1 : 0
            }}
          >
            {message.role === 'user' ? 'U' : message.agentName?.[0] || 'A'}
          </Avatar>
          <Box
            sx={{
              maxWidth: '70%',
              bgcolor: message.role === 'user' ? 'primary.light' : 'grey.100',
              color: message.role === 'user' ? 'primary.contrastText' : 'text.primary',
              borderRadius: 2,
              p: 1.5
            }}
          >
            {message.agentName && (
              <Typography variant="caption" sx={{ display: 'block', mb: 0.5 }}>
                {message.agentName}
              </Typography>
            )}
            <Typography>{message.content}</Typography>
          </Box>
        </Box>
      ))}
      <div ref={messagesEndRef} />
    </Paper>
  );
}; 