import React, { useMemo } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList
} from 'recharts';
import { BandwidthData, SortOption } from '../types';
import { CustomTooltip } from './Tooltip';
import { motion } from 'framer-motion';

interface BandwidthChartProps {
  data: BandwidthData[];
  scaleType: 'linear' | 'log';
  showRealWorld: boolean;
  showTheoretical: boolean;
  sortOption: SortOption;
}

// Custom label for the end of the bar
const renderCustomLabel = (props: any) => {
    const { x, y, width, height, value } = props;
    // Don't show if bar is too small
    if (width < 30) return null;
    return (
      <text 
        x={x + width - 10} 
        y={y + height / 2} 
        fill="#ecfeff" 
        textAnchor="end" 
        dominantBaseline="middle"
        className="text-[10px] font-bold"
        style={{ fontSize: '10px', textShadow: '0px 1px 2px rgba(0,0,0,0.8)' }}
      >
        {value} G
      </text>
    );
};

export const BandwidthChart: React.FC<BandwidthChartProps> = ({ 
    data, 
    scaleType,
    showRealWorld,
    showTheoretical,
    sortOption
}) => {
  // Sort data based on selected option
  const sortedData = useMemo(() => {
    const sorted = [...data];
    switch (sortOption) {
      case 'theoretical-desc':
        return sorted.sort((a, b) => b.theoretical - a.theoretical);
      case 'theoretical-asc':
        return sorted.sort((a, b) => a.theoretical - b.theoretical);
      case 'realworld-desc':
        return sorted.sort((a, b) => b.realWorld - a.realWorld);
      case 'realworld-asc':
        return sorted.sort((a, b) => a.realWorld - b.realWorld);
      case 'alpha-asc':
        return sorted.sort((a, b) => a.technology.localeCompare(b.technology));
      default:
        return sorted.sort((a, b) => b.theoretical - a.theoretical);
    }
  }, [data, sortOption]);

  // Dynamic height based on data length to prevent squishing
  const chartHeight = Math.max(600, sortedData.length * 60);

  // Tick formatter for axes
  const formatXAxis = (tick: number) => {
    if (tick >= 1000) return `${tick / 1000}T`;
    if (tick < 1) return tick.toString();
    return `${tick}G`;
  };

  // If both are shown, we want them to overlap (Real World inside Theoretical).
  // In Recharts vertical layout, we can achieve this overlap by setting a negative barGap equal to the barSize of the first bar.
  // Theoretical barSize is 24.
  const overlapGap = (showTheoretical && showRealWorld) ? -24 : 0;

  return (
    <div className="w-full relative px-2 md:px-0">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full bg-slate-900/40 rounded-3xl border border-slate-800/50 p-4 md:p-8 shadow-2xl overflow-hidden"
      >
        {/* Chart Container */}
        <div style={{ width: '100%', height: chartHeight }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              layout="vertical"
              data={sortedData}
              margin={{ top: 20, right: 30, left: 40, bottom: 20 }}
              barGap={overlapGap}
              barCategoryGap="20%"
            >
              <defs>
                {/* Gradient for Real World Bar */}
                <linearGradient id="realWorldGradient" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.8} />
                  <stop offset="100%" stopColor="#3b82f6" stopOpacity={0.9} />
                </linearGradient>
                {/* Gradient for Theoretical Bar (Indigo/Violet for better visibility) */}
                <linearGradient id="theoGradient" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#4f46e5" stopOpacity={0.5} />
                  <stop offset="100%" stopColor="#818cf8" stopOpacity={0.6} />
                </linearGradient>
              </defs>

              <CartesianGrid 
                strokeDasharray="3 3" 
                stroke="#1e293b" 
                horizontal={false} 
              />
              
              {/* Top Axis */}
              <XAxis 
                type="number" 
                scale={scaleType} 
                domain={['auto', 'auto']} 
                hide={false}
                orientation="top"
                stroke="#64748b"
                tick={{ fill: '#64748b', fontSize: 12 }}
                tickFormatter={formatXAxis}
                tickCount={8}
                allowDataOverflow={true}
                axisLine={false}
                tickLine={false}
              />

              {/* Bottom Axis */}
              <XAxis 
                type="number" 
                scale={scaleType} 
                domain={['auto', 'auto']} 
                hide={false}
                orientation="bottom"
                stroke="#64748b"
                tick={{ fill: '#64748b', fontSize: 12 }}
                tickFormatter={formatXAxis}
                tickCount={8}
                allowDataOverflow={true}
              />
              
              <YAxis 
                dataKey="technology" 
                type="category" 
                width={140}
                tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 500 }}
                interval={0}
              />

              <Tooltip 
                content={<CustomTooltip />} 
                cursor={{ fill: 'rgba(255,255,255,0.03)' }} 
              />

              {/* Theoretical Bar (Background) */}
              {showTheoretical && (
                  <Bar 
                    dataKey="theoretical" 
                    barSize={24} 
                    fill="url(#theoGradient)" 
                    radius={[0, 4, 4, 0]}
                    animationDuration={1000}
                  />
              )}

              {/* Real World Bar (Foreground/Overlay) */}
              {showRealWorld && (
                  <Bar 
                    dataKey="realWorld" 
                    barSize={showTheoretical ? 12 : 24} /* If separated, make it full width */
                    fill="url(#realWorldGradient)" 
                    radius={[0, 4, 4, 0]}
                    animationDuration={1500}
                  >
                      <LabelList dataKey="realWorld" content={renderCustomLabel} />
                  </Bar>
              )}

            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </div>
  );
};