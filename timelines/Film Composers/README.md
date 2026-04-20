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
