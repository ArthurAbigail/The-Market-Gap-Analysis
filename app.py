
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

st.set_page_config(
    page_title="Sugar Trap | Market Gap Analysis",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df  = pd.read_parquet("cleaned_food_data.parquet")
    opp = pd.read_parquet("opportunity_scores.parquet")
    return df, opp

df, opportunity_df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Helix_nebula_symbol.svg/240px-Helix_nebula_symbol.svg.png",
    width=60
)
st.sidebar.title("Filters")
st.sidebar.markdown("Adjust filters to explore the data across all charts.")
st.sidebar.markdown("---")

all_cats = sorted(df["primary_category"].unique())
selected_cats = st.sidebar.multiselect(
    "Product Category", all_cats, default=all_cats
)
sugar_max   = st.sidebar.slider("Max Sugar (g per 100g)",   0, 100, 100)
protein_min = st.sidebar.slider("Min Protein (g per 100g)", 0,  50,   0)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: Open Food Facts | 500,000 products analysed"
)

fdf = df[
    df["primary_category"].isin(selected_cats) &
    (df["sugars_100g"]   <= sugar_max) &
    (df["proteins_100g"] >= protein_min)
]

# Header 
st.title("Sugar Trap — Snack Market Gap Analysis")
st.markdown(
    "**Client:** Helix CPG Partners &nbsp;·&nbsp; "
    "**Dataset:** Open Food Facts (500,000 products) &nbsp;·&nbsp; "
    "**Question:** Where is the Blue Ocean in the snack aisle?"
)
st.markdown("---")

#  KPI Row 
k1, k2, k3, k4 = st.columns(4)
blue_ocean_products = fdf[
    (fdf["proteins_100g"] > 10) & (fdf["sugars_100g"] < 5)
]
k1.metric("Products Analysed",       f"{len(fdf):,}")
k2.metric("Avg Sugar (g/100g)",      f"{fdf['sugars_100g'].mean():.1f}g")
k3.metric("Avg Protein (g/100g)",    f"{fdf['proteins_100g'].mean():.1f}g")
k4.metric("Blue Ocean Products",     f"{len(blue_ocean_products):,}",
          help="High Protein (>10g) AND Low Sugar (<5g) per 100g")
st.markdown("---")


# STORY 3 — NUTRIENT MATRIX VISUALIZATION
# Scatter plot: Sugar (X) vs Protein (Y), coloured by category.
# The empty top-left quadrant is the Blue Ocean opportunity.

st.subheader("Story 3 — Nutrient Matrix Visualization")
st.caption(
    "Each dot represents one product. The green zone (top-left) is the "
    "Blue Ocean — high protein and low sugar — where almost no products "
    "currently exist. Use the sidebar to filter by category."
)

plot_df = fdf.sample(min(5000, len(fdf)), random_state=42) if len(fdf) > 5000 else fdf

fig_scatter = px.scatter(
    plot_df,
    x="sugars_100g",
    y="proteins_100g",
    color="primary_category",
    hover_name="product_name",
    opacity=0.5,
    labels={
        "sugars_100g":      "Sugar (g per 100g)",
        "proteins_100g":    "Protein (g per 100g)",
        "primary_category": "Category",
    },
    title="Nutrient Matrix Visualization — Sugar vs Protein by Snack Category",
    height=540,
)

max_prot = float(fdf["proteins_100g"].max())

fig_scatter.add_shape(
    type="rect", x0=0, x1=5, y0=10, y1=max_prot + 2,
    fillcolor="rgba(30,180,120,0.10)",
    line=dict(color="rgba(30,180,120,0.6)", width=1.5)
)
fig_scatter.add_annotation(
    x=2.5, y=max_prot + 1,
    text="Blue Ocean: High Protein + Low Sugar (Empty Quadrant)",
    showarrow=False, font=dict(size=11, color="#1a7a4a")
)
fig_scatter.add_vline(
    x=5, line_dash="dash", line_color="#aaaaaa",
    annotation_text="Sugar cut-off (5g)",
    annotation_position="top right"
)
fig_scatter.add_hline(
    y=10, line_dash="dash", line_color="#aaaaaa",
    annotation_text="Protein cut-off (10g)",
    annotation_position="top right"
)
fig_scatter.update_layout(
    legend_title_text="Category",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=12),
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.markdown("---")

# CANDIDATE'S CHOICE — MARKET OPPORTUNITY SCORE LEADERBOARD
# Why I built this:
# A scatter plot shows where the gap is but a client needs to know
# WHICH category to enter. This scoring model ranks every category
# on a 0-100 scale using four weighted signals, giving the R&D team
# one clear, defensible answer without interpreting multiple charts.
# Weights: Protein (35%) | Low Sugar (30%) | Fiber (20%) | Low Competition (15%)

st.subheader("Candidate's Choice — Market Opportunity Score Leaderboard")
st.info(
    "**Why I built this:** A scatter plot shows where the gap is, but a "
    "client needs to know which category to enter first. This leaderboard "
    "turns four data signals into one ranked score per category — giving "
    "the R&D team a single, defensible answer they can take to the boardroom. "
    "\n\n**Score weights:** Protein signal (35%) · Low Sugar signal (30%) · "
    "Fiber signal (20%) · Low Competition (15%)"
)

fopp = opportunity_df[
    opportunity_df["primary_category"].isin(selected_cats)
].copy()

fig_opp = px.bar(
    fopp.sort_values("opportunity_score"),
    x="opportunity_score",
    y="primary_category",
    orientation="h",
    color="opportunity_score",
    color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
    text="opportunity_score",
    hover_data={
        "total_products":   True,
        "avg_protein":      ":.1f",
        "avg_sugar":        ":.1f",
        "blue_ocean_count": True,
    },
    labels={
        "opportunity_score":  "Opportunity Score (0–100)",
        "primary_category":   "Category",
        "total_products":     "Total Products",
        "avg_protein":        "Avg Protein (g)",
        "avg_sugar":          "Avg Sugar (g)",
        "blue_ocean_count":   "Blue Ocean Products",
    },
    title="Market Opportunity Score — Which Category Has the Biggest Gap?",
    height=420,
)
fig_opp.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig_opp.update_layout(
    coloraxis_showscale=False,
    yaxis_title="",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=12),
)
st.plotly_chart(fig_opp, use_container_width=True)

st.markdown("##### Score breakdown by category")
display_df = fopp[[
    "rank", "primary_category", "opportunity_score",
    "avg_protein", "avg_sugar", "avg_fiber",
    "total_products", "blue_ocean_count"
]].rename(columns={
    "rank":             "Rank",
    "primary_category": "Category",
    "opportunity_score":"Score",
    "avg_protein":      "Avg Protein (g)",
    "avg_sugar":        "Avg Sugar (g)",
    "avg_fiber":        "Avg Fiber (g)",
    "total_products":   "Total Products",
    "blue_ocean_count": "Blue Ocean Products",
}).round(2)

st.dataframe(
    display_df.style.background_gradient(subset=["Score"], cmap="RdYlGn"),
    use_container_width=True,
    hide_index=True,
)

if len(fopp) > 0:
    winner = fopp.loc[fopp["opportunity_score"].idxmax()]
    st.success(
        f"**Top opportunity: {winner['primary_category']}** "
        f"(Score: {winner['opportunity_score']:.1f} / 100) — "
        f"Only {int(winner['blue_ocean_count'])} products currently sit in the "
        f"Blue Ocean zone, with an average of {winner['avg_protein']:.1f}g protein "
        f"and {winner['avg_sugar']:.1f}g sugar per 100g."
    )

st.markdown("---")

# FAT vs FIBER HEATMAP
# Supporting chart showing the second health dimension.
# The ideal zone — high fiber, low fat — is equally under-served.
st.subheader("Fat vs Fiber Health Heatmap")
st.caption(
    "Protein and sugar are only part of the picture. This heatmap adds fat "
    "and fiber — the two other critical health signals. The top-left zone "
    "(high fiber, low fat) is where truly clean-label snacks would live. "
    "It is almost entirely empty."
)

heat_df = fdf[fdf["fiber_100g"].notna() & fdf["fat_100g"].notna()].copy()
heat_df  = heat_df.sample(min(3000, len(heat_df)), random_state=1)

fig_heat = px.density_heatmap(
    heat_df,
    x="fat_100g",
    y="fiber_100g",
    nbinsx=30, nbinsy=30,
    color_continuous_scale="RdYlGn",
    labels={
        "fat_100g":   "Fat (g per 100g)",
        "fiber_100g": "Fiber (g per 100g)",
    },
    title="Fat vs Fiber Density — Where Are the Truly Healthy Snacks?",
    height=440,
)
fig_heat.add_annotation(
    x=3, y=heat_df["fiber_100g"].max() * 0.85,
    text="Ideal zone: High Fiber + Low Fat",
    showarrow=False, font=dict(size=11, color="#1a6b35")
)
fig_heat.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=12),
)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown("---")

# STORY 4 — KEY MARKET INSIGHT & RECOMMENDATION
# "Based on the data, the biggest market opportunity is in
# [Category], specifically targeting products with [X]g of protein
# and less than [Y]g of sugar."

st.subheader("Story 4 — Key Market Insight & Recommendation")

best_cat = (
    df.groupby("primary_category")
    .apply(lambda g: int(((g["proteins_100g"] > 10) & (g["sugars_100g"] < 5)).sum()))
    .idxmax()
)
best_grp = df[
    (df["primary_category"] == best_cat) &
    (df["proteins_100g"] > 10) &
    (df["sugars_100g"]   < 5)
]
avg_prot = best_grp["proteins_100g"].mean()
avg_sug  = best_grp["sugars_100g"].mean()

st.success(
    f"Based on the data, the biggest market opportunity is in **{best_cat}**, "
    f"specifically targeting products with **{avg_prot:.0f}g of protein** "
    f"and less than **{avg_sug:.0f}g of sugar** per 100g.\n\n"
    f"Across 500,000 products analysed, only **{len(best_grp):,}** currently "
    f"occupy this space — a clear, underserved gap that represents a strong "
    f"first-mover opportunity for our client."
)
st.markdown("---")

# BONUS STORY — THE HIDDEN GEM: TOP PROTEIN SOURCES
# Analyse ingredients_text in the High Protein / Low Sugar cluster
# to identify the top 3 protein sources for the R&D team.
st.subheader("Bonus Story — The Hidden Gem: Top Protein Sources")
st.caption(
    "To help the R&D team formulate the new product, we analysed the "
    "ingredient lists of every High-Protein (>10g) / Low-Sugar (<5g) "
    "product to find the most common protein sources driving success "
    "in the Blue Ocean zone."
)

hp_df = df[
    (df["proteins_100g"] > 10) &
    (df["sugars_100g"]   < 5)  &
    df["ingredients_text"].notna()
]

PROTEIN_SOURCES = [
    "whey", "casein", "soy", "pea protein", "egg", "peanut", "almond",
    "milk protein", "hemp", "rice protein", "chickpea", "lentil",
    "quinoa", "sunflower seed", "pumpkin seed",
]

counts = Counter()
for text in hp_df["ingredients_text"].dropna():
    t = text.lower()
    for src in PROTEIN_SOURCES:
        if src in t:
            counts[src] += 1

top10 = counts.most_common(10)

if top10:
    src_df = pd.DataFrame(top10, columns=["Ingredient", "Count"])
    fig_ing = px.bar(
        src_df,
        x="Count",
        y="Ingredient",
        orientation="h",
        color="Count",
        color_continuous_scale="Teal",
        title="Most Common Protein Sources in High-Protein / Low-Sugar Products",
        height=400,
    )
    fig_ing.update_layout(
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig_ing, use_container_width=True)

    top3 = ", ".join([x[0].title() for x in top10[:3]])
    st.info(
        f"**Top 3 protein sources:** {top3}\n\n"
        f"R&D recommendation: Lead formulation with these ingredients "
        f"to deliver a credible high-protein claim with a clean label."
    )
else:
    st.warning(
        "Not enough ingredient data for this filter. "
        "Try widening your sidebar filters."
    )

st.markdown("---")
st.caption(
    "Data: Open Food Facts · openfoodfacts.org · First 500,000 rows · "
    "Analysis by Helix CPG Partners"
)
