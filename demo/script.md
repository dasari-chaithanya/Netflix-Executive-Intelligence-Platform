# Live Demo Video Scripts

These scripts are structured to help you record professional 2-minute and 5-minute video walkthroughs of the dashboard for your portfolio, LinkedIn, and internship applications.

## General Recording Tips
1. Use **OBS Studio** or **ShareX** to record your screen.
2. Hide your bookmarks bar and ensure the browser is in full screen (F11).
3. Switch the theme to "Dark Mode" before starting, as it looks more premium on video.
4. Speak clearly, focusing on *business value* rather than technical code.

---

## 2-Minute Demo (LinkedIn / Quick Pitch)

**[0:00 - 0:15] The Hook & Executive Summary**
*Action*: Start on the Executive Dashboard. Hover over the KPI cards.
*Script*: "Hi, I'm [Your Name], and this is the Netflix Content Strategy Platform. I built this enterprise-grade dashboard to help content executives make data-driven acquisition decisions. Unlike typical notebooks, this is a fully functioning production app with a centralized business rules engine."

**[0:15 - 0:45] Global State & Storytelling**
*Action*: Open the sidebar. Change the Release Year filter to "2015 - 2024" and Content Type to "Movie". Click Apply.
*Script*: "Notice what happens when I filter the data to recent movies. The entire application state updates instantly. The Narrative Engine automatically generates a new Strategic Action Plan, translating raw KPIs into plain-English recommendations based on predefined business thresholds."

**[0:45 - 1:30] Analytics Drill-Down**
*Action*: Navigate to "Global Expansion", hover over the map. Then navigate to "Genre Intelligence".
*Script*: "The platform breaks down the catalog across several dimensions. The Global Expansion view maps production footprints, while Genre Intelligence highlights our core library pillars. Every visualization uses a custom Streamlit component framework I built from scratch, utilizing a centralized design token system."

**[1:30 - 2:00] The Developer Edge & Closing**
*Action*: Navigate to "Developer Tools". Toggle the Feature Flag.
*Script*: "I also built in a Developer Tools panel for monitoring system health and in-memory Parquet performance. If you're looking for a Data Analyst who understands full-stack data product development, I'd love to connect. Check out the GitHub link below!"

---

## 5-Minute Demo (Interview Deep Dive)

*Follow the 2-minute structure, but insert these deep-dives:*

**[Insert at 1:30] The Data Engineering Pipeline**
*Action*: Open your IDE (VS Code) or GitHub repo showing the `src/` folder.
*Script*: "Behind the UI is a robust Medallion architecture ETL pipeline. The raw CSV is cleaned, engineered into features, and exported as a highly optimized Parquet file. I strictly separated the KPI calculation engine from the ViewModels, meaning the UI only handles presentation, never heavy data crunching."

**[Insert at 3:00] Architecture & Reusability**
*Action*: Show the `app/charts/` factory classes.
*Script*: "To ensure maintainability, I didn't hardcode any charts. I built an Object-Oriented Chart Factory. Whether it's a bar chart or a choropleth map, the dashboard pages simply pass a dataframe to the builder, and the factory applies the global CSS theme and Plotly configurations automatically."

**[Insert at 4:30] Testing & QA**
*Action*: Run `pytest` in the terminal.
*Script*: "Finally, no enterprise product is complete without testing. I wrote comprehensive integration tests that validate the ViewModels, filter logic, and the storytelling bounds, ensuring that executive recommendations are mathematically sound before deployment."
