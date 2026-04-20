### FILE: project_tree.txt

.
./llms.txt
./composer_profile.html
./project_tree.txt
./composers.html
./PROJECT_CONTEXT_BUNDLE.md
./README.md
./scratch
./verified_live_profile.html
./PROJECT_STATE.md
./scripts
./scripts/final_validation.py
./scripts/scrape_and_verify_links.py
./scripts/archive
./scripts/fetch_tmdb_filmographies.py
./scripts/fetch_composer_dates.py
./scripts/patch_tmdb_filmographies.py
./scripts/update_html.py
./scripts/scrape_thumbnails.py
./# Prompts
./# Prompts/# 10.md
./# Prompts/# 24.md
./# Prompts/# 20.md
./# Prompts/# 14.md
./# Prompts/# 21.md
./# Prompts/# 15.md
./# Prompts/# 11.md
./# Prompts/# 25.md
./# Prompts/# 4.md
./# Prompts/# 5.md
./# Prompts/# 1.md
./# Prompts/# 6.md
./# Prompts/# 28.md
./# Prompts/# 2.md
./# Prompts/# 18.md
./# Prompts/# 3.md
./# Prompts/# 19.md
./# Prompts/# 7.md
./# Prompts/# 29.md
./# Prompts/# 22.md
./# Prompts/# 16.md
./# Prompts/# 8.md
./# Prompts/# 12.md
./# Prompts/# 26.md
./# Prompts/# 9.md
./# Prompts/# 13.md
./# Prompts/# 27.md
./# Prompts/# 23.md
./# Prompts/# 17.md
./data
./data/composer_lifespans.json
./data/Film Composers list.json
./data/Most important films.json
./data/blacklist.json
./thumbnails


### FILE: PROJECT_STATE.md

# Project State: Film Composers Timeline

## 1. System Architecture
The project is a high-fidelity data visualization system consisting of an interactive frontend and a robust Python-based data pipeline powered by the TMDb API.

### File Hierarchy
```text
.
├── data/                        # JSON Data Store
│   ├── filmographies/           # Pristine TMDb-sourced film credits
│   ├── Film Composers list.json # Global composer metadata
│   ├── composer_lifespans.json  # Career and life dates
│   ├── Most important films.json # Curated highlights for markers
│   └── blacklist.json           # Filter for unwanted TMDb entries
├── scripts/                     # Data Pipeline (TMDb, Enrichment)
│   ├── archive/                 # Deprecated/Debug scripts
│   ├── fetch_tmdb_filmographies.py # Primary TMDb data fetcher
│   ├── patch_tmdb_filmographies.py # TMDb edge-case patcher
│   ├── scrape_and_verify_links.py  # Unified audio scraper
│   ├── update_html.py           # Template injection script
│   ├── scrape_thumbnails.py     # Poster asset fetcher
│   ├── fetch_composer_dates.py  # Wikipedia date scraper
│   └── final_validation.py      # Data integrity checker
├── thumbnails/                  # Image Assets (Posters)
├── composer_profile.html        # Smart Timeline Visualization
└── composers.html               # Main Career Timeline
```

## 2. Tech Stack
-   **Frontend**: HTML5, Vanilla CSS (CSS Variables, Flexbox, Pseudo-elements), Vanilla JavaScript (ES6+).
-   **Graphics/Routing**: SVG (Dynamic Path Generation for "Elbow Routing").
-   **Data Pipeline**: Python 3.x, `requests`, `python-dotenv`, `beautifulsoup4`, `TMDb API`.
-   **Typography**: Google Fonts (Outfit).

## 3. Functional Module Summary
-   **Sky and Ground Visualizer**: A sophisticated timeline engine in `composer_profile.html` that separates "Important Film" labels into lanes in the "Sky" (above the track) and stacks standard markers in a "Ground" column system.
-   **Smart Collision Engine**: A dynamic JS algorithm that calculates lane occupancy, reverses Z-indexes for legibility, and generates SVG elbow paths to connect labels to markers without overlapping.
-   **TMDb Data Pipeline**: Official TMDb API integration for 100% data accuracy. Includes deduplication, chronological sorting, and targeted patching for edge cases (e.g., Tangerine Dream, Michel Legrand).
-   **Blacklist System**: A decoupled filtering layer in `data/blacklist.json` that allows for exclusion of unwanted TMDb entries (documentaries, shorts) without manual filmography editing.
-   **Unified Audio Pipeline**: Streamlined `scrape_and_verify_links.py` script using `yt-dlp` with a "Robust Threshold" algorithm to avoid re-processing healthy data gaps while ensuring complete link coverage.
-   **Automated Maintenance**: Includes `final_validation.py` for date format auditing and `scrape_thumbnails.py` for automated poster acquisition.

## 4. Recent Evolution
-   **Script Directory Purge**: Massive cleanup of the `scripts/` folder, archiving over 20 deprecated/debug scripts into `scripts/archive/` to isolate the core pipeline.
-   **Data Filtering**: Implemented the Blacklist system to handle messy TMDb data profiles, ensuring the timeline remains high-fidelity and focused on theatrical scores.
-   **Data Migration**: Completed full migration to TMDb API, rebuilding all filmography files with structured data and reliable poster paths.
-   **Layout Optimization**: Implemented dynamic vertical stacking and SVG elbow routing to prevent label collisions and improve visual clarity.

## 5. Current Work-in-Progress
-   **UI Refinement**: Fine-tuning absolute positioning of timeline tracks to ensure robust encapsulation across all viewport widths.
-   **Interactive Polishing**: Ensuring hover states and click-throughs are consistently responsive and target the correct DOM elements.
-   **Documentation Sync**: Finalizing the documentation audit to ensure all READMEs and state trackers match the refactored codebase.


### FILE: README.md

# Film Composers Data Visualization

A high-fidelity timeline and data visualization project mapping the careers and works of legendary film composers.

## Project Structure

```text
.
├── composer_profile.html        # Smart individual composer detail page
├── composers.html               # Main career timeline visualization
├── data/                        # JSON data storage
│   ├── filmographies/           # TMDb-sourced film credits per composer
│   ├── Film Composers list.json # Metadata for all composers
│   ├── composer_lifespans.json  # Career start/end and birth/death dates
│   ├── Most important films.json # Curated list for timeline markers
│   └── blacklist.json           # Filter for unwanted entries (e.g. documentaries)
├── scripts/                     # Python data pipeline
│   ├── archive/                 # Historical/Debug scripts
│   ├── fetch_tmdb_filmographies.py # Official TMDb data acquisition
│   ├── patch_tmdb_filmographies.py # Targeted TMDb fetcher for edge cases
│   ├── scrape_and_verify_links.py  # Unified yt-dlp audio scraper
│   ├── update_html.py           # Injects JSON data into templates
│   ├── scrape_thumbnails.py     # Automated poster scraper
│   └── final_validation.py      # Core data format verification
├── thumbnails/                  # Image assets for film posters
└── verified_live_profile.html   # Sandbox for UI testing
```

## Features

- **Sky and Ground Visualization**: Unique timeline layout that stacks markers in vertical columns and elevates "Most Important Films" into dynamic lanes ("Sky").
- **SVG Elbow Routing**: Precise SVG-based pole routing that connects elevated labels to their markers without visual overlap.
- **TMDb Integration + Blacklist**: Official API integration combined with a custom blacklist to ensure high-quality, theatrical-only filmographies.
- **Unified Scraper**: High-speed audio discovery using `yt-dlp` with built-in verification and rate-limit handling.
- **Dynamic Response**: JavaScript-driven layout engine that adjusts spacing and margins in real-time based on data density.
- **Premium Aesthetics**: Dark-mode UI with "Outfit" typography, soft gradients, and glassmorphism-inspired effects.

## Quick Start

1.  **View Timeline**: Open `composers.html` to see the global timeline or click on a composer to view their profile.
2.  **Update Data**: Refresh the dataset via the pipeline:
    *   **Phase 1 (TMDB)**: Run the primary fetcher:
        ```bash
        python3 scripts/fetch_tmdb_filmographies.py
        ```
    *   **Phase 2 (Audio)**: Run the unified scraper:
        ```bash
        python3 scripts/scrape_and_verify_links.py
        ```
    *   **Phase 3 (Thumbnails)**: Scrape any missing posters:
        ```bash
        python3 scripts/scrape_thumbnails.py
        ```

## Development

- **Frontend**: Pure Vanilla HTML/CSS/JS with SVG for complex routing.
- **Pipeline**: Python 3.x with a focus on structured API integration (TMDb).


