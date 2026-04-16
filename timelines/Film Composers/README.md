# Film Composers Data Visualization

A high-fidelity timeline and data visualization project mapping the careers and works of legendary film composers.

## Project Structure

```text
.
├── composer_profile.html        # Individual composer detail page
├── composers.html               # Main timeline visualization
├── data/                        # JSON data storage
│   ├── filmographies/           # Detailed film lists per composer
│   ├── Film Composers list.json # Metadata for all composers
│   ├── composer_lifespans.json  # Career start/end and birth/death dates
│   └── Most important films.json # Curated list for timeline markers
├── scripts/                     # Python data pipeline
│   ├── fetch_composer_dates.py  # Wikipedia scraping for lifespans
│   ├── scrape_thumbnails.py     # Image acquisition
│   ├── update_html.py           # Injects JSON data into HTML templates
│   └── final_validation.py      # Data integrity checks
├── thumbnails/                  # Image assets for film posters
└── verified_live_profile.html   # Sandbox for UI testing
```

## Features

- **Interactive Timeline**: Visual representation of composer careers from 1920 to 2030.
- **Film Markers**: Interactive nodes on the timeline showing major works with poster thumbnails and YouTube links.
- **Responsive UI**: Modern "Outfit" typography and dark-mode aesthetics.
- **Data Pipeline**: Automated scraping and enrichment scripts to maintain the composer database.

## Quick Start

1.  **View Timeline**: Open `composers.html` in any modern web browser.
2.  **Update Data**: Run Python scripts in `scripts/` to refresh lifespans or thumbnails.
    ```bash
    python3 scripts/fetch_composer_dates_v4.py
    python3 scripts/update_html.py
    ```

## Development

- **Frontend**: Vanilla HTML/CSS/JS. No framework for maximum performance and portability.
- **Pipeline**: Python 3.x focused on data scraping and JSON manipulation.
