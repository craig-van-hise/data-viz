# 2026-04-16 Repo Report

## Executive Summary
This report analyzes the `data-viz` repository following the addition of the "VV Studio: Network Topology" project. The codebase consists of several independent data visualization modules, some built with React/Vite and others using vanilla HTML/JS/Python.

## Changes Since Last Key Report
*No previous REPO_REPORT was found in the root.*

## Detailed Tree & Architecture Explanation
The repository is structured as a hub-and-spoke portfolio:
- **Root**: `index.html` serves as the main dashboard, linking to individual projects.
- **Bandwidth Visualizer**: A React/Vite project in `bandwidth-visualizer/`.
- **Network Topology**: A React/Vite project in `my-network/vv-studio_-network-topology/`.
- **OpenAlex Topics**: A vanilla HTML/JS visualization with a Python data ingestion script.
- **Timelines**: A collection of HTML timelines with extensive Python data processing scripts and JSON datasets.

## Component Interaction Analysis
- **index.html**: Uses CSS Grid to display project cards. Links are hardcoded to the deployment paths (usually `dist/index.html` or direct HTML files).
- **Data Pipeline**: Python scripts in `timelines/` and `open-alex-topics/` are used to fetch data from APIs (OpenAlex, Wikipedia) and generate JSON files used by the frontend.

## Vestigial File Report

### 🔴 High Confidence (Dead / Reference Code)
- `index.html.bak`: Backup of the main entry point, no longer needed.
- `my-network/xOlder/`: Contains legacy network diagrams and administrative notes.
- `timelines/Spatial Audio/# Spatial Audio Technologies: A Chronology v2.md`: Outdated version of the chronology.
- `timelines/Spatial Audio/# Spatial Audio Technologies: A Chronology v3.md`: Outdated version of the chronology.
- `timelines/Spatial Audio/# Timeline addendum.md`: Temporary notes for the timeline.

### 🟡 Medium Confidence (Review Needed)
- `my-network/### **VV Studio- Network Topology**.txt`: Likely a text version of the topology or design notes.
- `timelines/verified_live_profile.html`: Test file for composer profiles.
- `timelines/debug_missing_final.py`: Debug script for data validation.
- `timelines/final_validation.py`: Validation script for datasets.

### 🟢 Low Confidence (Likely Useful)
- `timelines/fetch_composer_dates_v4.py`: Latest data fetching script.
- `timelines/find_overlaps.py`: Core logic for composer overlap analysis.
- `open-alex-topics/get_topics_make_tree.py`: Data generation script for the topic tree.
