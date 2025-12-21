import React from 'react';
import { CATEGORIES } from '../constants';
import { Category, SortOption } from '../types';
import { LayoutGrid, Network, Globe, HardDrive, Cpu, Activity, BarChart2, Eye, EyeOff, Layers, Bluetooth, Cable, ArrowUpDown } from 'lucide-react';

interface ControlPanelProps {
  currentCategory: Category;
  setCategory: (c: Category) => void;
  scaleType: 'linear' | 'log';
  setScaleType: (s: 'linear' | 'log') => void;
  showRealWorld: boolean;
  setShowRealWorld: (show: boolean) => void;
  showTheoretical: boolean;
  setShowTheoretical: (show: boolean) => void;
  sortOption: SortOption;
  setSortOption: (s: SortOption) => void;
}

const getIcon = (cat: Category) => {
  switch (cat) {
    case 'Internet (ISP)': return <Globe size={16} />;
    case 'Network': return <Network size={16} />;
    case 'Bluetooth': return <Bluetooth size={16} />;
    case 'Peripherals': return <Cable size={16} />;
    case 'Storage': return <HardDrive size={16} />;
    case 'System PCIe': return <Cpu size={16} />;
    default: return <LayoutGrid size={16} />;
  }
};

export const ControlPanel: React.FC<ControlPanelProps> = ({
  currentCategory,
  setCategory,
  scaleType,
  setScaleType,
  showRealWorld,
  setShowRealWorld,
  showTheoretical,
  setShowTheoretical,
  sortOption,
  setSortOption,
}) => {
  return (
    <div className="sticky top-0 z-20 bg-slate-950/80 backdrop-blur-md border-b border-slate-800 py-4 px-4 md:px-8 mb-6">
      <div className="max-w-7xl mx-auto flex flex-col xl:flex-row gap-4 justify-between items-center">
        
        {/* Category Filters - Scrollable on mobile */}
        <div className="w-full xl:w-auto overflow-x-auto pb-2 xl:pb-0 no-scrollbar order-2 xl:order-1">
          <div className="flex gap-2 min-w-max px-1">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300
                  ${currentCategory === cat 
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/50 shadow-[0_0_15px_rgba(6,182,212,0.3)]' 
                    : 'bg-slate-900 text-slate-400 border border-slate-800 hover:bg-slate-800 hover:text-slate-200'}
                `}
              >
                {getIcon(cat)}
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Right Side Controls */}
        <div className="flex flex-wrap justify-center md:justify-end gap-3 w-full xl:w-auto order-1 xl:order-2">
            
            {/* Sort Dropdown */}
            <div className="relative group flex items-center bg-slate-900 rounded-lg border border-slate-800 px-3 py-1.5 shrink-0">
               <ArrowUpDown size={14} className="text-slate-500 mr-2" />
               <select
                  value={sortOption}
                  onChange={(e) => setSortOption(e.target.value as SortOption)}
                  className="bg-transparent text-xs font-bold uppercase tracking-wide text-slate-400 hover:text-slate-200 focus:outline-none appearance-none cursor-pointer pr-4"
               >
                  <option value="theoretical-desc">Theoretical (High → Low)</option>
                  <option value="theoretical-asc">Theoretical (Low → High)</option>
                  <option value="realworld-desc">Real World (High → Low)</option>
                  <option value="realworld-asc">Real World (Low → High)</option>
                  <option value="alpha-asc">Name (A → Z)</option>
               </select>
            </div>

            {/* Visibility Toggles */}
            <div className="flex bg-slate-900 p-1 rounded-lg border border-slate-800 shrink-0">
                 <button
                    onClick={() => setShowRealWorld(!showRealWorld)}
                    className={`
                    flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-bold uppercase tracking-wide transition-all
                    ${showRealWorld
                        ? 'bg-cyan-900/40 text-cyan-400 shadow-sm border border-cyan-500/20' 
                        : 'text-slate-600 hover:text-slate-400'}
                    `}
                    title="Toggle Real World Data"
                >
                    {showRealWorld ? <Eye size={14} /> : <EyeOff size={14} />} <span className="hidden sm:inline">Real</span>
                </button>
                <button
                    onClick={() => setShowTheoretical(!showTheoretical)}
                    className={`
                    flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-bold uppercase tracking-wide transition-all
                    ${showTheoretical
                        ? 'bg-slate-700 text-slate-200 shadow-sm' 
                        : 'text-slate-600 hover:text-slate-400'}
                    `}
                    title="Toggle Theoretical Data"
                >
                    {showTheoretical ? <Layers size={14} /> : <EyeOff size={14} />} <span className="hidden sm:inline">Theo</span>
                </button>
            </div>

            {/* Scale Toggle */}
            <div className="flex bg-slate-900 p-1 rounded-lg border border-slate-800 shrink-0">
            <button
                onClick={() => setScaleType('linear')}
                className={`
                flex items-center gap-2 px-3 sm:px-4 py-1.5 rounded-md text-xs font-bold uppercase tracking-wide transition-all
                ${scaleType === 'linear' 
                    ? 'bg-slate-700 text-white shadow-sm' 
                    : 'text-slate-500 hover:text-slate-300'}
                `}
            >
                <Activity size={14} /> <span className="hidden sm:inline">Lin</span>
            </button>
            <button
                onClick={() => setScaleType('log')}
                className={`
                flex items-center gap-2 px-3 sm:px-4 py-1.5 rounded-md text-xs font-bold uppercase tracking-wide transition-all
                ${scaleType === 'log' 
                    ? 'bg-slate-700 text-white shadow-sm' 
                    : 'text-slate-500 hover:text-slate-300'}
                `}
            >
                <BarChart2 size={14} /> <span className="hidden sm:inline">Log</span>
            </button>
            </div>
        </div>

      </div>
    </div>
  );
};
