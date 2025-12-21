import React, { useState, useMemo } from 'react';
import { BANDWIDTH_DATA } from './constants';
import { Category, SortOption } from './types';
import { ControlPanel } from './components/ControlPanel';
import { BandwidthChart } from './components/BandwidthChart';
import { Zap } from 'lucide-react';

const App: React.FC = () => {
  const [category, setCategory] = useState<Category>('All');
  const [scaleType, setScaleType] = useState<'linear' | 'log'>('log'); // Default to log as ranges are huge
  const [showRealWorld, setShowRealWorld] = useState(true);
  const [showTheoretical, setShowTheoretical] = useState(true);
  const [sortOption, setSortOption] = useState<SortOption>('theoretical-desc');

  // Filter Data
  const filteredData = useMemo(() => {
    if (category === 'All') return BANDWIDTH_DATA;
    return BANDWIDTH_DATA.filter((item) => item.category === category);
  }, [category]);

  return (
    <div className="min-h-screen w-full flex flex-col bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black text-slate-100 font-sans">
      
      {/* Header */}
      <header className="pt-10 pb-6 px-6 text-center">
        <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 mb-4 shadow-[0_0_30px_rgba(6,182,212,0.15)]">
            <Zap className="text-cyan-400 mr-2" size={28} />
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-500">
            What's Your Bottleneck?
            </h1>
        </div>
        <p className="text-slate-400 max-w-2xl mx-auto text-sm md:text-base leading-relaxed">
          Interactive comparison of <span className="text-cyan-400 font-semibold">Real World</span> vs. <span className="text-indigo-400 font-semibold">Theoretical</span> throughput across modern digital interfaces.
        </p>
      </header>

      {/* Controls */}
      <ControlPanel 
        currentCategory={category} 
        setCategory={setCategory} 
        scaleType={scaleType}
        setScaleType={setScaleType}
        showRealWorld={showRealWorld}
        setShowRealWorld={setShowRealWorld}
        showTheoretical={showTheoretical}
        setShowTheoretical={setShowTheoretical}
        sortOption={sortOption}
        setSortOption={setSortOption}
      />

      {/* Main Content */}
      <main className="flex-grow w-full max-w-7xl mx-auto pb-20">
        <BandwidthChart 
            data={filteredData} 
            scaleType={scaleType}
            showRealWorld={showRealWorld}
            showTheoretical={showTheoretical}
            sortOption={sortOption}
        />
        
        {/* Legend / Info */}
        <div className="flex flex-col md:flex-row justify-center items-center gap-6 mt-8 text-xs text-slate-500">
           {showRealWorld && (
             <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-gradient-to-r from-cyan-500 to-blue-500 shadow-[0_0_8px_rgba(6,182,212,0.6)]"></div>
                <span>Real World Speed (Gbps)</span>
             </div>
           )}
           {showTheoretical && (
             <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-indigo-500/50 border border-indigo-400"></div>
                <span>Theoretical Max Limit (Gbps)</span>
             </div>
           )}
           <div className="hidden md:block text-slate-700">|</div>
           <div>
              *Data represents typical peak performance.
           </div>
        </div>
      </main>

    </div>
  );
};

export default App;