import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Mental Health in Tech - EDA", layout="wide")

sns.set_style("whitegrid")


@st.cache_data
def load_data():
    df = pd.read_csv("survey.csv")

    df_clean = df.drop(columns=["comments", "Timestamp", "state"])

    df_clean["Age"] = df_clean["Age"].apply(lambda x: x if 18 <= x <= 75 else np.nan)
    df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
    df_clean["Age"] = df_clean["Age"].astype(int)

    def clean_gender(g):
        g = str(g).strip().lower()
        if g.startswith("m"):
            return "Male"
        elif g.startswith("f") or g == "woman":
            return "Female"
        else:
            return "Other"

    df_clean["Gender"] = df["Gender"].apply(clean_gender)
    df_clean["self_employed"] = df_clean["self_employed"].fillna("No")
    df_clean["work_interfere"] = df_clean["work_interfere"].fillna("Not applicable")
    df_clean["Country"] = df_clean["Country"].str.strip()

    return df_clean


df_clean = load_data()

st.title("Mental Health in Tech: An EDA of Workplace Attitudes and Treatment Seeking")
st.caption("Based on the 2014 OSMI Mental Health in Tech survey, 1259 responses")

st.sidebar.header("Filters")

countries = sorted(df_clean["Country"].unique())
top_countries = df_clean["Country"].value_counts().head(15).index.tolist()
selected_countries = st.sidebar.multiselect(
    "Country", options=countries, default=top_countries
)

genders = sorted(df_clean["Gender"].unique())
selected_genders = st.sidebar.multiselect("Gender", options=genders, default=genders)

size_order = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
sizes_present = [s for s in size_order if s in df_clean["no_employees"].unique()]
selected_sizes = st.sidebar.multiselect(
    "Company size", options=sizes_present, default=sizes_present
)

age_min, age_max = int(df_clean["Age"].min()), int(df_clean["Age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

filtered = df_clean[
    (df_clean["Country"].isin(selected_countries))
    & (df_clean["Gender"].isin(selected_genders))
    & (df_clean["no_employees"].isin(selected_sizes))
    & (df_clean["Age"].between(age_range[0], age_range[1]))
]

if filtered.empty:
    st.warning("No responses match the current filters. Adjust the filters in the sidebar.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Respondents shown", len(filtered))
treatment_rate = (filtered["treatment"] == "Yes").mean() * 100
col2.metric("Sought treatment", f"{treatment_rate:.1f}%")
col3.metric("Avg age", f"{filtered['Age'].mean():.0f}")
col4.metric("Countries", filtered["Country"].nunique())

st.divider()

tab1, tab2, tab3 = st.tabs(["Who took the survey", "Treatment drivers", "Policy factors"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(filtered["Age"], bins=20, kde=True, color="teal", ax=ax)
        ax.set_title("Age Distribution")
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(6, 4))
        order = filtered["Gender"].value_counts().index
        sns.countplot(data=filtered, x="Gender", order=order, palette="viridis", ax=ax)
        ax.set_title("Gender Distribution")
        st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    top_c = filtered["Country"].value_counts().head(10)
    sns.barplot(x=top_c.values, y=top_c.index, palette="mako", ax=ax)
    ax.set_title("Top Countries by Respondents")
    st.pyplot(fig)

with tab2:
    st.markdown(
        "Personal and clinical factors are the strongest predictors of treatment seeking "
        "in this dataset."
    )
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(
            data=filtered, x="family_history", hue="treatment", palette="Set1", ax=ax
        )
        ax.set_title("Family History vs Treatment")
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(7, 4))
        order = ["Never", "Rarely", "Sometimes", "Often", "Not applicable"]
        order = [o for o in order if o in filtered["work_interfere"].unique()]
        sns.countplot(
            data=filtered, x="work_interfere", hue="treatment", order=order,
            palette="Set1", ax=ax,
        )
        ax.set_title("Work Interference vs Treatment")
        plt.xticks(rotation=20)
        st.pyplot(fig)

with tab3:
    st.markdown(
        "Employees unsure about their benefits or care options behave much closer to "
        "employees with none at all than to employees who know their support clearly."
    )
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        order = [o for o in ["Yes", "Don't know", "No"] if o in filtered["benefits"].unique()]
        sns.countplot(
            data=filtered, x="benefits", hue="treatment", order=order, palette="Set1", ax=ax
        )
        ax.set_title("Benefits Awareness vs Treatment")
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(6, 4))
        order = [o for o in ["Yes", "Not sure", "No"] if o in filtered["care_options"].unique()]
        sns.countplot(
            data=filtered, x="care_options", hue="treatment", order=order,
            palette="Set1", ax=ax,
        )
        ax.set_title("Care Options Awareness vs Treatment")
        st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    order = ["Very easy", "Somewhat easy", "Don't know", "Somewhat difficult", "Very difficult"]
    order = [o for o in order if o in filtered["leave"].unique()]
    sns.countplot(
        data=filtered, x="leave", hue="treatment", order=order, palette="Set1", ax=ax
    )
    ax.set_title("Ease of Taking Leave vs Treatment")
    plt.xticks(rotation=15)
    st.pyplot(fig)

st.divider()
st.subheader("Key takeaway")
st.info(
    "Family history and symptom severity remain the strongest predictors of treatment "
    "seeking, and employers cannot influence either. The highest leverage, lowest cost "
    "action for employers is making existing benefits, care options, and leave policies "
    "unambiguous and well communicated."
)
