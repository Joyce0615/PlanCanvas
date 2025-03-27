import React, { useCallback, useRef, useEffect } from 'react';
import { Box } from '@mui/material';
import { Excalidraw } from '@excalidraw/excalidraw';
import type { ExcalidrawImperativeAPI } from '@excalidraw/excalidraw/types';
import { DiagramData } from '../types';
import '@excalidraw/excalidraw/index.css';

interface ExcalidrawCanvasProps {
  diagramData?: DiagramData;
  onChange?: (data: DiagramData) => void;
}

export const ExcalidrawCanvas: React.FC<ExcalidrawCanvasProps> = ({ 
  diagramData,
  onChange 
}) => {
  const lastUpdateRef = useRef<string>("");
  const updateTimeoutRef = useRef<number | undefined>(undefined);
  const excalidrawAPIRef = useRef<ExcalidrawImperativeAPI | null>(null);

  // Handle initial data loading
  useEffect(() => {
    if (diagramData && excalidrawAPIRef.current) {
      // Update the scene with all elements and background color
      excalidrawAPIRef.current.updateScene({
        elements: diagramData.elements.map(element => ({
          ...element,
          // Ensure bound elements are properly linked
          boundElements: element.boundElements || [],
          containerId: element.containerId || null
        })),
        appState: {
          ...diagramData.appState,
          viewBackgroundColor: "#AFEEEE",
          // Add necessary text element settings
          currentItemFontFamily: 1,
          currentItemTextAlign: "center",
          defaultFontSize: 20,
        },
      });
    }
  }, [diagramData]);

  const handleChange = useCallback((elements: any, state: any, files: any) => {
    if (!onChange) return;

    // Clear any pending updates
    if (updateTimeoutRef.current) {
      window.clearTimeout(updateTimeoutRef.current);
    }

    // Debounce the update
    updateTimeoutRef.current = window.setTimeout(() => {
      const newData = {
        elements: elements,
        appState: state,
        files
      };

      // Convert to string for comparison
      const newDataString = JSON.stringify(newData);

      // Only trigger onChange if the data has actually changed
      if (newDataString !== lastUpdateRef.current) {
        lastUpdateRef.current = newDataString;
        onChange(newData);
      }
    }, 100);
  }, [onChange]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (updateTimeoutRef.current) {
        window.clearTimeout(updateTimeoutRef.current);
      }
    };
  }, []);

  return (
    <Box 
      sx={{ 
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        borderRadius: '8px',
        overflow: 'hidden',
        bgcolor: '#ffffff',
        boxShadow: '0 0 0 1px rgba(0,0,0,0.1)',
        display: 'flex',
        flexDirection: 'column',
        '& .excalidraw': {
          height: '100%',
          width: '100%'
        },
        '& .excalidraw .App-menu_top': {
          padding: '0.5rem'
        },
        '& .excalidraw .Island': {
          boxShadow: 'none'
        },
        '& .excalidraw .App-menu_top .buttonList': {
          background: 'transparent'
        }
      }}
    >
      <Excalidraw
        excalidrawAPI={(api) => {
          excalidrawAPIRef.current = api;
          if (diagramData) {
            api.updateScene({
              elements: diagramData.elements.map(element => ({
                ...element,
                // Ensure bound elements are properly linked
                boundElements: element.boundElements || [],
                containerId: element.containerId || null
              })),
              appState: {
                ...diagramData.appState,
                viewBackgroundColor: "#AFEEEE",
                // Add necessary text element settings
                currentItemFontFamily: 1,
                currentItemTextAlign: "center",
                defaultFontSize: 20,
              },
            });
          }
        }}
        onChange={handleChange}
        UIOptions={{
          canvasActions: {
            changeViewBackgroundColor: false,
            export: false,
            loadScene: false,
            saveToActiveFile: false,
            saveAsImage: false
          }
        }}
        initialData={diagramData}
      />
    </Box>
  );
}; 