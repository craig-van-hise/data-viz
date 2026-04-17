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
2.  **Update Data**: Refresh filmography data using the TMDb fetcher.
    ```bash
    export TMDB_API_READ_ACCESS_TOKEN="your_token_here"
    python3 scripts/fetch_tmdb_filmographies.py
    ```

## Development

- **Frontend**: Pure Vanilla HTML/CSS/JS with SVG for complex routing.
- **Pipeline**: Python 3.x with a focus on structured API integration (TMDb).
