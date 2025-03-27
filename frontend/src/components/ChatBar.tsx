import React, { useState } from 'react';
import { Box, TextField, IconButton, Paper } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

interface ChatBarProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const ChatBar: React.FC<ChatBarProps> = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <Paper 
      component="form" 
      onSubmit={handleSubmit}
      sx={{ 
        p: 2, 
        display: 'flex', 
        alignItems: 'center',
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 1000
      }}
    >
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Describe what you want to create..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        disabled={disabled}
        sx={{ mr: 1 }}
      />
      <IconButton 
        type="submit" 
        color="primary"
        disabled={!message.trim() || disabled}
      >
        <SendIcon />
      </IconButton>
    </Paper>
  );
}; 