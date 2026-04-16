# PROJECT_STATE (2026-04-16)

## 1. Architecture
```text
.
├── README.md
├── PROJECT_STATE.md
├── llms.txt
├── index.html             # Main Entry Point
├── bandwidth-visualizer/  # React/Vite Project (Bandwidth Visualizer)
│   ├── dist/
│   └── package.json
├── my-network/            # Network Visualization
│   └── vv-studio_-network-topology/ # React/Vite Project (Topology)
│       ├── dist/
│       └── package.json
├── open-alex-topics/      # HTML/JS Visualization
│   └── index.html
└── timelines/             # HTML/JS Timelines
    ├── Film Composers/
    └── Spatial Audio/
        └── index.html     # Spatial Audio Chronology
```

## 2. Tech Stack
- **Frontend Core:** HTML5, CSS3, Vanilla JavaScript
- **Bandwidth Visualizer:** React, TypeScript, Vite
- **Network Topology:** React, Lucide-React, Motion (Framer), Vite
- **Data Processing:** Python (scripts in `timelines/` for data fetching/processing)

## 3. Status
- **Functional Module Summary:**
  - **Timelines:** Interactive chronological visualizations for Film Composers and Spatial Audio history.
  - **Bandwidth Visualizer:** Tool for analyzing and visualizing digital interface speeds.
  - **Network Topology:** Interactive infrastructure mapping for VV Studio (React/Motion).
  - **Topic Exploration:** Hierarchical tree visualization of OpenAlex research data.
- **Current Work-in-Progress:**
  - Maintenance and documentation sync.

## 4. Recent Changes
- **Recent Changes:**
  - Added "VV Studio: Network Topology" visualization to the portfolio.
  - Updated main dashboard `index.html` with new interactive cards.
  - Condensed documentation and updated project state to reflect current architecture.
