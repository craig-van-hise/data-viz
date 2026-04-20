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
│   └── Most important films.json # Curated list for timeline markers
├── scripts/                     # Python data pipeline
│   ├── fetch_tmdb_filmographies.py # Official TMDb data acquisition
│   ├── patch_tmdb_filmographies.py # Targeted TMDb fetcher for edge-case composers
│   ├── scrape_and_verify_links.py  # Unified yt-dlp audio scraper with rate-limit checkpointing
│   └── update_html.py           # Injects JSON data into HTML templates
├── thumbnails/                  # Image assets for film posters
└── verified_live_profile.html   # Sandbox for UI testing
```

## Features

- **Sky and Ground Visualization**: Unique timeline layout that stacks regular markers in vertical columns and elevates "Most Important Films" into dynamic lanes ("Sky").
- **SVG Elbow Routing**: Precise SVG-based pole routing that connects elevated labels to their markers without visual overlap.
- **TMDb Integration**: All filmography data is pulled from the official TMDb API for maximum consistency and accuracy.
- **Dynamic Response**: JavaScript-driven layout engine that adjusts spacing and margins in real-time based on data density.
- **Premium Aesthetics**: Dark-mode UI with "Outfit" typography, soft gradients, and glassmorphism-inspired effects.

## Quick Start

1.  **View Timeline**: Open `composers.html` to see the global timeline or click on a composer to view their profile.
2.  **Update Data**: Refresh the dataset via the pipeline:
    *   **Phase 1 (TMDB)**: Run the primary fetcher (and patcher if needed):
        ```bash
        python3 scripts/fetch_tmdb_filmographies.py
        python3 scripts/patch_tmdb_filmographies.py
        ```
    *   **Phase 2 (Audio)**: Run the unified scraper to populate YouTube links:
        ```bash
        python3 scripts/scrape_and_verify_links.py
        ```

## Development

- **Frontend**: Pure Vanilla HTML/CSS/JS with SVG for complex routing.
- **Pipeline**: Python 3.x with a focus on structured API integration (TMDb).
