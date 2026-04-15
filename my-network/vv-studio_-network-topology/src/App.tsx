import React, { useState } from 'react';
import { NetworkDiagram } from './components/NetworkDiagram';
import { DetailPanel } from './components/DetailPanel';
import { nodes } from './data';

export default function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const selectedNode = selectedNodeId ? nodes.find(n => n.id === selectedNodeId) || null : null;

  return (
    <div className="w-screen h-screen bg-[var(--bg-color)] text-[var(--text-primary)] overflow-hidden flex flex-col font-sans">
      {/* Header */}
      <header className="absolute top-0 left-0 w-full p-6 z-20 pointer-events-none">
        <h1 className="font-mono text-[14px] uppercase tracking-[2px] text-[var(--text-secondary)] mb-5 border-b border-[var(--border-color)] pb-2 max-w-[300px]">
          VV Studio: Network Topology
        </h1>
      </header>

      {/* Main Canvas */}
      <main className={`flex-1 relative transition-[margin] duration-300 ease-in-out ${selectedNodeId ? 'mr-[320px]' : 'mr-0'}`}>
        <NetworkDiagram 
          selectedNodeId={selectedNodeId} 
          onSelectNode={setSelectedNodeId} 
        />
      </main>

      {/* Detail Panel Overlay */}
      <DetailPanel 
        node={selectedNode} 
        onClose={() => setSelectedNodeId(null)} 
      />
    </div>
  );
}

