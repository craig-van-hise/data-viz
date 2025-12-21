import { BandwidthData, Category } from './types';

export const CATEGORIES: Category[] = ['All', 'Internet (ISP)', 'Network', 'Bluetooth', 'Peripherals', 'Storage', 'System PCIe'];

export const BANDWIDTH_DATA: BandwidthData[] = [
  // Internet (ISP)
  { id: 'i1', category: 'Internet (ISP)', technology: 'Fiber (Multi-Gig)', realWorld: 9.2, theoretical: 10.0 },
  { id: 'i2', category: 'Internet (ISP)', technology: 'Fiber (Consumer)', realWorld: 0.94, theoretical: 1.0 },
  { id: 'i3', category: 'Internet (ISP)', technology: 'US Avg Internet (2025)', realWorld: 0.24, theoretical: 0.24 },
  { id: 'i4', category: 'Internet (ISP)', technology: 'Starlink (Satellite)', realWorld: 0.12, theoretical: 0.25 },
  { id: 'i5', category: 'Internet (ISP)', technology: 'DSL (Average)', realWorld: 0.04, theoretical: 0.1 },
  { id: 'i6', category: 'Internet (ISP)', technology: 'Dial-up', realWorld: 0.00004, theoretical: 0.000056 },

  // Network
  { id: 'n1', category: 'Network', technology: '100G Ethernet', realWorld: 94.0, theoretical: 100.0 },
  { id: 'n2', category: 'Network', technology: '40G Ethernet', realWorld: 37.0, theoretical: 40.0 },
  { id: 'n3', category: 'Network', technology: 'Wi-Fi 7 (be)', realWorld: 11.5, theoretical: 46.0 },
  { id: 'n4', category: 'Network', technology: '10G Ethernet', realWorld: 9.4, theoretical: 10.0 },
  { id: 'n5', category: 'Network', technology: 'Wi-Fi 6E (ax)', realWorld: 3.5, theoretical: 9.6 },
  { id: 'n6', category: 'Network', technology: '2.5G Ethernet', realWorld: 2.35, theoretical: 2.5 },
  { id: 'n7', category: 'Network', technology: 'Wi-Fi 5 (ac)', realWorld: 1.2, theoretical: 3.5 },
  { id: 'n8', category: 'Network', technology: 'Gigabit Ethernet', realWorld: 0.94, theoretical: 1.0 },
  { id: 'n9', category: 'Network', technology: 'Wi-Fi 4 (n)', realWorld: 0.24, theoretical: 0.6 },
  { id: 'n10', category: 'Network', technology: 'Fast Ethernet', realWorld: 0.09, theoretical: 0.1 },

  // Bluetooth
  { id: 'b1', category: 'Bluetooth', technology: 'Bluetooth 2.1 (EDR)', realWorld: 0.0021, theoretical: 0.003 },
  { id: 'b2', category: 'Bluetooth', technology: 'Bluetooth 5.0', realWorld: 0.0016, theoretical: 0.002 },
  { id: 'b3', category: 'Bluetooth', technology: 'Bluetooth 4.2 (LE)', realWorld: 0.0008, theoretical: 0.001 },
  { id: 'b4', category: 'Bluetooth', technology: 'Bluetooth 1.2', realWorld: 0.0007, theoretical: 0.001 },

  // Peripherals
  { id: 'pe1', category: 'Peripherals', technology: 'Thunderbolt 5', realWorld: 64.0, theoretical: 80.0 },
  { id: 'pe2', category: 'Peripherals', technology: 'Thunderbolt 3/4', realWorld: 32.0, theoretical: 40.0 },
  { id: 'pe3', category: 'Peripherals', technology: 'USB4', realWorld: 32.0, theoretical: 40.0 },
  { id: 'pe4', category: 'Peripherals', technology: 'USB 3.2 2x2 (20Gbps)', realWorld: 16.0, theoretical: 20.0 },
  { id: 'pe5', category: 'Peripherals', technology: 'USB 3.1 (10Gbps)', realWorld: 8.0, theoretical: 10.0 },
  { id: 'pe6', category: 'Peripherals', technology: 'USB 3.0 (5Gbps)', realWorld: 3.6, theoretical: 5.0 },
  { id: 'pe7', category: 'Peripherals', technology: 'FireWire 800', realWorld: 0.64, theoretical: 0.8 },
  { id: 'pe8', category: 'Peripherals', technology: 'USB 2.0', realWorld: 0.32, theoretical: 0.48 },
  { id: 'pe9', category: 'Peripherals', technology: 'FireWire 400', realWorld: 0.32, theoretical: 0.4 },
  { id: 'pe10', category: 'Peripherals', technology: 'USB 1.1', realWorld: 0.007, theoretical: 0.012 },

  // Storage
  { id: 's1', category: 'Storage', technology: 'NVMe Gen 5', realWorld: 116.0, theoretical: 128.0 },
  { id: 's2', category: 'Storage', technology: 'NVMe Gen 4', realWorld: 60.0, theoretical: 64.0 },
  { id: 's3', category: 'Storage', technology: 'NVMe Gen 3', realWorld: 28.0, theoretical: 32.0 },
  { id: 's4', category: 'Storage', technology: 'SATA III (SSD)', realWorld: 4.5, theoretical: 6.0 },
  { id: 's5', category: 'Storage', technology: 'SATA II', realWorld: 2.2, theoretical: 3.0 },
  { id: 's6', category: 'Storage', technology: 'SATA III (HDD)', realWorld: 2.1, theoretical: 6.0 },
  { id: 's7', category: 'Storage', technology: 'SATA I', realWorld: 1.0, theoretical: 1.5 },

  // System PCIe
  { id: 'p1', category: 'System PCIe', technology: 'PCIe 6.0 x16', realWorld: 1008.0, theoretical: 1024.0 },
  { id: 'p2', category: 'System PCIe', technology: 'PCIe 5.0 x16 (GPU)', realWorld: 504.0, theoretical: 512.0 },
  { id: 'p3', category: 'System PCIe', technology: 'PCIe 4.0 x16 (GPU)', realWorld: 252.0, theoretical: 256.0 },
  { id: 'p4', category: 'System PCIe', technology: 'PCIe 3.0 x16 (GPU)', realWorld: 126.0, theoretical: 128.0 },
  { id: 'p5', category: 'System PCIe', technology: 'PCIe 3.0 x1', realWorld: 7.9, theoretical: 8.0 },
];
