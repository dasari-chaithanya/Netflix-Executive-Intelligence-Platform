"""
visualization.py
================
Reusable, publication-quality plotting functions for the Netflix Content Strategy Analysis project.

Design Principles
-----------------
- Neutral palette with Netflix red used for emphasis only.
- Every chart answers ONE business question.
- Consistent typography, titles, subtitles, and annotations.
- All figures can be saved via utils.save_fig() or utils.save_plotly().
"""

from __future__ import annotations

import logging
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from src.config import (
    NETFLIX_RED, SEQ_PALETTE, DIV_PALETTE, PLOTLY_TEMPLATE,
    FONT_FAMILY, TITLE_SIZE, SUBTITLE_SIZE, LABEL_SIZE, TICK_SIZE,
    FIG_DPI, FIG_SIZE_SM, FIG_SIZE_MD, FIG_SIZE_LG, FIG_SIZE_WIDE,
    GRAY_DARK, GRAY_LIGHT, GRAY_MID, ACCENT_DARK,
)
from src.utils import save_fig, save_plotly

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# GLOBAL MATPLOTLIB STYLE
# ─────────────────────────────────────────────────────────────
def apply_global_style() -> None:
    """Apply a consistent Matplotlib style across all static charts."""
    plt.rcParams.update({
        "figure.facecolor":       "#1A1A1A",
        "axes.facecolor":         "#1A1A1A",
        "axes.edgecolor":         GRAY_DARK,
        "axes.labelcolor":        GRAY_LIGHT,
        "axes.titlesize":         TITLE_SIZE,
        "axes.labelsize":         LABEL_SIZE,
        "xtick.color":            GRAY_MID,
        "ytick.color":            GRAY_MID,
        "xtick.labelsize":        TICK_SIZE,
        "ytick.labelsize":        TICK_SIZE,
        "text.color":             GRAY_LIGHT,
        "font.family":            "sans-serif",
        "font.sans-serif":        ["Arial", "DejaVu Sans"],
        "grid.color":             GRAY_DARK,
        "grid.linestyle":         "--",
        "grid.alpha":             0.4,
        "legend.facecolor":       "#2A2A2A",
        "legend.edgecolor":       GRAY_DARK,
        "legend.fontsize":        TICK_SIZE,
        "figure.dpi":             FIG_DPI,
    })


apply_global_style()


# ─────────────────────────────────────────────────────────────
# HELPER: ANNOTATE BARS
# ─────────────────────────────────────────────────────────────
def _annotate_bars(ax: plt.Axes, fmt: str = "{:.0f}", fontsize: int = 9,
                   color: str = GRAY_LIGHT, ha: str = "center", va: str = "bottom",
                   offset: float = 0.5) -> None:
    """Annotate each bar in a bar chart with its value."""
    for patch in ax.patches:
        width  = patch.get_width()
        height = patch.get_height()
        x      = patch.get_x() + width / 2
        y      = patch.get_y() + height + offset
        ax.annotate(fmt.format(height), (x, y),
                    ha=ha, va=va, fontsize=fontsize, color=color)


def _set_title(ax: plt.Axes, title: str, subtitle: str = "") -> None:
    """Set chart title and optional subtitle in consistent style."""
    ax.set_title(title, fontsize=TITLE_SIZE, fontweight="bold",
                 color=GRAY_LIGHT, pad=12)
    if subtitle:
        ax.text(0.5, 1.01, subtitle, transform=ax.transAxes,
                fontsize=SUBTITLE_SIZE - 2, color=GRAY_MID,
                ha="center", style="italic")


# ─────────────────────────────────────────────────────────────
# OVERVIEW CHARTS (5)
# ─────────────────────────────────────────────────────────────
def plot_content_type_donut(df: pd.DataFrame, save: bool = True):
    """
    [Overview-1] Business Question: How is Netflix content split between Movies and TV Shows?
    Chart: Donut chart of Movies vs TV Shows.
    """
    counts = df["type"].value_counts()
    colors = [NETFLIX_RED, SEQ_PALETTE[0]]
    fig, ax = plt.subplots(figsize=FIG_SIZE_SM)
    wedges, texts, autotexts = ax.pie(
        counts, labels=None, autopct="%1.1f%%",
        startangle=90, colors=colors,
        wedgeprops=dict(width=0.5, edgecolor="#1A1A1A", linewidth=2),
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_fontsize(12)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.legend(counts.index, loc="lower center", ncol=2,
              bbox_to_anchor=(0.5, -0.08), frameon=False,
              labelcolor=GRAY_LIGHT, fontsize=LABEL_SIZE)
    ax.set_title("Content Type Distribution\nMovies vs TV Shows",
                 fontsize=TITLE_SIZE, fontweight="bold", color=GRAY_LIGHT, pad=10)
    centre_text = f"{len(df):,}\nTitles"
    ax.text(0, 0, centre_text, ha="center", va="center",
            fontsize=13, fontweight="bold", color=GRAY_LIGHT)
    fig.tight_layout()
    if save:
        save_fig(fig, "overview", "01_content_type_donut.png")
    return fig


def plot_top_ratings_bar(df: pd.DataFrame, top_n: int = 10, save: bool = True):
    """
    [Overview-2] Business Question: Which content ratings dominate Netflix?
    Chart: Horizontal bar chart of top N ratings.
    """
    data = df["rating"].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=FIG_SIZE_SM)
    bars = ax.barh(data.index[::-1], data.values[::-1],
                   color=SEQ_PALETTE[:top_n][::-1], edgecolor="none", height=0.65)
    for bar, val in zip(bars, data.values[::-1]):
        ax.text(bar.get_width() + 15, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", ha="left", fontsize=10, color=GRAY_LIGHT)
    _set_title(ax, f"Top {top_n} Content Ratings", "Which ratings dominate the catalog?")
    ax.set_xlabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.set_ylabel("")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "overview", "02_top_ratings_bar.png")
    return fig


def plot_content_type_by_year_area(df: pd.DataFrame, save: bool = True):
    """
    [Overview-3] Business Question: How has the Movies/TV Show split changed over time?
    Chart: Stacked area chart of content type added per year.
    """
    yearly = df.dropna(subset=["year_added"]).groupby(["year_added", "type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    yearly.plot.area(ax=ax, color=[NETFLIX_RED, SEQ_PALETTE[0]], alpha=0.8, linewidth=0)
    _set_title(ax, "Content Added per Year by Type", "How has the Movie/Show balance evolved?")
    ax.set_xlabel("Year", fontsize=LABEL_SIZE)
    ax.set_ylabel("Titles Added", fontsize=LABEL_SIZE)
    ax.legend(loc="upper left", frameon=False, labelcolor=GRAY_LIGHT)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "overview", "03_content_type_by_year_area.png")
    return fig


def plot_kpi_summary_bar(kpis: dict, save: bool = True):
    """
    [Overview-4] Business Question: What are the key portfolio metrics at a glance?
    Chart: KPI summary bar (horizontal bars for numeric KPIs).
    """
    numeric_kpis = {k: v for k, v in kpis.items()
                    if isinstance(v, (int, float)) and v is not None
                    and k not in ("Movies", "TV Shows", "Total Titles")}
    if not numeric_kpis:
        logger.warning("No numeric KPIs to plot.")
        return None

    labels = list(numeric_kpis.keys())
    values = list(numeric_kpis.values())

    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    bars = ax.barh(labels, values, color=SEQ_PALETTE[:len(labels)], height=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                f"{val:,.1f}" if isinstance(val, float) else f"{val:,}",
                va="center", ha="left", fontsize=9, color=GRAY_LIGHT)
    _set_title(ax, "Key Business KPIs", "Summary of locked business metrics")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "overview", "04_kpi_summary_bar.png")
    return fig


def plot_decade_distribution(df: pd.DataFrame, save: bool = True):
    """
    [Overview-5] Business Question: Which production eras dominate Netflix's catalog?
    Chart: Bar chart of content by release decade.
    """
    data = df["release_decade"].value_counts().sort_index()
    data = data[data.index != "Unknown"]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    bars = ax.bar(data.index, data.values,
                  color=[NETFLIX_RED if d == "2010s" else SEQ_PALETTE[1] for d in data.index],
                  edgecolor="none")
    _annotate_bars(ax, fmt="{:,.0f}", offset=5)
    _set_title(ax, "Content by Release Decade", "Which era dominates Netflix's catalog?")
    ax.set_xlabel("Decade", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "overview", "05_decade_distribution.png")
    return fig


# ─────────────────────────────────────────────────────────────
# TIMELINE CHARTS (5)
# ─────────────────────────────────────────────────────────────
def plot_yearly_additions_line(df: pd.DataFrame, save: bool = True):
    """
    [Timeline-1] Business Question: How has Netflix's content growth trended year-over-year?
    Chart: Line chart of titles added per year.
    """
    data = df.dropna(subset=["year_added"]).groupby("year_added").size().reset_index(name="count")
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.plot(data["year_added"], data["count"], color=NETFLIX_RED,
            linewidth=2.5, marker="o", markersize=5, zorder=3)
    ax.fill_between(data["year_added"], data["count"], alpha=0.15, color=NETFLIX_RED)
    _set_title(ax, "Netflix Content Added per Year", "Year-over-year growth of the catalog")
    ax.set_xlabel("Year Added", fontsize=LABEL_SIZE)
    ax.set_ylabel("Titles Added", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    if save:
        save_fig(fig, "timeline", "01_yearly_additions_line.png")
    return fig


def plot_monthly_heatmap(df: pd.DataFrame, save: bool = True):
    """
    [Timeline-2] Business Question: Which months and years see the most content additions?
    Chart: Heatmap of content added by year × month.
    """
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    pivot = (df.dropna(subset=["year_added","month_added"])
               .groupby(["year_added","month_added"])
               .size()
               .unstack(fill_value=0))
    pivot = pivot.reindex(columns=month_order, fill_value=0)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.3,
                linecolor="#1A1A1A", annot=False,
                cbar_kws={"label": "Titles Added", "shrink": 0.6})
    _set_title(ax, "Content Additions: Year × Month Heatmap",
               "When does Netflix add the most content?")
    ax.set_xlabel("Month", fontsize=LABEL_SIZE)
    ax.set_ylabel("Year", fontsize=LABEL_SIZE)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    if save:
        save_fig(fig, "timeline", "02_monthly_heatmap.png")
    return fig


def plot_cumulative_growth(df: pd.DataFrame, save: bool = True):
    """
    [Timeline-3] Business Question: What does Netflix's cumulative catalog size look like?
    Chart: Cumulative area chart split by type.
    """
    data = (df.dropna(subset=["year_added"])
              .groupby(["year_added","type"])
              .size()
              .unstack(fill_value=0)
              .cumsum())
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    data.plot.area(ax=ax, color=[NETFLIX_RED, SEQ_PALETTE[0]], alpha=0.75, linewidth=0)
    _set_title(ax, "Cumulative Netflix Content Growth", "Total catalog size over time")
    ax.set_xlabel("Year", fontsize=LABEL_SIZE)
    ax.set_ylabel("Cumulative Titles", fontsize=LABEL_SIZE)
    ax.legend(loc="upper left", frameon=False, labelcolor=GRAY_LIGHT)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "timeline", "03_cumulative_growth.png")
    return fig


def plot_yoy_growth_rate(df: pd.DataFrame, save: bool = True):
    """
    [Timeline-4] Business Question: How fast is Netflix growing year-over-year?
    Chart: Bar chart of YoY % growth rate.
    """
    yearly = df.dropna(subset=["year_added"]).groupby("year_added").size()
    yoy = yearly.pct_change() * 100
    yoy = yoy.dropna()
    colors = [NETFLIX_RED if v < 0 else SEQ_PALETTE[1] for v in yoy.values]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.bar(yoy.index, yoy.values, color=colors, edgecolor="none")
    ax.axhline(0, color=GRAY_MID, linewidth=1, linestyle="--")
    _set_title(ax, "Year-over-Year Content Growth Rate (%)",
               "How fast has the catalog been expanding?")
    ax.set_xlabel("Year", fontsize=LABEL_SIZE)
    ax.set_ylabel("Growth Rate (%)", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "timeline", "04_yoy_growth_rate.png")
    return fig


def plot_weekday_additions(df: pd.DataFrame, save: bool = True):
    """
    [Timeline-5] Business Question: On which day of the week does Netflix add the most content?
    Chart: Bar chart of additions by weekday.
    """
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    data  = df["weekday_added"].value_counts().reindex(order, fill_value=0)
    fig, ax = plt.subplots(figsize=FIG_SIZE_SM)
    bars = ax.bar(data.index, data.values,
                  color=[NETFLIX_RED if d == "Friday" else SEQ_PALETTE[1] for d in data.index])
    _annotate_bars(ax, fmt="{:,.0f}", offset=5)
    _set_title(ax, "Content Additions by Weekday", "Does Netflix prefer a specific day to add content?")
    ax.set_xlabel("Day of Week", fontsize=LABEL_SIZE)
    ax.set_ylabel("Titles Added", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "timeline", "05_weekday_additions.png")
    return fig


# ─────────────────────────────────────────────────────────────
# COUNTRY CHARTS (5)
# ─────────────────────────────────────────────────────────────
def plot_top_countries_bar(df: pd.DataFrame, top_n: int = 15, save: bool = True):
    """
    [Country-1] Business Question: Which countries produce the most Netflix content?
    Chart: Horizontal bar chart of top N producing countries.
    """
    data = (df["country"].dropna()
              .str.split(",").explode().str.strip()
              .value_counts()
              .drop("Unknown", errors="ignore")
              .head(top_n))
    colors = [NETFLIX_RED] + [SEQ_PALETTE[i % len(SEQ_PALETTE)] for i in range(1, top_n)]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.barh(data.index[::-1], data.values[::-1], color=colors[::-1], height=0.7)
    for i, (val, name) in enumerate(zip(data.values[::-1], data.index[::-1])):
        ax.text(val + 10, i, f"{val:,}", va="center", fontsize=9, color=GRAY_LIGHT)
    _set_title(ax, f"Top {top_n} Content-Producing Countries",
               "Which countries dominate Netflix's catalog?")
    ax.set_xlabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "country", "01_top_countries_bar.png")
    return fig


def plot_country_treemap(df: pd.DataFrame, top_n: int = 20, save: bool = True):
    """
    [Country-2] Business Question: How does country-level production compare proportionally?
    Chart: Plotly treemap.
    """
    data = (df["country"].dropna()
              .str.split(",").explode().str.strip()
              .value_counts()
              .drop("Unknown", errors="ignore")
              .head(top_n)
              .reset_index())
    data.columns = ["country", "count"]
    fig = px.treemap(data, path=["country"], values="count",
                     color="count", color_continuous_scale="Reds",
                     template=PLOTLY_TEMPLATE)
    fig.update_layout(title=dict(text="Country-Level Production Treemap",
                                  font=dict(size=TITLE_SIZE)),
                      margin=dict(t=50, l=10, r=10, b=10))
    fig.update_traces(textinfo="label+value+percent root")
    if save:
        save_plotly(fig, "country", "02_country_treemap.png")
    return fig


def plot_country_content_type_stacked(df: pd.DataFrame, top_n: int = 10, save: bool = True):
    """
    [Country-3] Business Question: Do top countries skew toward Movies or TV Shows?
    Chart: Stacked horizontal bar.
    """
    exploded = df.copy()
    exploded["country"] = exploded["country"].str.split(",")
    exploded = exploded.explode("country")
    exploded["country"] = exploded["country"].str.strip()
    top = (exploded[exploded["country"] != "Unknown"]
           .groupby("country").size()
           .nlargest(top_n).index)
    pivot = (exploded[exploded["country"].isin(top)]
             .groupby(["country","type"]).size()
             .unstack(fill_value=0))
    pivot = pivot.loc[top[::-1]]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    pivot.plot.barh(ax=ax, color=[NETFLIX_RED, SEQ_PALETTE[0]],
                    stacked=True, width=0.7, edgecolor="none")
    _set_title(ax, "Movies vs TV Shows by Country (Top 10)",
               "Do countries specialize in Movies or TV Shows?")
    ax.set_xlabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.set_ylabel("")
    ax.legend(loc="lower right", frameon=False, labelcolor=GRAY_LIGHT)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "country", "03_country_type_stacked.png")
    return fig


def plot_country_diversity_bar(df: pd.DataFrame, save: bool = True):
    """
    [Country-4] Business Question: How has country diversity on Netflix changed over time?
    Chart: Bar chart of unique countries per year_added.
    """
    def _unique_countries(series):
        return (series.dropna()
                .str.split(",").explode().str.strip()
                .replace("Unknown","").replace("", pd.NA)
                .dropna().nunique())

    data = (df.dropna(subset=["year_added"])
              .groupby("year_added")["country"]
              .apply(_unique_countries)
              .reset_index(name="unique_countries"))
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.bar(data["year_added"], data["unique_countries"],
           color=SEQ_PALETTE[2], edgecolor="none")
    ax.plot(data["year_added"], data["unique_countries"],
            color=NETFLIX_RED, linewidth=2, marker="o", markersize=4)
    _set_title(ax, "Country Diversity per Year",
               "Is Netflix expanding to more countries over time?")
    ax.set_xlabel("Year Added", fontsize=LABEL_SIZE)
    ax.set_ylabel("Unique Countries", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "country", "04_country_diversity_bar.png")
    return fig


def plot_choropleth_map(df: pd.DataFrame, save: bool = True):
    """
    [Country-5] Business Question: Where in the world is Netflix content produced?
    Chart: Plotly choropleth world map.
    """
    data = (df["country"].dropna()
              .str.split(",").explode().str.strip()
              .value_counts()
              .drop("Unknown", errors="ignore")
              .reset_index())
    data.columns = ["country", "count"]
    fig = px.choropleth(data, locations="country", locationmode="country names",
                        color="count", hover_name="country",
                        color_continuous_scale="Reds",
                        template=PLOTLY_TEMPLATE,
                        title="Global Netflix Content Production")
    fig.update_layout(
        title=dict(font=dict(size=TITLE_SIZE)),
        geo=dict(showframe=False, showcoastlines=True,
                 coastlinecolor=GRAY_DARK, bgcolor="#1A1A1A"),
        margin=dict(t=50, l=0, r=0, b=0),
    )
    if save:
        save_plotly(fig, "country", "05_choropleth_map.png")
    return fig


# ─────────────────────────────────────────────────────────────
# GENRE CHARTS (5)
# ─────────────────────────────────────────────────────────────
def plot_top_genres_bar(df: pd.DataFrame, top_n: int = 15, save: bool = True):
    """
    [Genre-1] Business Question: Which genres dominate Netflix's catalog?
    Chart: Horizontal bar chart of top N genres.
    """
    data = (df["genres"].explode().str.strip()
              .value_counts().head(top_n))
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.barh(data.index[::-1], data.values[::-1],
            color=SEQ_PALETTE[:top_n][::-1], height=0.7)
    for i, val in enumerate(data.values[::-1]):
        ax.text(val + 5, i, f"{val:,}", va="center", fontsize=9, color=GRAY_LIGHT)
    _set_title(ax, f"Top {top_n} Genres on Netflix", "Which genres dominate the catalog?")
    ax.set_xlabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "genre", "01_top_genres_bar.png")
    return fig


def plot_genre_treemap(df: pd.DataFrame, top_n: int = 25, save: bool = True):
    """
    [Genre-2] Business Question: How do genres compare proportionally?
    Chart: Plotly treemap.
    """
    data = (df["genres"].explode().str.strip()
              .value_counts().head(top_n)
              .reset_index())
    data.columns = ["genre", "count"]
    fig = px.treemap(data, path=["genre"], values="count",
                     color="count", color_continuous_scale="RdBu",
                     template=PLOTLY_TEMPLATE)
    fig.update_layout(title=dict(text="Genre Distribution Treemap",
                                  font=dict(size=TITLE_SIZE)),
                      margin=dict(t=50,l=5,r=5,b=5))
    if save:
        save_plotly(fig, "genre", "02_genre_treemap.png")
    return fig


def plot_genre_sunburst(df: pd.DataFrame, top_n: int = 15, save: bool = True):
    """
    [Genre-3] Business Question: How are genres distributed across Movies and TV Shows?
    Chart: Plotly sunburst (type → genre).
    """
    exploded = df.explode("genres").dropna(subset=["genres"])
    top_genres = exploded["genres"].str.strip().value_counts().head(top_n).index
    filtered = exploded[exploded["genres"].isin(top_genres)]
    data = filtered.groupby(["type", "genres"]).size().reset_index(name="count")
    fig = px.sunburst(data, path=["type", "genres"], values="count",
                      color_discrete_sequence=[NETFLIX_RED] + SEQ_PALETTE,
                      template=PLOTLY_TEMPLATE)
    fig.update_layout(title=dict(text="Genre Distribution by Content Type",
                                  font=dict(size=TITLE_SIZE)),
                      margin=dict(t=50,l=5,r=5,b=5))
    if save:
        save_plotly(fig, "genre", "03_genre_sunburst.png")
    return fig


def plot_genre_by_type_bar(df: pd.DataFrame, top_n: int = 12, save: bool = True):
    """
    [Genre-4] Business Question: Which genres lean toward Movies vs TV Shows?
    Chart: Grouped bar chart.
    """
    exploded = df.explode("genres")
    exploded["genres"] = exploded["genres"].str.strip()
    top = exploded["genres"].value_counts().head(top_n).index
    pivot = (exploded[exploded["genres"].isin(top)]
             .groupby(["genres","type"]).size()
             .unstack(fill_value=0))
    pivot = pivot.loc[top]
    fig, ax = plt.subplots(figsize=FIG_SIZE_LG)
    pivot.plot.bar(ax=ax, color=[NETFLIX_RED, SEQ_PALETTE[0]],
                   width=0.7, edgecolor="none")
    _set_title(ax, "Top Genres: Movies vs TV Shows",
               "Which genres are Movie-heavy vs TV Show-heavy?")
    ax.set_xlabel("")
    ax.set_ylabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.legend(frameon=False, labelcolor=GRAY_LIGHT)
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=35, ha="right")
    fig.tight_layout()
    if save:
        save_fig(fig, "genre", "04_genre_by_type_bar.png")
    return fig


def plot_genre_heatmap(df: pd.DataFrame, top_n: int = 12, save: bool = True):
    """
    [Genre-5] Business Question: How has genre popularity changed over the years?
    Chart: Heatmap of genre × year.
    """
    exploded = df.dropna(subset=["year_added"]).explode("genres")
    exploded["genres"] = exploded["genres"].str.strip()
    top = exploded["genres"].value_counts().head(top_n).index
    pivot = (exploded[exploded["genres"].isin(top)]
             .groupby(["genres","year_added"]).size()
             .unstack(fill_value=0))
    pivot = pivot.loc[top]
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.3,
                linecolor="#1A1A1A", annot=False,
                cbar_kws={"label": "Titles", "shrink": 0.5})
    _set_title(ax, "Genre Popularity Over Time (Heatmap)",
               "Which genres are gaining or losing momentum?")
    ax.set_xlabel("Year Added", fontsize=LABEL_SIZE)
    ax.set_ylabel("Genre", fontsize=LABEL_SIZE)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    if save:
        save_fig(fig, "genre", "05_genre_heatmap.png")
    return fig


# ─────────────────────────────────────────────────────────────
# RATINGS CHARTS (4)
# ─────────────────────────────────────────────────────────────
def plot_rating_distribution_bar(df: pd.DataFrame, save: bool = True):
    """
    [Ratings-1] Business Question: What is the overall rating distribution?
    Chart: Vertical bar chart.
    """
    data = df["rating"].value_counts()
    colors = [NETFLIX_RED if r == "TV-MA" else SEQ_PALETTE[i % len(SEQ_PALETTE)]
              for i, r in enumerate(data.index)]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    bars = ax.bar(data.index, data.values, color=colors, edgecolor="none")
    _annotate_bars(ax, fmt="{:,.0f}", offset=5)
    _set_title(ax, "Content Rating Distribution", "Which rating is most common on Netflix?")
    ax.set_xlabel("Rating", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=30)
    fig.tight_layout()
    if save:
        save_fig(fig, "ratings", "01_rating_distribution_bar.png")
    return fig


def plot_rating_by_type_grouped(df: pd.DataFrame, save: bool = True):
    """
    [Ratings-2] Business Question: Do Movies and TV Shows differ in their rating profiles?
    Chart: Grouped bar chart.
    """
    top_ratings = df["rating"].value_counts().head(8).index
    pivot = (df[df["rating"].isin(top_ratings)]
             .groupby(["rating","type"]).size()
             .unstack(fill_value=0))
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    pivot.plot.bar(ax=ax, color=[NETFLIX_RED, SEQ_PALETTE[0]],
                   width=0.7, edgecolor="none")
    _set_title(ax, "Ratings by Content Type",
               "Do Movies and TV Shows have different rating profiles?")
    ax.set_xlabel("Rating", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.legend(frameon=False, labelcolor=GRAY_LIGHT)
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=30)
    fig.tight_layout()
    if save:
        save_fig(fig, "ratings", "02_rating_by_type_grouped.png")
    return fig


def plot_rating_pie(df: pd.DataFrame, save: bool = True):
    """
    [Ratings-3] Business Question: How does audience targeting break down by rating group?
    Chart: Pie chart of rating groups (Kids/Family/Teen/Mature/Unrated).
    """
    from src.config import RATING_GROUPS
    def _group(r):
        for group, ratings in RATING_GROUPS.items():
            if r in ratings:
                return group
        return "Other"

    df = df.copy()
    df["rating_group"] = df["rating"].apply(_group)
    data = df["rating_group"].value_counts()
    colors = [NETFLIX_RED, SEQ_PALETTE[0], SEQ_PALETTE[2], SEQ_PALETTE[4], GRAY_MID]
    fig, ax = plt.subplots(figsize=FIG_SIZE_SM)
    wedges, texts, autotexts = ax.pie(
        data, labels=data.index, autopct="%1.1f%%",
        startangle=90, colors=colors[:len(data)],
        wedgeprops=dict(edgecolor="#1A1A1A", linewidth=1.5),
    )
    for t in texts:
        t.set_color(GRAY_LIGHT)
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(10)
    _set_title(ax, "Audience Targeting by Rating Group",
               "Is Netflix primarily targeting mature audiences?")
    fig.tight_layout()
    if save:
        save_fig(fig, "ratings", "03_rating_pie.png")
    return fig


def plot_rating_heatmap_by_year(df: pd.DataFrame, save: bool = True):
    """
    [Ratings-4] Business Question: How has rating distribution changed year over year?
    Chart: Heatmap of rating × year.
    """
    top_ratings = df["rating"].value_counts().head(8).index
    pivot = (df[df["rating"].isin(top_ratings)].dropna(subset=["year_added"])
             .groupby(["rating","year_added"]).size()
             .unstack(fill_value=0))
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.3,
                linecolor="#1A1A1A",
                cbar_kws={"label": "Titles", "shrink": 0.5})
    _set_title(ax, "Rating Distribution Over Years",
               "Which ratings have grown as Netflix expanded?")
    ax.set_xlabel("Year Added", fontsize=LABEL_SIZE)
    ax.set_ylabel("Rating", fontsize=LABEL_SIZE)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    if save:
        save_fig(fig, "ratings", "04_rating_heatmap_by_year.png")
    return fig


# ─────────────────────────────────────────────────────────────
# DURATION CHARTS (3)
# ─────────────────────────────────────────────────────────────
def plot_movie_duration_histogram(df: pd.DataFrame, save: bool = True):
    """
    [Duration-1] Business Question: What is the typical length of a Netflix movie?
    Chart: Histogram with KDE overlay.
    """
    movies = df[(df["type"] == "Movie") & df["duration_minutes"].notna()]["duration_minutes"]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.hist(movies, bins=40, color=SEQ_PALETTE[1], edgecolor="#1A1A1A", alpha=0.8)
    mean_dur = movies.mean()
    ax.axvline(mean_dur, color=NETFLIX_RED, linewidth=2, linestyle="--",
               label=f"Mean: {mean_dur:.0f} min")
    ax.legend(frameon=False, labelcolor=GRAY_LIGHT)
    _set_title(ax, "Movie Duration Distribution (Minutes)",
               "What is the typical length of a Netflix movie?")
    ax.set_xlabel("Duration (minutes)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Movies", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "duration", "01_movie_duration_histogram.png")
    return fig


def plot_duration_boxplot(df: pd.DataFrame, save: bool = True):
    """
    [Duration-2] Business Question: Are there significant outliers in movie durations?
    Chart: Boxplot of movie duration by decade.
    """
    movies = df[(df["type"] == "Movie") & df["duration_minutes"].notna()
                & (df["release_decade"] != "Unknown")].copy()
    fig, ax = plt.subplots(figsize=FIG_SIZE_LG)
    decades = sorted(movies["release_decade"].unique())
    data_by_decade = [movies[movies["release_decade"] == d]["duration_minutes"].values
                      for d in decades]
    bp = ax.boxplot(data_by_decade, labels=decades, patch_artist=True,
                    medianprops=dict(color=NETFLIX_RED, linewidth=2))
    for patch, color in zip(bp["boxes"], SEQ_PALETTE * 5):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    _set_title(ax, "Movie Duration by Decade (Boxplot)",
               "Have movie lengths changed over the decades?")
    ax.set_xlabel("Release Decade", fontsize=LABEL_SIZE)
    ax.set_ylabel("Duration (minutes)", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "duration", "02_duration_boxplot.png")
    return fig


def plot_tv_seasons_bar(df: pd.DataFrame, save: bool = True):
    """
    [Duration-3] Business Question: How many seasons do Netflix TV shows typically run?
    Chart: Bar chart of season count distribution.
    """
    shows = df[(df["type"] == "TV Show") & df["duration_seasons"].notna()]
    data = shows["duration_seasons"].value_counts().sort_index()
    data = data[data.index <= 15]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.bar(data.index.astype(str), data.values,
           color=[NETFLIX_RED if i == 1 else SEQ_PALETTE[1] for i in data.index])
    _set_title(ax, "TV Show Season Count Distribution",
               "Most Netflix shows run for how many seasons?")
    ax.set_xlabel("Number of Seasons", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of TV Shows", fontsize=LABEL_SIZE)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "duration", "03_tv_seasons_bar.png")
    return fig


# ─────────────────────────────────────────────────────────────
# DIRECTOR CHARTS (2)
# ─────────────────────────────────────────────────────────────
def plot_top_directors_bar(df: pd.DataFrame, top_n: int = 15, save: bool = True):
    """
    [Directors-1] Business Question: Which directors contribute the most titles to Netflix?
    Chart: Horizontal bar chart.
    """
    data = (df[df["director"] != "Unknown Director"]["director"]
              .str.split(",").explode().str.strip()
              .value_counts().head(top_n))
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.barh(data.index[::-1], data.values[::-1],
            color=SEQ_PALETTE[:top_n][::-1], height=0.7)
    for i, val in enumerate(data.values[::-1]):
        ax.text(val + 0.1, i, f"{val}", va="center", fontsize=9, color=GRAY_LIGHT)
    _set_title(ax, f"Top {top_n} Most Prolific Directors",
               "Which directors have contributed the most titles?")
    ax.set_xlabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top","right","bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "directors", "01_top_directors_bar.png")
    return fig


def plot_director_content_type_bubble(df: pd.DataFrame, top_n: int = 15, save: bool = True):
    """
    [Directors-2] Business Question: Do top directors specialize in Movies or TV Shows?
    Chart: Bubble chart (director × type × count).
    """
    exploded = df[df["director"] != "Unknown Director"].copy()
    exploded["director"] = exploded["director"].str.split(",")
    exploded = exploded.explode("director")
    exploded["director"] = exploded["director"].str.strip()
    top = exploded["director"].value_counts().head(top_n).index
    data = (exploded[exploded["director"].isin(top)]
            .groupby(["director","type"]).size()
            .reset_index(name="count"))
    fig = px.scatter(data, x="director", y="type", size="count",
                     color="type", size_max=40,
                     color_discrete_map={"Movie": NETFLIX_RED, "TV Show": SEQ_PALETTE[0]},
                     template=PLOTLY_TEMPLATE)
    fig.update_layout(title=dict(text=f"Top {top_n} Directors: Movies vs TV Shows",
                                  font=dict(size=TITLE_SIZE)),
                      xaxis_tickangle=-45,
                      margin=dict(t=60, b=120))
    if save:
        save_plotly(fig, "directors", "02_director_type_bubble.png")
    return fig


# ─────────────────────────────────────────────────────────────
# CAST CHARTS (2)
# ─────────────────────────────────────────────────────────────
def plot_top_actors_bar(df: pd.DataFrame, top_n: int = 20, save: bool = True):
    """
    [Cast-1] Business Question: Which actors appear most frequently on Netflix?
    Chart: Horizontal bar chart.
    """
    data = (df[df["cast"] != "Unknown Cast"]["cast"]
              .str.split(",").explode().str.strip()
              .value_counts().head(top_n))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(data.index[::-1], data.values[::-1],
            color=SEQ_PALETTE[:top_n][::-1], height=0.7)
    for i, val in enumerate(data.values[::-1]):
        ax.text(val + 0.1, i, f"{val}", va="center", fontsize=9, color=GRAY_LIGHT)
    _set_title(ax, f"Top {top_n} Most Frequent Actors",
               "Which actors appear most frequently on Netflix?")
    ax.set_xlabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top","right","bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "cast", "01_top_actors_bar.png")
    return fig


def plot_cast_count_distribution(df: pd.DataFrame, save: bool = True):
    """
    [Cast-2] Business Question: How large are typical Netflix casts?
    Chart: Histogram of cast_count.
    """
    data = df[df["cast_count"] > 0]["cast_count"]
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    ax.hist(data, bins=30, color=SEQ_PALETTE[2], edgecolor="#1A1A1A", alpha=0.8)
    mean_cast = data.mean()
    ax.axvline(mean_cast, color=NETFLIX_RED, linewidth=2, linestyle="--",
               label=f"Mean: {mean_cast:.1f} actors")
    ax.legend(frameon=False, labelcolor=GRAY_LIGHT)
    _set_title(ax, "Cast Size Distribution", "How large are typical Netflix casts?")
    ax.set_xlabel("Number of Cast Members", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "cast", "02_cast_count_distribution.png")
    return fig


# ─────────────────────────────────────────────────────────────
# MISSING VALUE CHARTS (2)
# ─────────────────────────────────────────────────────────────
def plot_missing_value_heatmap(df_raw: pd.DataFrame, save: bool = True):
    """
    [Missing-1] Business Question: Where are the data quality gaps in the raw dataset?
    Chart: Missing value heatmap (columns × sample rows).
    """
    sample = df_raw.sample(min(500, len(df_raw)), random_state=42).isnull()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(sample.T, ax=ax, cbar=False, yticklabels=True,
                cmap=["#2A2A2A", NETFLIX_RED])
    _set_title(ax, "Missing Value Heatmap (Sample of 500 Rows)",
               "Which columns have the most missing data?")
    ax.set_xlabel("Sample Rows", fontsize=LABEL_SIZE)
    ax.set_ylabel("Column", fontsize=LABEL_SIZE)
    fig.tight_layout()
    if save:
        save_fig(fig, "missing", "01_missing_value_heatmap.png")
    return fig


def plot_missing_value_bar(df_raw: pd.DataFrame, save: bool = True):
    """
    [Missing-2] Business Question: What percentage of each column is missing?
    Chart: Horizontal bar chart of missing % per column.
    """
    missing_pct = (df_raw.isnull().sum() / len(df_raw) * 100).sort_values(ascending=False)
    missing_pct = missing_pct[missing_pct > 0]
    fig, ax = plt.subplots(figsize=FIG_SIZE_SM)
    ax.barh(missing_pct.index[::-1], missing_pct.values[::-1],
            color=[NETFLIX_RED if p > 20 else SEQ_PALETTE[2] for p in missing_pct.values[::-1]],
            height=0.6)
    for i, val in enumerate(missing_pct.values[::-1]):
        ax.text(val + 0.3, i, f"{val:.1f}%", va="center", fontsize=9, color=GRAY_LIGHT)
    _set_title(ax, "Missing Data by Column (%)", "Which columns have data quality issues?")
    ax.set_xlabel("Missing %", fontsize=LABEL_SIZE)
    ax.spines[["top","right","bottom"]].set_visible(False)
    ax.xaxis.set_visible(False)
    fig.tight_layout()
    if save:
        save_fig(fig, "missing", "02_missing_value_bar.png")
    return fig


# ─────────────────────────────────────────────────────────────
# FEATURE ENGINEERING CHARTS (2)
# ─────────────────────────────────────────────────────────────
def plot_duration_category_dist(df: pd.DataFrame, save: bool = True):
    """
    [Features-1] Business Question: How do movies cluster by duration category?
    Chart: Bar chart of duration_category.
    """
    movies = df[df["type"] == "Movie"]["duration_category"].dropna().value_counts()
    fig, ax = plt.subplots(figsize=FIG_SIZE_SM)
    bars = ax.bar(movies.index, movies.values,
                  color=SEQ_PALETTE[:len(movies)], edgecolor="none")
    _annotate_bars(ax, fmt="{:,.0f}", offset=5)
    _set_title(ax, "Movie Duration Category Distribution",
               "How do movies cluster by runtime category?")
    ax.set_xlabel("Duration Category", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Movies", fontsize=LABEL_SIZE)
    ax.spines[["top","right"]].set_visible(False)
    plt.xticks(rotation=15, ha="right")
    fig.tight_layout()
    if save:
        save_fig(fig, "features", "01_duration_category_dist.png")
    return fig


def plot_release_decade_by_type(df: pd.DataFrame, save: bool = True):
    """
    [Features-2] Business Question: How does content type vary across release decades?
    Chart: Grouped bar chart of release_decade × type.
    """
    filtered = df[df["release_decade"] != "Unknown"]
    pivot = filtered.groupby(["release_decade","type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=FIG_SIZE_MD)
    pivot.plot.bar(ax=ax, color=[NETFLIX_RED, SEQ_PALETTE[0]],
                   width=0.7, edgecolor="none")
    _set_title(ax, "Content Type by Release Decade",
               "How has the Movie/TV Show split changed by era?")
    ax.set_xlabel("Release Decade", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number of Titles", fontsize=LABEL_SIZE)
    ax.legend(frameon=False, labelcolor=GRAY_LIGHT)
    ax.spines[["top","right"]].set_visible(False)
    plt.xticks(rotation=0)
    fig.tight_layout()
    if save:
        save_fig(fig, "features", "02_release_decade_by_type.png")
    return fig
