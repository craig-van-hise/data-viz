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
│   └── Most important films.json # Curated highlights for markers
├── scripts/                     # Data Pipeline (TMDb, Enrichment)
│   ├── fetch_tmdb_filmographies.py # Primary TMDb data fetcher
│   └── update_html.py           # Template injection script
├── thumbnails/                  # Image Assets (Posters)
├── composer_profile.html        # Smart Timeline Visualization
└── composers.html               # Main Career Timeline
```

## 2. Tech Stack
-   **Frontend**: HTML5, Vanilla CSS (CSS Variables, Flexbox, Pseudo-elements), Vanilla JavaScript (ES6+).
-   **Graphics/Routing**: SVG (Dynamic Path Generation for "Elbow Routing").
-   **Data Pipeline**: Python 3.x, `requests`, `python-dotenv`, `TMDb API`.
-   **Typography**: Google Fonts (Outfit).

## 3. Functional Module Summary
-   **Sky and Ground Visualizer**: A sophisticated timeline engine in `composer_profile.html` that separates "Important Film" labels into lanes in the "Sky" (above the track) and stacks standard markers in a "Ground" column system.
-   **Smart Collision Engine**: A dynamic JS algorithm that calculates lane occupancy, reverses Z-indexes for legibility, and generates SVG elbow paths to connect labels to markers without overlapping.
-   **TMDb Data Pipeline**: Transitioned from unreliable web scraping to the official TMDb API for 100% data accuracy. Includes deduplication and chronological sorting.
-   **Dynamic Layout Engine**: Replaced static CSS margins with JS-driven math that calculates `marginTop` and `marginBottom` based on the stack height and lane count.

## 4. Recent Evolution
-   **Data Migration**: Completed full migration to TMDb API, rebuilding all filmography files with structured data and reliable poster paths.
-   **Layout Optimization**: Implemented dynamic vertical stacking to prevent data loss in busy years, replacing old modulo-based staggering.
-   **Visual Overhaul**: Implemented SVG elbow routing for flag posts, decoupled hover animations for cleaner feedback, and extended the timeline track visually with a pseudo-element pill design.

## 5. Current Work-in-Progress
-   **Final UI Tweaks**: Refining the absolute positioning of the timeline track and axis to ensure perfect encapsulation of all markers and labels across viewport sizes.
-   **Hover Cleanup**: Ensuring hover interactions target only the interactive dot elements while keeping the "Sky" flags static.
