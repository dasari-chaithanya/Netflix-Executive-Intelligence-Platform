# Interview Questions & Answers

Use this guide to prepare for technical and behavioral questions related to this project during interviews.

### 1. "Walk me through your Netflix dashboard project."
**Answer Strategy**: Focus on the *business problem* first, then the *architecture*, then the *outcome*.
"I noticed a lot of data science portfolios just create simple exploratory notebooks. I wanted to build something an executive would actually use. So, I built a full-stack platform. I started with a data pipeline to clean the raw Netflix dataset and convert it to Parquet for speed. Then, I built a KPI engine to define metrics like 'Catalog Freshness.' Finally, I built a Streamlit UI on top with a custom Storytelling Engine that reads those metrics and automatically generates strategic recommendations, like whether to increase investment in Dramas or decrease in Comedies."

### 2. "Why did you use Parquet instead of just loading the CSV?"
**Answer Strategy**: Show you understand performance at scale.
"In my initial testing, loading an 8,800-row CSV took over a second on every rerun. By migrating to a Medallion architecture, I moved the heavy data cleaning offline. The Streamlit app only reads the optimized, columnar Parquet file, wrapped in an `@st.cache_data` decorator. This dropped my I/O latency to near zero and allowed the global filters to feel instantaneous."

### 3. "How did you handle the UI and design?"
**Answer Strategy**: Talk about design systems.
"I didn't want it to look like a generic Streamlit app, so I implemented a centralized `design_tokens.json` file. All colors, spacing, and typography are defined there. I then built a `ThemeProvider` and a `ChartFactory` that injects those tokens into the Plotly charts and Streamlit CSS. This guarantees visual consistency and makes it incredibly easy to maintain or re-brand."

### 4. "What was the hardest part of building this?"
**Answer Strategy**: Highlight architectural complexity.
"Separating the concerns. It's very tempting in Streamlit to put Pandas filtering, KPI math, and UI rendering all in the same file. I forced myself to build a `ViewModel` layer. The UI only talks to the ViewModel. The ViewModel talks to the KPI Engine and the Storytelling Engine. It took more time upfront, but it made writing the `pytest` integration tests much easier."
