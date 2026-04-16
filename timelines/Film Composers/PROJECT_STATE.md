# Project State: Film Composers Timeline

## 1. System Architecture
The project is a data-driven static web application supported by a Python-based data enrichment pipeline.

### File Hierarchy
```text
.
├── data/                        # JSON Data Store
├── scripts/                     # Python Data Tools
├── thumbnails/                  # Image Assets
├── composers.html               # Main Visualization
└── composer_profile.html        # Detailed View
```

## 2. Tech Stack
-   **Frontend**: HTML5, Vanilla CSS (CSS Variables, Flexbox), Vanilla JavaScript (ES6+).
-   **Data Pipeline**: Python 3.x, `requests`, `BeautifulSoup4`, `json`.
-   **Typography**: Google Fonts (Outfit).

## 3. Functional Module Summary
-   **Timeline Visualizer**: Renders a multi-track horizontal timeline of composer careers. Features include sticky headers, relative positioning based on years, and interactive film markers.
-   **Data Enrichment Pipeline**: A suite of scripts for fetching biographical data from Wikipedia, scraping film thumbnails from DuckDuckGo/Wikipedia, and validating data integrity.
-   **Dynamic Injection**: Scripts that build the final HTML by injecting processed JSON data directly into templates for zero-dependency deployment.

## 4. Recent Evolution
-   **Data Refinement**: Significantly hardened the date fetching logic (v4) to handle complex Wikipedia career summaries.
-   **UI Polish**: Implemented high-fidelity tooltips and smooth transitions for the timeline markers.
-   **Thumbnail Management**: Standardized the storage and naming convention for film poster assets.

## 5. Current Work-in-Progress
-   **Validation**: Finalizing data integrity checks across the entire composer list to ensure no missing thumbnails or broken YouTube links.
