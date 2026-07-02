# Netflix Executive Intelligence Platform
## High-Fidelity Product Blueprint & Engineering Handoff

---

## 1. INFORMATION ARCHITECTURE

**Primary Navigation (Sidebar)**
The platform is organized into three strategic tiers representing operational frequency.

*   **CORE ANALYTICS**
    *   Executive Dashboard (Landing)
    *   Content Portfolio
    *   Global Expansion
    *   Genre Intelligence
    *   Audience Analytics
    *   Growth Trends
    *   Content Quality
*   **STRATEGY**
    *   Executive Insights
    *   Strategic Recommendations
*   **SYSTEM**
    *   Reports
    *   About

**Page Relationships & User Flow**
1.  **Entry Point**: User lands on **Executive Dashboard**.
2.  **Drill-Down Flow**: Clicking a KPI or summary chart on the Dashboard redirects the user to the corresponding **Core Analytics** page (e.g., clicking "Country Diversity" goes to Global Expansion).
3.  **Synthesis Flow**: After exploring analytics, users navigate to **Strategy** pages for synthesized, text-heavy strategic takeaways derived from the analytics.
4.  **Export Flow**: Users navigate to **Reports** to generate PDF snapshots of any saved views.

---

## 2. SCREEN INVENTORY

### 2.1 Executive Dashboard (Landing)
*   **Business Objective**: Provide an immediate health check of the global content catalog.
*   **User Objective**: Get a 10-second summary of scale, growth, and composition.
*   **Layout**: 1 Top row (KPIs) + 1 Middle row (Overview charts) + 1 Bottom row (Geographic map).
*   **KPIs**: Total Titles, Movies vs. TV Shows, Country Diversity.
*   **Charts**: YoY Growth Line Chart, Movie vs TV Show Donut, Global Map.
*   **Filters**: Global Date Range, Content Type toggle.

### 2.2 Content Portfolio
*   **Business Objective**: Analyze the balance between Movies and TV Shows.
*   **User Objective**: Understand if the catalog is skewing too heavily toward one format.
*   **Layout**: 1 Top row (KPIs) + 2x2 Grid (Charts).
*   **Charts**: Content Type Donut, Decade Distribution Bar, Content Type by Year Area Chart.

### 2.3 Global Expansion
*   **Business Objective**: Monitor geographic diversification and production hubs.
*   **User Objective**: Identify which countries produce the most high-value content.
*   **Layout**: Full-width Map + 2-column detail charts.
*   **Charts**: Choropleth World Map, Top 10 Countries Bar Chart, Country Content Stacked Bar, Country Treemap.

### 2.4 Genre Intelligence
*   **Business Objective**: Identify whitespace and oversaturated content genres.
*   **User Objective**: Decide which genres need more investment.
*   **Layout**: 3-column top metrics + 1 full-width chart + 2-column detailed charts.
*   **Charts**: Top Genres Bar, Genre Heatmap by Year, Genre Treemap, Genre Sunburst.

### 2.5 Audience Analytics
*   **Business Objective**: Ensure content aligns with target demographic (Mature vs. Kids).
*   **User Objective**: See maturity ratings across formats.
*   **Layout**: 2x2 Grid.
*   **Charts**: Rating Distribution Bar, Rating Pie Chart, Ratings by Content Type, Ratings Heatmap by Year.

### 2.6 Growth Trends (Timeline)
*   **Business Objective**: Analyze historical addition velocity and seasonal acquisition.
*   **User Objective**: Predict optimal release windows.
*   **Layout**: 1 Top row (Historical) + 1 Bottom row (Seasonal).
*   **Charts**: Yearly Additions Line, Cumulative Growth Line, Monthly Heatmap, Weekday Additions Bar.

### 2.7 Content Quality (Duration/Seasons)
*   **Business Objective**: Measure content length and series longevity.
*   **User Objective**: Determine if shows are surviving past Season 1.
*   **Layout**: 1 row (Movie focus) + 1 row (TV focus).
*   **Charts**: Movie Duration Histogram, Duration Boxplot, TV Seasons Bar.

### 2.8 Executive Insights
*   **Business Objective**: Translate data into plain-text executive observations.
*   **User Objective**: Read the "so what?" of the data without analyzing charts.
*   **Layout**: Masonry grid of Insight Cards.

### 2.9 Strategic Recommendations
*   **Business Objective**: Provide actionable next steps based on insights.
*   **User Objective**: Make budget/acquisition decisions.
*   **Layout**: Vertical list of Recommendation Cards.

### 2.10 Reports
*   **Business Objective**: Facilitate offline sharing with stakeholders.
*   **Layout**: List view of generated PDF reports with download buttons.

### 2.11 About
*   **Business Objective**: Document project methodology for transparency.
*   **Layout**: Standard markdown rendering panel.

---

## 3. WIREFRAME SPECIFICATIONS

**Global App Shell (Applies to all screens)**
*   **Sidebar (Left)**: Fixed 260px width. Logo top, navigation list center, user profile bottom.
*   **Header (Top)**: Fixed 64px height. Global search left, breadcrumbs center, filters/export right.
*   **Main Content Area**: `calc(100vw - 260px)`. 24px padding all around.
*   **Max Width**: Content is constrained to `1600px` max-width, horizontally centered on ultra-wide monitors.

**Standard Analytics Page Grid**
*   **Row 1 (KPIs)**: 12-column grid divided into 4 columns (span 3 each). Contains KPI Cards.
*   **Row 2 (Primary Charts)**: 12-column grid divided into 2 columns (span 6 each). Contains Chart Containers.
*   **Row 3 (Deep Dive)**: 12-column grid, single column (span 12). Contains full-width Chart Container.

**Mobile Behavior (<768px)**
*   Sidebar hides. Hamburger menu appears in Header.
*   KPI row collapses from 4 columns to 1 column.
*   Chart rows collapse from 2 columns to 1 column.

---

## 4. COMPONENT LIBRARY

**4.1 KPI Card**
*   **Purpose**: Display a single, critical top-line metric.
*   **Variants**: Standard (Text only), Trend (Includes YoY delta), Visual (Includes mini sparkline).
*   **States**: Default (Surface `#141414`), Hover (Surface `#232323`), Loading (Pulsing `#232323`).
*   **Placement**: Top row of any analytics page.

**4.2 Insight Card**
*   **Purpose**: Display a data-backed observation.
*   **Structure**: `[🔍 OBSERVATION]` tag (Info Blue), Title, Context paragraph, small supporting visualization (right-aligned).
*   **Placement**: Executive Insights page.

**4.3 Recommendation Card**
*   **Purpose**: Display a strategic action.
*   **Structure**: `[💡 ACTION]` tag (Success Green), Recommendation Title, Rationale text, Action Button (Primary Red).
*   **Placement**: Strategic Recommendations page.

**4.4 Filter Panel**
*   **Purpose**: Control global dataset parameters.
*   **Components**: Dropdown Multiselects (Year, Genre, Country), Segment Toggle (Movie/TV).
*   **Placement**: Pinned to the top of the Main Content Area, below the Header.

**4.5 Chart Container**
*   **Purpose**: Standardized wrapper for all visual data.
*   **Structure**: 24px padding, Surface `#141414`, 8px border radius. Header contains Title and Export icon. Content contains SVG/Canvas chart.
*   **Interaction**: Hovering over the export icon changes it to White.

**4.6 Loading Skeleton**
*   **Purpose**: Reduce perceived wait time during data fetches.
*   **Style**: Shapes matching the expected component (e.g., a circle for donuts, blocks for bars) with a CSS animation sweeping a lighter gradient left-to-right.

**4.7 Tooltip**
*   **Purpose**: Provide exact data values on chart hover.
*   **Style**: Absolute positioned, Background `#000000`, Text `#FFFFFF`, 4px radius, 8px padding. No arrows.

---

## 5. CHART PLACEMENT BLUEPRINT

*Note: Every chart maps directly to a predefined business question.*

| Page | Chart Name | Order | Size (Grid Span) | Business Question Answered |
| :--- | :--- | :--- | :--- | :--- |
| **Dashboard** | KPI Summary Bar | 1 | 12 (Full) | What is the overall portfolio scale? |
| **Dashboard** | Content Type Donut | 2 | 6 (Half) | Does Netflix focus more on Movies or TV? |
| **Dashboard** | Decade Distribution | 3 | 6 (Half) | How fresh is the catalog? |
| **Portfolio** | Content Type by Year | 1 | 12 (Full) | How has the Movie/TV balance shifted over time? |
| **Expansion** | World Choropleth Map | 1 | 12 (Full) | Which regions are untouched by Netflix production? |
| **Expansion** | Top Countries Bar | 2 | 6 (Half) | Which countries dominate production? |
| **Expansion** | Country Treemap | 3 | 6 (Half) | What is the proportional weight of top regions? |
| **Genre** | Top Genres Bar | 1 | 12 (Full) | What are the most common genres? |
| **Genre** | Genre Sunburst | 2 | 6 (Half) | How do sub-genres breakdown? |
| **Genre** | Genre Heatmap by Year | 3 | 6 (Half) | Which genres are growing recently? |
| **Audience** | Rating Distribution | 1 | 6 (Half) | Which ratings dominate the platform? |
| **Audience** | Rating Heatmap by Year | 2 | 6 (Half) | Is the platform shifting toward mature content? |
| **Trends** | Yearly Additions Line | 1 | 6 (Half) | How fast is the catalog growing? |
| **Trends** | Monthly Additions Heatmap| 2 | 6 (Half) | Are there seasonal trends in content acquisition? |
| **Quality** | Movie Duration Histogram| 1 | 6 (Half) | What is the standard duration of a Netflix movie? |
| **Quality** | TV Seasons Bar | 2 | 6 (Half) | Do Netflix shows survive past Season 1? |

---

## 6. INTERACTION FLOW

*   **Hover Behavior**: Hovering over interactive elements (cards, list items, chart bars) lifts the surface color from `#141414` to `#232323`. It never uses drop shadows.
*   **Chart Cross-Filtering**: Clicking a bar on a chart (e.g., clicking "India" on the Top Countries chart) acts as a temporary filter, fading other bars to 0.3 opacity and updating the page's KPI cards to reflect only Indian content.
*   **Filter Interactions**: Selecting an item from the Filter Panel instantly triggers a data recalculation. A subtle opacity pulse (1.0 -> 0.7 -> 1.0, 200ms) occurs on all charts to confirm the update.
*   **Export Flow**: Clicking the download icon on a Chart Container opens a small dropdown menu: [Download CSV] [Download PNG]. Clicking triggers browser download.
*   **Reset Flow**: The "Reset Filters" button in the Top Nav reverts the dataset to the unfiltered state and removes all active filter chips.

---

## 7. RESPONSIVENESS

*   **Desktop (1440px+)**: Sidebar is fixed at 260px. 4 KPIs per row. Charts sit comfortably side-by-side (2 columns).
*   **Laptop (1024px - 1439px)**: Sidebar fixed at 260px. 4 KPIs per row. Charts remain side-by-side but reduce in height to maintain aspect ratio.
*   **Tablet (768px - 1023px)**: Sidebar shrinks to icon-only mode (64px). Navigation text is hidden. Main content expands. KPIs switch to 2x2 grid. Multi-column charts stack vertically into a single column.
*   **Mobile (<768px)**: Sidebar completely hidden. Accessible via Hamburger menu in header. All components are full-width stacked. Legends on charts move from the right side to the bottom. Tooltips trigger on tap instead of hover.

---

## 8. ENGINEERING HANDOFF

**8.1 Component Inventory (For Frontend Implementation)**
Frontend engineers should build these isolated components first, matching the Design System Tokens:
1.  `<AppShell />` (Manages sidebar, header, routing)
2.  `<KPICard />` (Accepts props: title, metric, trend, sparklineData)
3.  `<ChartContainer />` (Accepts props: title, subtitle, children[svg], exportData)
4.  `<FilterDropdown />` (Accepts props: label, options, multiSelect)
5.  `<InsightCard />` (Accepts props: tagType, title, body, chart)

**8.2 Design Tokens**
Refer to Section 18 of the *Product Design Specification*. Use `#E50914` strictly for active/brand elements. Use `#141414` for all component surfaces.

**8.3 Implementation Order**
1.  **Phase 1**: App Shell & Routing (Sidebar, Header, empty pages).
2.  **Phase 2**: Global State & Filters (Connecting the dataset to the top filter bar).
3.  **Phase 3**: Reusable Components (KPI Cards, Chart Containers).
4.  **Phase 4**: Chart Implementation (Binding data to Plotly/Recharts components).
5.  **Phase 5**: Insights & Recommendations pages (Static layout).
6.  **Phase 6**: Polish (Hover states, transitions, accessibility checks).

**8.4 Risks & Dependencies**
*   **Risk**: Rendering 35 charts simultaneously on the DOM may cause performance lag.
*   **Mitigation**: Implement lazy loading (Intersection Observer) for charts below the fold.
*   **Dependency**: Requires pre-processed data (`netflix_features.csv`). Data processing must run prior to UI mounting.

**8.5 Acceptance Criteria**
*   [ ] Navigation flows exactly as documented in Section 1.
*   [ ] Colors and typography match the Design Tokens precisely.
*   [ ] Filtering the Top Nav correctly cascades data changes down to all charts on the active page.
*   [ ] App maintains functionality and readability down to 320px viewport width.
*   [ ] All interactive elements display a visible hover state.
*   [ ] Tooltips on charts are accessible without getting cut off by `overflow: hidden` boundaries.
