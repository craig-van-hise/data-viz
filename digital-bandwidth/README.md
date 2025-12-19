
# What is your Bottleneck? - Digital Bandwidth Comparison

An interactive data visualization comparing the **Theoretical Limits** vs. **Real-World Speeds** of common digital technologies, including Internet (ISP), Peripherals (USB/Thunderbolt), Storage (SATA/NVMe), and Networking (Wi-Fi/Ethernet).

### 🚀 [View Live Interactive Chart](https://[YOUR_USERNAME].github.io/data-visualizations/digital-bandwidth/)

## 📊 About the Project
Marketing materials often advertise "Theoretical Maximums" (e.g., 40Gbps USB4) that are rarely achievable in practice due to protocol overhead, encoding efficiency, and hardware limitations.

This chart visualizes that gap, helping users understand:
1.  **The Reality Gap:** How much speed you actually lose to overhead (Green vs. Blue bars).
2.  **Scale:** The massive difference between a Dial-up connection (56k) and a PCIe 5.0 GPU link (64GB/s).
3.  **Bottlenecks:** Why your fast SSD might be limited by your slow USB port.

## 🎛️ Interactive Features
The visualization is built with **Python (Plotly)** and features a fully interactive toolbar:

* **🔍 Dynamic Filtering:** Focus on specific categories (e.g., *Storage only*, *Networking only*) with dynamic height resizing to keep the view clean.
* **A-Z / Speed Sorting:** Sort by Category groups or purely by Speed (Low → High / High → Low).
* **Logarithmic vs. Linear Scale:**
    * *Log Scale (Default):* Allows massive differences (Dial-up vs. Fiber) to be visible on the same screen.
    * *Linear Scale:* Shows the true, brutal difference in raw throughput.
* **Hover Data:** Hover over any bar to see the exact Gbps values for both Theoretical and Real-World performance.

## 🛠️ Technology Stack
* **Language:** Python 3.10+
* **Libraries:**
    * `plotly`: For generating the interactive HTML/JS graph.
    * `pandas`: For data structuring and sorting.
* **Output:** Standalone HTML5 file (No server required).

## 📂 Project Structure
```text
data-visualizations/
└── digital-bandwidth/
    ├── index.html       # The interactive chart (generated output)
    └── README.md        # This documentation

```

## 📝 Data Sources

Data points were aggregated from technical specifications (USB-IF, IEEE 802.11 standards, SATA-IO) and real-world benchmark averages.

* **Theoretical:** The raw signaling rate defined by the physical interface standard.
* **Real-World:** Calculated based on encoding overhead (e.g., 8b/10b, 128b/132b) and protocol efficiency.


*Created by Craig Van Hise- [virtualvirgin.net](https://www.virtualvirgin.net/)*

