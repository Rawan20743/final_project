# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import joblib
# import os
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.pipeline import Pipeline

# st.set_page_config(page_title="Financial & ESG Dashboard", page_icon="🌍", layout="wide")

# FINANCIAL_PATH = "financial_dataset.csv"
# ESG_PATH = "esg_dataset.csv"
# MODEL_PATH = "random_forest_regressor.pkl"


# def sustainability(score):
#     if score >= 80:
#         return "High"
#     elif score >= 60:
#         return "Medium"
#     else:
#         return "Low"


# @st.cache_data
# def load_data():
#     """Load and merge financial and ESG datasets directly in memory."""
#     if not os.path.exists(FINANCIAL_PATH) or not os.path.exists(ESG_PATH):
#         st.error("⚠️ Files financial_dataset.csv and esg_dataset.csv must be in the same folder as the application.")
#         st.stop()

#     financial_df = pd.read_csv(FINANCIAL_PATH)
#     esg_df = pd.read_csv(ESG_PATH)

#     df = pd.merge(
#         financial_df,
#         esg_df,
#         on=["CompanyID", "CompanyName", "Year"],
#         how="inner"
#     )

#     df["GrowthRate"] = df["GrowthRate"].fillna(0)
#     df["Sustainability_Level"] = df["ESG_Overall"].apply(sustainability)
    
#     return df


# def train_model(df):
#     X = df[['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 'CarbonEmissions', 'WaterUsage', 'EnergyConsumption', 'Industry', 'Region']]
#     y = df['ESG_Overall']
#     preprocessor = ColumnTransformer(transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), ["Industry", "Region"])], remainder="passthrough")
#     model = Pipeline([("preprocessor", preprocessor), ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))])
#     model.fit(X, y)
#     joblib.dump(model, MODEL_PATH)
#     return model


# def prepare_model(df):
#     if not os.path.exists(MODEL_PATH):
#         train_model(df)


# # Load data and model
# df = load_data()
# prepare_model(df)

# @st.cache_resource
# def load_model():
#     return joblib.load(MODEL_PATH)

# model = load_model()

# # Sidebar Filters
# st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3003/3003314.png", width=100)
# st.sidebar.header("🔍 Data Filters")

# selected_year = st.sidebar.multiselect("Select Year", options=sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
# selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
# selected_industry = st.sidebar.multiselect("Select Industry", options=df['Industry'].unique(), default=df['Industry'].unique())
# selected_sus_level = st.sidebar.multiselect("Select Sustainability Level", options=df['Sustainability_Level'].unique(), default=df['Sustainability_Level'].unique())

# filtered_df = df[
#     (df['Year'].isin(selected_year)) &
#     (df['Region'].isin(selected_region)) &
#     (df['Industry'].isin(selected_industry)) &
#     (df['Sustainability_Level'].isin(selected_sus_level))
# ]

# if filtered_df.empty:
#     st.warning("⚠️ No data matches the selected filters.")
#     st.stop()

# # Main Dashboard Layout
# st.title("🌍 Financial and Environmental Performance Dashboard (ESG Analytics)")
# st.divider()

# st.header("📈 Key Performance Indicators (KPIs)")
# kpi1, kpi2, kpi3 = st.columns(3)
# kpi1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
# kpi2.metric("Average Profit Margin", f"{filtered_df['ProfitMargin'].mean():.2f}%")
# kpi3.metric("Average ESG Score", f"{filtered_df['ESG_Overall'].mean():.2f}")

# kpi4, kpi5, kpi6 = st.columns(3)
# kpi4.metric("Average Growth Rate", f"{filtered_df['GrowthRate'].mean():.2f}%")
# kpi5.metric("Total Carbon Emissions", f"{filtered_df['CarbonEmissions'].sum():,.0f}")
# kpi6.metric("Unique Companies", f"{filtered_df['CompanyID'].nunique():,.0f}")

# st.divider()
# st.header("📉 Charts")
# col1, col2 = st.columns(2)

# with col1:
#     esg_by_industry = filtered_df.groupby("Industry")["ESG_Overall"].mean().reset_index()
#     fig1 = px.bar(esg_by_industry, x='Industry', y='ESG_Overall', title="Average ESG Score by Industry", color='Industry')
#     st.plotly_chart(fig1, use_container_width=True)

# with col2:
#     fig2 = px.scatter(filtered_df, x="ESG_Overall", y="Revenue", color="Sustainability_Level", title="Revenue vs. ESG Score")
#     st.plotly_chart(fig2, use_container_width=True)
# st.divider()
# st.header("📈 Average Revenue Over Years")

# revenue_year = filtered_df.groupby("Year")["Revenue"].mean().reset_index()

# fig3 = px.line(
#     revenue_year,
#     x="Year",
#     y="Revenue",
#     markers=True,
#     title="Average Revenue Over Years"
# )

# fig3.update_layout(
#     xaxis_title="Year",
#     yaxis_title="Average Revenue"
# )

# st.plotly_chart(fig3, use_container_width=True)


# st.divider()
# st.header("🤖 Sustainability Score Prediction (ESG Score Prediction)")



# with st.form("prediction_form"):
#     c1, c2, c3 = st.columns(3)
#     with c1:
#         rev = st.number_input("Revenue", value=1000.0)
#         prof = st.number_input("Profit Margin", value=10.0)
#         cap = st.number_input("Market Cap", value=5000.0)
#     with c2:
#         growth = st.number_input("Growth Rate", value=5.0)
#         carbon = st.number_input("Carbon Emissions", value=10000.0)
#         water = st.number_input("Water Usage", value=5000.0)
#     with c3:
#         energy = st.number_input("Energy Consumption", value=20000.0)
#         ind = st.selectbox("Industry", options=df['Industry'].unique())
#         reg = st.selectbox("Region", options=df['Region'].unique())
        
#     if st.form_submit_button("Predict ESG Score 🎯"):
#         input_data = pd.DataFrame({
#             "Revenue": [rev], "ProfitMargin": [prof], "MarketCap": [cap], 
#             "GrowthRate": [growth], "CarbonEmissions": [carbon], "WaterUsage": [water], 
#             "EnergyConsumption": [energy], "Industry": [ind], "Region": [reg]
#         })
#         pred = model.predict(input_data)[0]
#         st.success(f"Predicted ESG Score: {pred:.2f}")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Financial & ESG Dashboard",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# 2. FILE PATHS
# ============================================================

FINANCIAL_PATH = "financial_dataset.csv"
ESG_PATH = "esg_dataset.csv"
MODEL_PATH = "random_forest_regressor.pkl"


# ============================================================
# 3. SUSTAINABILITY LEVEL FUNCTION
# ============================================================

def sustainability(score):

    if score >= 80:
        return "High"

    elif score >= 60:
        return "Medium"

    else:
        return "Low"


# ============================================================
# 4. LOAD AND MERGE DATA
# ============================================================

@st.cache_data
def load_data():

    # Check if datasets exist
    if not os.path.exists(FINANCIAL_PATH) or not os.path.exists(ESG_PATH):

        st.error(
            "Files financial_dataset.csv and esg_dataset.csv "
            "must be in the same folder as the application."
        )

        st.stop()

    # Read datasets
    financial_df = pd.read_csv(FINANCIAL_PATH)
    esg_df = pd.read_csv(ESG_PATH)

    # Merge Financial and ESG datasets
    df = pd.merge(
        financial_df,
        esg_df,
        on=["CompanyID", "CompanyName", "Year"],
        how="inner"
    )

    # Fill missing GrowthRate values
    df["GrowthRate"] = df["GrowthRate"].fillna(0)

    # Create Sustainability Level
    df["Sustainability_Level"] = df["ESG_Overall"].apply(
        sustainability
    )

    return df


# ============================================================
# 5. TRAIN MACHINE LEARNING MODEL
# ============================================================

def train_model(df):

    # Features
    X = df[
        [
            "Revenue",
            "ProfitMargin",
            "MarketCap",
            "GrowthRate",
            "CarbonEmissions",
            "WaterUsage",
            "EnergyConsumption",
            "Industry",
            "Region"
        ]
    ]

    # Target
    y = df["ESG_Overall"]

    # Encode categorical columns
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                ["Industry", "Region"]
            )
        ],
        remainder="passthrough"
    )

    # Random Forest model
    model = Pipeline(
        [
            ("preprocessor", preprocessor),

            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
            )
        ]
    )

    # Train model
    model.fit(X, y)

    # Save model
    joblib.dump(model, MODEL_PATH)

    return model


# ============================================================
# 6. PREPARE MODEL
# ============================================================

def prepare_model(df):

    if not os.path.exists(MODEL_PATH):

        train_model(df)


# ============================================================
# 7. LOAD DATA AND MODEL
# ============================================================

df = load_data()

prepare_model(df)


@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)


model = load_model()


# ============================================================
# 8. SIDEBAR FILTERS
# ============================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3003/3003314.png",
    width=100
)

st.sidebar.header("🔍 Data Filters")


# ------------------------------------------------------------
# YEAR TIMELINE / RANGE SLIDER
# ------------------------------------------------------------

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)


# ------------------------------------------------------------
# REGION FILTER
# ------------------------------------------------------------

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)


# ------------------------------------------------------------
# INDUSTRY FILTER
# ------------------------------------------------------------

selected_industry = st.sidebar.multiselect(
    "Select Industry",
    options=sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)


# ------------------------------------------------------------
# SUSTAINABILITY LEVEL FILTER
# ------------------------------------------------------------

selected_sus_level = st.sidebar.multiselect(
    "Select Sustainability Level",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)


# ============================================================
# 9. APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Year"] >= selected_year_range[0]) &
    (df["Year"] <= selected_year_range[1]) &
    (df["Region"].isin(selected_region)) &
    (df["Industry"].isin(selected_industry)) &
    (df["Sustainability_Level"].isin(selected_sus_level))
]


# Check if filtered data is empty
if filtered_df.empty:

    st.warning(
        "⚠️ No data matches the selected filters."
    )

    st.stop()


# ============================================================
# 10. DASHBOARD TITLE
# ============================================================

st.title(
    "🌍 Financial and Environmental Performance Dashboard"
)

st.subheader("ESG Analytics")

st.divider()


# ============================================================
# 11. KEY PERFORMANCE INDICATORS
# ============================================================

st.header("📈 Key Performance Indicators (KPIs)")


# First row of KPIs

kpi1, kpi2, kpi3 = st.columns(3)


kpi1.metric(
    "Total Revenue",
    f"${filtered_df['Revenue'].sum():,.0f}"
)


kpi2.metric(
    "Average Profit Margin",
    f"{filtered_df['ProfitMargin'].mean():.2f}%"
)


kpi3.metric(
    "Average ESG Score",
    f"{filtered_df['ESG_Overall'].mean():.2f}"
)


# Second row of KPIs

kpi4, kpi5, kpi6 = st.columns(3)


kpi4.metric(
    "Average Growth Rate",
    f"{filtered_df['GrowthRate'].mean():.2f}%"
)


kpi5.metric(
    "Total Carbon Emissions",
    f"{filtered_df['CarbonEmissions'].sum():,.0f}"
)


kpi6.metric(
    "Unique Companies",
    f"{filtered_df['CompanyID'].nunique():,.0f}"
)


st.divider()


# ============================================================
# 12. CHARTS
# ============================================================

st.header("📉 Data Visualizations")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# CHART 1: ESG SCORE BY INDUSTRY
# ------------------------------------------------------------

with col1:

    esg_by_industry = (
        filtered_df
        .groupby("Industry")["ESG_Overall"]
        .mean()
        .reset_index()
    )

    fig1 = px.bar(
        esg_by_industry,
        x="Industry",
        y="ESG_Overall",
        title="Average ESG Score by Industry",
        color="Industry"
    )

    fig1.update_layout(
        xaxis_title="Industry",
        yaxis_title="Average ESG Score"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


# ------------------------------------------------------------
# CHART 2: REVENUE VS ESG SCORE
# ------------------------------------------------------------

with col2:

    fig2 = px.scatter(
        filtered_df,
        x="ESG_Overall",
        y="Revenue",
        color="Sustainability_Level",
        title="Revenue vs. ESG Score"
    )

    fig2.update_layout(
        xaxis_title="ESG Score",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ============================================================
# 13. AVERAGE REVENUE OVER YEARS
# ============================================================

st.divider()

st.header("📈 Average Revenue Over Years")


revenue_year = (
    filtered_df
    .groupby("Year")["Revenue"]
    .mean()
    .reset_index()
)


fig3 = px.line(
    revenue_year,
    x="Year",
    y="Revenue",
    markers=True,
    title="Average Revenue Over Years"
)


fig3.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Revenue"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# ============================================================
# 14. SUSTAINABILITY LEVEL DISTRIBUTION
# ============================================================

st.divider()

st.header("🌱 Sustainability Level Distribution")


sustainability_count = (
    filtered_df["Sustainability_Level"]
    .value_counts()
    .reindex(["High", "Medium", "Low"], fill_value=0)
    .reset_index()
)


sustainability_count.columns = [
    "Sustainability_Level",
    "Number_of_Records"
]


fig4 = px.bar(
    sustainability_count,
    x="Sustainability_Level",
    y="Number_of_Records",
    title="Distribution of Sustainability Levels",
    color="Sustainability_Level"
)


fig4.update_layout(
    xaxis_title="Sustainability Level",
    yaxis_title="Number of Records"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# ============================================================
# 15. MACHINE LEARNING PREDICTION
# ============================================================

st.divider()

st.header(
    "🤖 Sustainability Score Prediction"
)


st.write(
    "Enter company information to predict the ESG score."
)


with st.form("prediction_form"):

    c1, c2, c3 = st.columns(3)


    # --------------------------------------------------------
    # COLUMN 1
    # --------------------------------------------------------

    with c1:

        rev = st.number_input(
            "Revenue",
            value=1000.0
        )

        prof = st.number_input(
            "Profit Margin",
            value=10.0
        )

        cap = st.number_input(
            "Market Cap",
            value=5000.0
        )


    # --------------------------------------------------------
    # COLUMN 2
    # --------------------------------------------------------

    with c2:

        growth = st.number_input(
            "Growth Rate",
            value=5.0
        )

        carbon = st.number_input(
            "Carbon Emissions",
            value=10000.0
        )

        water = st.number_input(
            "Water Usage",
            value=5000.0
        )


    # --------------------------------------------------------
    # COLUMN 3
    # --------------------------------------------------------

    with c3:

        energy = st.number_input(
            "Energy Consumption",
            value=20000.0
        )

        ind = st.selectbox(
            "Industry",
            options=sorted(df["Industry"].unique())
        )

        reg = st.selectbox(
            "Region",
            options=sorted(df["Region"].unique())
        )


    # --------------------------------------------------------
    # PREDICTION BUTTON
    # --------------------------------------------------------

    submitted = st.form_submit_button(
        "Predict ESG Score 🎯"
    )


    if submitted:

        input_data = pd.DataFrame(
            {
                "Revenue": [rev],
                "ProfitMargin": [prof],
                "MarketCap": [cap],
                "GrowthRate": [growth],
                "CarbonEmissions": [carbon],
                "WaterUsage": [water],
                "EnergyConsumption": [energy],
                "Industry": [ind],
                "Region": [reg]
            }
        )


        # Make prediction
        pred = model.predict(input_data)[0]


        # Keep prediction within ESG score range
        pred = max(0, min(100, pred))


        st.success(
            f"Predicted ESG Score: {pred:.2f}"
        )


        # Display sustainability level
        if pred >= 80:

            level = "High"

        elif pred >= 60:

            level = "Medium"

        else:

            level = "Low"


        st.info(
            f"Predicted Sustainability Level: {level}"
        )