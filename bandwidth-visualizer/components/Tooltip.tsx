import React from 'react';
import { TooltipProps } from 'recharts';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const CustomTooltip: React.FC<TooltipProps<any, any>> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const theoretical = payload.find(p => p.dataKey === 'theoretical')?.value;
    const realWorld = payload.find(p => p.dataKey === 'realWorld')?.value;
    const category = payload[0].payload.category;
    
    // Calculate efficiency
    const efficiency = theoretical ? Math.round((realWorld / theoretical) * 100) : 0;

    return (
      <div className="bg-slate-900/90 backdrop-blur-md border border-slate-700 p-4 rounded-xl shadow-2xl min-w-[200px] animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between mb-2">
            <h4 className="text-slate-100 font-bold text-sm">{label}</h4>
            <span className="text-[10px] uppercase tracking-wider font-semibold text-slate-400 bg-slate-800 px-2 py-0.5 rounded-full ml-2">
                {category}
            </span>
        </div>
        
        <div className="space-y-3">
          <div className="flex flex-col">
             <div className="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span>Theoretical Limit</span>
                <span className="text-cyan-200 font-mono">{theoretical} Gbps</span>
             </div>
             <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-cyan-900/50 w-full"></div>
             </div>
          </div>

          <div className="flex flex-col">
             <div className="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span>Real World</span>
                <span className="text-cyan-400 font-bold font-mono">{realWorld} Gbps</span>
             </div>
             <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div 
                    className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 shadow-[0_0_10px_rgba(34,211,238,0.5)]" 
                    style={{ width: `${Math.min(100, (realWorld / theoretical) * 100)}%` }}
                ></div>
             </div>
          </div>

          <div className="pt-2 mt-2 border-t border-slate-700 flex justify-between items-center">
            <span className="text-xs text-slate-500">Efficiency</span>
            <span className={`text-xs font-bold ${efficiency > 80 ? 'text-emerald-400' : efficiency > 50 ? 'text-yellow-400' : 'text-red-400'}`}>
                {efficiency}%
            </span>
          </div>
        </div>
      </div>
    );
  }

  return null;
};
