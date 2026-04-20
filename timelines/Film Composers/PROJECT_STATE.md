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
