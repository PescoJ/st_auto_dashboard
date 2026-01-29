# This code imports Pandas and Streamlit libraries to create a simple dashboard application.
import time
from pathlib import Path
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_autorefresh import st_autorefresh
from pathlib import path
# Setting the file paths
BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR
DATA_FILE = REPO_ROOT / "Project-Management-Sample=Data.xlsx"
# Auto-refresh setup
file_path = "Project-Management-Sample-Data.xlsx"
refresh_interval = 30_000  # seconds
st.components.v1.html(
    f"""
    <script>
      setTimeout(() => window.location.reload(), {refresh_interval});
    </script>
    """,
    height=0,
)
def get_mtime(path: str) -> float:
    return Path(path).stat().st_mtime
# Set up the Streamlit page configuration
st.set_page_config(layout="wide")
# Display a logo at the top of the dashboard
st.image("logo.png", width=100)
# Custom CSS to align buttons to the right
st.markdown(
    """
    <style>
      /* Try to prevent the middle link button from stretching */
      div[data-testid="stLinkButton"] > a {
        width: auto !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        white-space: nowrap !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)
# Creating a banner for the page
st.markdown('<div class="top-actions">', unsafe_allow_html=True)
# Creating three buttons: Manage Projects, Manage Tasks, and Manage Users
spacer, button_one, button_two, button_three = st.columns([9, 1, 1, 1], gap="small")
with button_one:
    manage_projects = st.popover(label="Manage Projects")
    with manage_projects:
        st.page_link("http://www.google.com", label="Home", icon="🏠")
        st.page_link("http://www.google.com", label="Project 1", icon="1️⃣")
        st.page_link("http://www.google.com", label="Project 2", icon="2️⃣")
        st.page_link("http://www.google.com", label="Project 3", icon="3️⃣")
with button_two:
        st.link_button(label="Manage Tasks", url="http://www.google.com")
with button_three:
    manage_users = st.popover(label="Manage Users")
    with manage_users:
        st.page_link("http://www.google.com", label="Admin", icon="🛠️")
        st.page_link("http://www.google.com", label="Leaders", icon="🛠️")
        st.page_link("http://www.google.com", label="Managers", icon="🛠️")
        st.page_link("http://www.google.com", label="Specialists", icon="🛠️")
# Close the banner div
st.markdown("</div>", unsafe_allow_html=True)
# Set the title and version of the dashboard
st.title("Project Management Master Dashboard")
st.markdown("Version 0.1.4")
# Function to load data from an Excel file with caching
@st.cache_data(ttl=30)
def load_workbook(path: str, mtime: float):
    return pd.read_excel(path, sheet_name=None)
mtime = get_mtime("Project-Management-Sample-Data.xlsx")
sheets = load_workbook("Project-Management-Sample-Data.xlsx", mtime)
st.caption(f"Last updated: {time.ctime(mtime)}")
df = load_workbook("Project-Management-Sample-Data.xlsx", get_mtime("Project-Management-Sample-Data.xlsx"))
# Format data for Line Chart on Step Tab 1
def load_progress_data(filepath):
    df = pd.read_excel(filepath, sheet_name="Progress Over Time")
    df.columns = df.columns.str.strip()
    if "Task Name" not in df.columns:
        st.error("The 'Progress Over Time' sheet must contain a 'Task Name' column.")
        return pd.DataFrame(columns=["Task Name", "Week", "Progress"])
    long_df = pd.melt(df,
                      id_vars=["Task Name"], 
                      var_name="Week", 
                      value_name="Progress"
                      )
    return long_df
# Create a side bar for holding Project Information
with st.sidebar:
    st.logo("logo.png", size="large")
    st.header("Project Information")
    project_name = st.text_input("Project Name", value="New Project")
    project_manager = st.text_input("Project Manager", value="John Doe")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    st.markdown("---")
# Use a default file if no file is uploaded
DEFAULT_FILE = "Project-Management-Sample-Data.xlsx"
data_source = DEFAULT_FILE
# Create tabs for uploading data, viewing data, and displaying progress graphics
tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(["Progress Graphics", "End of Week 1", "End of Week 2", "End of Week 3", "End of Week 4"])
# Tab 1 - Progress Graphic
with tab_1:
    st.header("Progress Graphic")
    progress_df = load_progress_data(data_source)
    all_tasks = progress_df["Task Name"].unique()
    chosen_tasks = st.multiselect(
            "Select Tasks to Display", 
            options=all_tasks, 
            default=all_tasks[:15], 
            max_selections=15
            )
    filtered_df = progress_df[progress_df["Task Name"].isin(chosen_tasks)]
    chart = (
        alt.Chart(filtered_df)
        .mark_line(point=True)
        .encode(
            x = alt.X("Week:N", title = "Project Week"),
            y = alt.Y("Progress:Q", title = "Progress (%)", scale=alt.Scale(domain=[0, 1])),
            color = alt.Color("Task Name:N", title = "Task Name"),
            tooltip = ["Task Name:N", "Week:N", "Progress:Q"]     
        )
    )
    st.altair_chart(chart, use_container_width=True)
# Tab 2 - End of Week 1
with tab_2:
    st.header("End of Week 1")
    df = pd.read_excel(data_source, sheet_name="End of Week 1")
    st.dataframe(df, use_container_width=True, column_config={
        "Start Date": st.column_config.DateColumn("Start Date"),
        "End Date": st.column_config.DateColumn("End Date"),
        "Progress": st.column_config.ProgressColumn("Progress", color="auto")})
# Tab 3 - End of Week 2
with tab_3:
    st.header("End of Week 2")
    df = pd.read_excel(data_source, sheet_name="End of Week 2")
    st.dataframe(df, use_container_width=True, column_config={
        "Start Date": st.column_config.DateColumn("Start Date"),
        "End Date": st.column_config.DateColumn("End Date"),
        "Progress": st.column_config.ProgressColumn("Progress", color="auto")})
# Tab 4 - End of Week 3
with tab_4:
    st.header("End of Week 3")
    df = pd.read_excel(data_source, sheet_name="End of Week 3")
    st.dataframe(df, use_container_width=True, column_config={
        "Start Date": st.column_config.DateColumn("Start Date"),
        "End Date": st.column_config.DateColumn("End Date"),
        "Progress": st.column_config.ProgressColumn("Progress", color="auto")})
# Tab 5 - End of Week 4
with tab_5:
    st.header("End of Week 4")
    df = pd.read_excel(data_source, sheet_name="End of Week 4")
    st.dataframe(df, use_container_width=True, column_config={
        "Start Date": st.column_config.DateColumn("Start Date"),
        "End Date": st.column_config.DateColumn("End Date"),
        "Progress": st.column_config.ProgressColumn("Progress", color="auto")})
    