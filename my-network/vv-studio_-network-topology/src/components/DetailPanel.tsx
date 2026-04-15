import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Database, Network, Layers, CheckCircle2 } from 'lucide-react';
import { NetworkNode } from '../data';
import { cn } from '../lib/utils';

interface DetailPanelProps {
  node: NetworkNode | null;
  onClose: () => void;
}

const getTypeColorClass = (type: string) => {
  switch (type) {
    case 'mac': return 'text-mac border-mac';
    case 'windows': return 'text-win border-win';
    case 'network': return 'text-network border-network';
    case 'storage': return 'text-storage border-storage';
    default: return 'text-gray-400 border-gray-400';
  }
};

const parseStorage = (storageStr: string) => {
  const match = storageStr.match(/^(.*?)\s*\((.*?)(?:\s*-\s*(.*))?\)$/);
  if (match) {
    return {
      title: match[1].trim(),
      type: match[2].trim(),
      desc: match[3] ? match[3].trim() : ''
    };
  }
  return { title: storageStr, type: '', desc: '' };
};

export function DetailPanel({ node, onClose }: DetailPanelProps) {
  if (!node) return (
    <AnimatePresence>
      {null}
    </AnimatePresence>
  );

  const nodeColorClass = getTypeColorClass(node.type).split(' ')[0];
  const nodeBorderClass = getTypeColorClass(node.type).split(' ')[1];

  return (
    <AnimatePresence>
      {node && (
        <motion.div
          initial={{ x: '100%', opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: '100%', opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="absolute top-0 right-0 h-full w-[320px] bg-[var(--panel-bg)] border-l border-[var(--border-color)] shadow-[-10px_0_30px_rgba(0,0,0,0.5)] overflow-y-auto z-50 flex flex-col p-6 gap-6 custom-scrollbar"
        >
          {/* Header */}
          <div className="flex items-start justify-between border-b border-[var(--border-color)] pb-4 relative">
            <div className="pr-6">
              <h1 className="font-sans text-2xl font-black tracking-wide text-[var(--text-primary)] uppercase leading-tight">
                {node.label}
              </h1>
              <p className="font-sans text-[13px] text-[var(--text-secondary)] mt-1">
                {node.role}
              </p>
            </div>
            <button 
              onClick={onClose}
              className="absolute top-0 right-0 p-1 text-[var(--text-secondary)] hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 flex flex-col gap-8">
            {node.details ? (
              <>
                {/* Storage Hierarchy */}
                {node.details.storage && (
                  <div>
                    <div className={cn("flex items-center gap-2 mb-4", nodeColorClass)}>
                      <Database className="w-5 h-5" />
                      <h3 className="font-sans text-[12px] font-bold tracking-[1px] uppercase">
                        Storage Hierarchy
                      </h3>
                    </div>
                    <div className="flex flex-col gap-3">
                      {(Array.isArray(node.details.storage) ? node.details.storage : [node.details.storage]).map((item, i) => {
                        const parsed = parseStorage(item);
                        return (
                          <div key={i} className="bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md p-3.5">
                            <div className="font-sans font-bold text-[13px] text-[var(--text-primary)]">
                              {parsed.title}
                            </div>
                            {parsed.type && (
                              <div className="font-sans text-[10px] font-bold tracking-wider text-[var(--text-secondary)] uppercase mt-1.5">
                                {parsed.type}
                              </div>
                            )}
                            {parsed.desc && (
                              <div className="font-sans text-[12px] text-[var(--text-primary)] mt-0.5">
                                {parsed.desc}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Network Interconnections */}
                {node.details.network && (
                  <div>
                    <div className={cn("flex items-center gap-2 mb-4", nodeColorClass)}>
                      <Network className="w-5 h-5" />
                      <h3 className="font-sans text-[12px] font-bold tracking-[1px] uppercase">
                        Network Interconnections
                      </h3>
                    </div>
                    <div className="flex flex-col gap-2.5">
                      {node.details.network.split(',').map((net, i) => (
                        <div key={i} className="flex items-center gap-2.5 text-[13px] text-[var(--text-primary)]">
                          <CheckCircle2 className={cn("w-4 h-4", nodeColorClass)} />
                          <span>{net.trim()}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Application Stack */}
                {node.details.apps && (
                  <div>
                    <div className={cn("flex items-center gap-2 mb-4", nodeColorClass)}>
                      <Layers className="w-5 h-5" />
                      <h3 className="font-sans text-[12px] font-bold tracking-[1px] uppercase">
                        Application Stack
                      </h3>
                    </div>
                    <div className="flex flex-col gap-6">
                      {Object.entries(node.details.apps).map(([category, appsStr]) => (
                        <div key={category}>
                          <div className={cn("border-l-2 pl-2.5 mb-3 font-sans text-[11px] font-bold tracking-wider uppercase text-[var(--text-secondary)]", nodeBorderClass)}>
                            {category}
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {appsStr.split(',').map((app, i) => (
                              <div key={i} className="bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md px-3 py-1.5 font-sans text-[12px] text-[var(--text-primary)] shadow-sm">
                                {app.trim()}
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <p className="text-[var(--text-secondary)] font-sans text-sm text-center">
                  No detailed configuration available for this node.
                </p>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
