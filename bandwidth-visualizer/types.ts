export type Category = 'All' | 'Internet (ISP)' | 'Network' | 'Bluetooth' | 'Peripherals' | 'Storage' | 'System PCIe';

export type SortOption = 'theoretical-desc' | 'theoretical-asc' | 'realworld-desc' | 'realworld-asc' | 'alpha-asc';

export interface BandwidthData {
  id: string;
  category: Category;
  technology: string;
  realWorld: number; // Gbps
  theoretical: number; // Gbps
}

export interface ChartConfig {
  scaleType: 'linear' | 'log';
  categoryFilter: Category;
}
