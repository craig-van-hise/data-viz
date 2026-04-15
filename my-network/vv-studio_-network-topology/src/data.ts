export type NodeType = 'mac' | 'windows' | 'network' | 'storage';

export interface AppStack {
  production?: string;
  infrastructure?: string;
  management?: string;
}

export interface NodeDetails {
  storage?: string | string[];
  network?: string;
  apps?: AppStack;
}

export interface NetworkNode {
  id: string;
  label: string;
  role: string;
  type: NodeType;
  icon: string;
  x: number;
  y: number;
  details?: NodeDetails;
  parentId?: string; // For storage nodes
}

export interface NetworkConnection {
  id: string;
  source: string;
  target: string;
  protocol: string;
  type: 'tailscale' | 'thunderbolt' | 'ethernet' | 'wifi' | 'usb';
}

export const nodes: NetworkNode[] = [
  {
    id: 'mac-laptop',
    label: 'MAC-LAPTOP',
    role: 'Management Console',
    type: 'mac',
    icon: 'laptop',
    x: 50,
    y: 15,
    details: {
      storage: '256GB Internal SSD (Primary Storage - OS / System)',
      network: '5GHz Wi-Fi LAN, Tailscale VPN',
      apps: {
        production: 'Antigravity, Claude Code, VS Code, Obsidian',
        infrastructure: 'Tailscale',
        management: 'Jump Desktop, Microsoft Remote Desktop, Apple Screen Sharing',
      },
    },
  },
  {
    id: 'mac-mini',
    label: 'MAC-MINI',
    role: 'Infrastructure Hub',
    type: 'mac',
    icon: 'server',
    x: 80,
    y: 65,
    details: {
      storage: [
        '256GB Internal SSD (Primary Storage - OS / System)',
        '1TB M.2 NVMe (Primary Storage - Agent Sandbox)',
        '2TB M.2 NVMe (Primary Storage - Sandbox Staging / Mac Laptop Remote Work)',
        '32TB 8-Bay Array (Primary/Secondary/Tertiary - Hybrid Pool)',
      ],
      network: 'Tailscale Subnet Router, Thunderbolt 4 Bridge (SMB), 5GHz Wi-Fi LAN',
      apps: {
        production: 'Antigravity, Claude Code, VS Code, Xcode, Dorico, Notion, Reaper, Nuendo, Bidule, Blender',
        infrastructure: 'Custom App: Fortress Security Control Center, Tailscale',
      },
    },
  },
  {
    id: 'win-workstation',
    label: 'WIN-WORKSTATION',
    role: 'Production Core',
    type: 'windows',
    icon: 'monitor',
    x: 50,
    y: 65,
    details: {
      storage: [
        '8TB M.2 NVMe Internal (Primary Storage - Active Projects)',
        '8TB SATA III SSD Internal (Secondary Storage - Backups)',
        '8TB 4-Bay Array (Tertiary Storage - Cold Storage)',
      ],
      network: 'Thunderbolt 4 Bridge (SMB), 1Gb Gigabit Ethernet, 5GHz Wi-Fi LAN',
      apps: {
        production: 'Ollama, n8n, Langflow, Reaper, Nuendo, Bidule, VSL, SWAM, Sample Modeling, SPARTA, IEM, MIR PRO 3D, Wwise, Unity, Unreal Engine, Blender, OBS Studio, DaVinci Resolve',
        infrastructure: 'Docker, WSL 2, Tailscale, rtpMIDI',
      },
    },
  },
  {
    id: 'win-laptop',
    label: 'WIN-LAPTOP',
    role: 'Mobile Production',
    type: 'windows',
    icon: 'laptop',
    x: 20,
    y: 65,
    details: {
      storage: '2TB SATA III SSD (Primary Storage - Field Production)',
      network: '1Gb Gigabit Ethernet, 5GHz Wi-Fi LAN',
      apps: {
        production: 'Dorico, Notion, Reaper, Nuendo',
        infrastructure: 'Tailscale, rtpMIDI',
      },
    },
  },
  {
    id: 'wifi-lan',
    label: '5GHz Wi-Fi LAN',
    role: 'Local Boundary',
    type: 'network',
    icon: 'wifi',
    x: 50,
    y: 40,
  },
  // Peripherals
  {
    id: 'mac-nvme-1',
    label: '1TB NVMe',
    role: 'Agent Sandbox',
    type: 'storage',
    icon: 'microchip',
    x: 70,
    y: 88,
    parentId: 'mac-mini',
  },
  {
    id: 'mac-nvme-2',
    label: '2TB NVMe',
    role: 'Sandbox Staging',
    type: 'storage',
    icon: 'microchip',
    x: 80,
    y: 88,
    parentId: 'mac-mini',
  },
  {
    id: 'mac-array',
    label: '32TB Array',
    role: 'Hybrid Pool',
    type: 'storage',
    icon: 'hard-drive',
    x: 90,
    y: 88,
    parentId: 'mac-mini',
  },
  {
    id: 'win-array',
    label: '8TB Array',
    role: 'Cold Storage',
    type: 'storage',
    icon: 'hard-drive',
    x: 50,
    y: 88,
    parentId: 'win-workstation',
  },
];

export const connections: NetworkConnection[] = [
  { id: 'c1', source: 'mac-laptop', target: 'mac-mini', protocol: 'Tailscale VPN', type: 'tailscale' },
  { id: 'c2', source: 'mac-mini', target: 'win-workstation', protocol: 'Thunderbolt 4 Bridge', type: 'thunderbolt' },
  { id: 'c3', source: 'win-workstation', target: 'win-laptop', protocol: '1Gb Ethernet', type: 'ethernet' },
  { id: 'c4', source: 'mac-laptop', target: 'wifi-lan', protocol: 'Wi-Fi', type: 'wifi' },
  { id: 'c5', source: 'mac-mini', target: 'wifi-lan', protocol: 'Wi-Fi', type: 'wifi' },
  { id: 'c6', source: 'win-workstation', target: 'wifi-lan', protocol: 'Wi-Fi', type: 'wifi' },
  { id: 'c7', source: 'win-laptop', target: 'wifi-lan', protocol: 'Wi-Fi', type: 'wifi' },
  { id: 'c8', source: 'mac-mini', target: 'mac-nvme-1', protocol: 'Thunderbolt 4', type: 'thunderbolt' },
  { id: 'c9', source: 'mac-mini', target: 'mac-nvme-2', protocol: 'Thunderbolt 4', type: 'thunderbolt' },
  { id: 'c10', source: 'mac-mini', target: 'mac-array', protocol: 'USB 3', type: 'usb' },
  { id: 'c11', source: 'win-workstation', target: 'win-array', protocol: 'USB 3', type: 'usb' },
];
