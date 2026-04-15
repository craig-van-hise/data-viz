import React, { useEffect, useState, useRef } from 'react';
import { motion } from 'motion/react';
import { Monitor, Laptop, Server, Wifi, HardDrive, Database, Router, Microchip } from 'lucide-react';
import { nodes, connections, NetworkNode, NetworkConnection } from '../data';
import { cn } from '../lib/utils';

interface NetworkDiagramProps {
  selectedNodeId: string | null;
  onSelectNode: (id: string | null) => void;
}

const getIcon = (iconName: string) => {
  switch (iconName) {
    case 'laptop': return <Laptop className="w-6 h-6" />;
    case 'monitor': return <Monitor className="w-6 h-6" />;
    case 'server': return <Server className="w-6 h-6" />;
    case 'wifi': return <Router className="w-6 h-6" />;
    case 'hard-drive': return <HardDrive className="w-5 h-5" />;
    case 'database': return <Database className="w-5 h-5" />;
    case 'microchip': return <Microchip className="w-5 h-5" />;
    default: return <Monitor className="w-6 h-6" />;
  }
};

const getTypeColorClass = (type: string) => {
  switch (type) {
    case 'mac': return 'text-mac border-mac';
    case 'windows': return 'text-win border-win';
    case 'network': return 'text-network border-network';
    case 'storage': return 'text-storage border-storage';
    default: return 'text-gray-400 border-gray-400';
  }
};

const getLineStyle = (type: string) => {
  switch (type) {
    case 'tailscale': return { stroke: 'var(--line-tailscale)', strokeWidth: 2, strokeDasharray: '8 4', isAnimated: true };
    case 'thunderbolt': return { stroke: 'var(--line-thunderbolt)', strokeWidth: 4, strokeDasharray: 'none', isAnimated: false };
    case 'ethernet': return { stroke: 'var(--line-ethernet)', strokeWidth: 2, strokeDasharray: 'none', isAnimated: false };
    case 'wifi': return { stroke: 'var(--line-wifi)', strokeWidth: 2, strokeDasharray: '4 2', isAnimated: true, opacity: 0.4 };
    case 'usb': return { stroke: 'var(--line-usb)', strokeWidth: 1, strokeDasharray: 'none', isAnimated: false };
    default: return { stroke: '#ffffff', strokeWidth: 1, strokeDasharray: 'none', isAnimated: false };
  }
};

export function NetworkDiagram({ selectedNodeId, onSelectNode }: NetworkDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (!containerRef.current) return;
    
    const observer = new ResizeObserver((entries) => {
      if (entries[0]) {
        setDimensions({
          width: entries[0].contentRect.width,
          height: entries[0].contentRect.height,
        });
      }
    });
    
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  const getNodePos = (node: NetworkNode) => {
    return {
      x: (node.x / 100) * dimensions.width,
      y: (node.y / 100) * dimensions.height,
    };
  };

  return (
    <div ref={containerRef} className="relative w-full h-full bg-[var(--bg-color)] overflow-hidden" onClick={() => onSelectNode(null)}>
      {/* Background Grid */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: 'radial-gradient(var(--border-color) 1px, transparent 1px)',
          backgroundSize: '40px 40px'
        }}
      />

      {/* Legend */}
      <div className="absolute bottom-5 left-5 bg-black/60 p-3 border border-[var(--border-color)] grid grid-cols-2 gap-2 text-[10px] font-mono z-20 pointer-events-none backdrop-blur-sm">
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 bg-[var(--line-tailscale)] border-b-2 border-dashed border-black"></div> Tailscale VPN
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-1 bg-[var(--line-thunderbolt)]"></div> TB4 Bridge
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 bg-[var(--line-ethernet)]"></div> 1Gb Ethernet
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 bg-[var(--line-wifi)] opacity-50 border-b-2 border-dotted border-black"></div> 5GHz LAN
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 bg-[var(--line-usb)]"></div> USB 3
        </div>
      </div>

      {/* Connections (SVG) */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        {dimensions.width > 0 && connections.map((conn) => {
          const sourceNode = nodes.find(n => n.id === conn.source);
          const targetNode = nodes.find(n => n.id === conn.target);
          if (!sourceNode || !targetNode) return null;

          const sourcePos = getNodePos(sourceNode);
          const targetPos = getNodePos(targetNode);
          const style = getLineStyle(conn.type);

          // Use a straight line to keep the diagram clean and untangled
          const pathD = `M ${sourcePos.x} ${sourcePos.y} L ${targetPos.x} ${targetPos.y}`;

          return (
            <g key={conn.id}>
              {/* Invisible wider path for hover/click if needed, or just glow */}
              <path
                d={pathD}
                fill="none"
                stroke={style.stroke}
                strokeWidth={style.strokeWidth + 4}
                opacity={0.1}
              />
              <path
                d={pathD}
                fill="none"
                stroke={style.stroke}
                strokeWidth={style.strokeWidth}
                strokeDasharray={style.strokeDasharray}
                className={cn(style.isAnimated && "line-animated")}
                opacity={selectedNodeId ? (selectedNodeId === conn.source || selectedNodeId === conn.target ? (style.opacity || 1) : 0.2) : (style.opacity || 0.8)}
                style={{ transition: 'opacity 0.3s ease' }}
              />
            </g>
          );
        })}
      </svg>

      {/* Nodes */}
      {dimensions.width > 0 && nodes.map((node) => {
        const pos = getNodePos(node);
        const isSelected = selectedNodeId === node.id;
        const isPeripheral = node.type === 'storage';
        const isFaded = selectedNodeId && !isSelected;

        return (
          <motion.div
            key={node.id}
            className={cn(
              "absolute flex flex-col items-center justify-center cursor-pointer transition-[opacity,filter] duration-300",
              isFaded ? "opacity-30 grayscale" : "opacity-100"
            )}
            style={{
              left: pos.x,
              top: pos.y,
              x: '-50%',
              y: '-50%',
              zIndex: isSelected ? 50 : 10
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={(e) => {
              e.stopPropagation();
              onSelectNode(node.id);
            }}
          >
            {isPeripheral ? (
              <div className={cn(
                "flex flex-col items-center justify-center border bg-[var(--bg-color)] transition-all duration-300 shadow-[0_0_10px_rgba(0,0,0,0.3)]",
                "w-[72px] h-[64px] rounded-lg gap-1.5",
                getTypeColorClass(node.type),
                isSelected && "ring-2 ring-white/20 scale-110"
              )}>
                {getIcon(node.icon)}
                <span className="font-sans text-[8px] font-bold tracking-[0.5px] uppercase text-[var(--text-primary)] text-center px-1 leading-tight">
                  {node.label}
                </span>
              </div>
            ) : (
              <div className={cn(
                "flex flex-col items-center justify-center border-2 transition-all duration-300 shadow-[0_0_20px_rgba(0,0,0,0.3)]",
                node.type === 'network' ? 'rounded-full w-[120px] h-[120px]' : 'rounded-xl w-[128px] h-[104px]',
                getTypeColorClass(node.type),
                "bg-[var(--bg-color)] gap-2",
                isSelected && "scale-110 ring-4 ring-white/10 shadow-[0_0_30px_rgba(0,0,0,0.6)]"
              )}>
                {getIcon(node.icon)}
                <div className="flex flex-col items-center px-2">
                  <span className="font-sans text-[10px] font-bold tracking-[1px] uppercase text-[var(--text-primary)] text-center leading-tight">
                    {node.label}
                  </span>
                  <span className="font-mono text-[8px] text-[var(--text-secondary)] mt-1 uppercase text-center leading-tight">
                    {node.role}
                  </span>
                </div>
              </div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
