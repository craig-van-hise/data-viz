# Product Requirements Prompt (PRP) for Digital Bandwidth Chart

**Role:** Expert Data Visualization Designer & Front-End Developer

**Goal:** Recreate and modernize a "Digital Bandwidth Comparison" interactive chart. The goal is to maximize visual impact ("wow factor") while maintaining scientific accuracy and interactivity.

## 1. Project Overview
We have an existing Plotly-based chart that compares the real-world vs. theoretical bandwidth of various digital interfaces. We want to rebuild this with a significantly upgraded UI/UX.

## 2. The Data
Here is the accurate data extracted from the source. The values are in Gigabits per second (Gbps).

### Category: Internet (ISP)
| Technology | Real World (Gbps) | Theoretical (Gbps) |
| :--- | :--- | :--- |
| Fiber (Multi-Gig) | 9.2 | 10.0 |
| Fiber (Consumer) | 0.94 | 1.0 |
| US Avg Internet (2025) | 0.24 | 0.24 |
| Starlink (Satellite) | 0.12 | 0.25 |
| DSL (Average) | 0.04 | 0.1 |
| Dial-up | 0.00004 | 0.000056 |

### Category: Network
| Technology | Real World (Gbps) | Theoretical (Gbps) |
| :--- | :--- | :--- |
| 100G Ethernet | 94.0 | 100.0 |
| 40G Ethernet | 37.0 | 40.0 |
| Wi-Fi 7 (be) | 11.5 | 46.0 |
| 10G Ethernet | 9.4 | 10.0 |
| Wi-Fi 6E (ax) | 3.5 | 9.6 |
| 2.5G Ethernet | 2.35 | 2.5 |
| Wi-Fi 5 (ac) | 1.2 | 3.5 |
| Gigabit Ethernet | 0.94 | 1.0 |
| Wi-Fi 4 (n) | 0.24 | 0.6 |
| Fast Ethernet | 0.09 | 0.1 |

### Category: Bluetooth
| Technology | Real World (Gbps) | Theoretical (Gbps) |
| :--- | :--- | :--- |
| Bluetooth 2.1 (EDR) | 0.0021 | 0.003 |
| Bluetooth 5.0 | 0.0016 | 0.002 |
| Bluetooth 4.2 (LE) | 0.0008 | 0.001 |
| Bluetooth 1.2 | 0.0007 | 0.001 |

### Category: Peripherals (USB/Thunderbolt)
| Technology | Real World (Gbps) | Theoretical (Gbps) |
| :--- | :--- | :--- |
| Thunderbolt 5 | 64.0 | 80.0 |
| Thunderbolt 3/4 | 32.0 | 40.0 |
| USB4 | 32.0 | 40.0 |
| USB 3.2 2x2 (20Gbps) | 16.0 | 20.0 |
| USB 3.1 (10Gbps) | 8.0 | 10.0 |
| USB 3.0 (5Gbps) | 3.6 | 5.0 |
| FireWire 800 | 0.64 | 0.8 |
| USB 2.0 | 0.32 | 0.48 |
| FireWire 400 | 0.32 | 0.4 |
| USB 1.1 | 0.007 | 0.012 |

### Category: Storage
| Technology | Real World (Gbps) | Theoretical (Gbps) |
| :--- | :--- | :--- |
| NVMe Gen 5 | 116.0 | 128.0 |
| NVMe Gen 4 | 60.0 | 64.0 |
| NVMe Gen 3 | 28.0 | 32.0 |
| SATA III (SSD) | 4.5 | 6.0 |
| SATA II | 2.2 | 3.0 |
| SATA III (HDD) | 2.1 | 6.0 |
| SATA I | 1.0 | 1.5 |

### Category: System PCIe
| Technology | Real World (Gbps) | Theoretical (Gbps) |
| :--- | :--- | :--- |
| PCIe 6.0 x16 | 1008.0 | 1024.0 |
| PCIe 5.0 x16 (GPU) | 504.0 | 512.0 |
| PCIe 4.0 x16 (GPU) | 252.0 | 256.0 |
| PCIe 3.0 x16 (GPU) | 126.0 | 128.0 |
| PCIe 3.0 x1 | 7.9 | 8.0 |

## 3. Functional Requirements
1.  **Filters:** Users must be able to filter the view by category: "All", "Internet", "Network", "Bluetooth", "Peripherals", "Storage", "System PCIe".
2.  **Scales:** A toggle to switch between Linear and Logarithmic scales (crucial because values range from 0.00004 to 1000+).
3.  **Comparisons:** Visually distinguish between "Real World" and "Theoretical" performance for each item (e.g., grouped bars, overlapping bars, or a marker-on-bar design).
4.  **Responsiveness:** The chart must look good on desktop and mobile.

## 4. Design & Aesthetics (The "Wow" Factor)
You have full creative freedom to determine the layout, colors, typography, and spacing. However, please adhere to these guidelines:
*   **Modern & Premium:** Avoid default library aesthetics. Think "Apple" or "Stripe" design quality.
*   **Typography:** Use modern sans-serif fonts (e.g., Inter, Roboto, SF Pro).
*   **Color Palette:** Use a sophisticated palette. Consider dark mode or high-contrast neon-on-dark for a "tech" feel, or a clean, airy light mode. Differentiate categories with distinct but harmonious colors.
*   **Interactivity:** Add subtle animations on hover, transitions when filtering, and smooth scale changes.
*   **Layout:** Ensure labels are readable. The axis should be clear.

## 5. Technical Deliverables
*   A single-file HTML solution (or HTML + CSS + JS) that renders this chart.
*   You may use Chart.js, D3.js, Recharts, or a custom Canvas implementation—whichever yields the best visual result.
*   Ensure the code is clean and commented.

## 6. Prompt for AI Agent
"Please generate the complete code for the application described above. Focus heavily on the visual polish—make it look beautiful and professional."
