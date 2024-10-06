import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# Establish SQLite connection
connection = sqlite3.connect(r'C:\Users\VIGNESH V\OneDrive\Desktop\code\project.db')

# Streamlit title
# Title with contrasting color to blue
st.markdown('<h1 style="color: orange;">GitHub Data Drive</h1>', unsafe_allow_html=True)


# Sidebar menu
with st.sidebar:
    select_fun = option_menu("Menu", ["App Info", "ANALYSIS", "Document"])

# Analysis section
if select_fun == "ANALYSIS":
    cols1 = st.columns([1, 1])

    # Load data from SQLite into a pandas DataFrame
    df = pd.read_sql("SELECT * FROM repositories", connection)

    # Multi-select options for filtering
    with cols1[0]:
        topic = st.multiselect("Select the Topic", df["Topic"].unique())

    with cols1[1]:
        language = st.multiselect("Select the Programming Language", df["Programming_Language"].unique())

    # Filter by selected topics (use `isin` since `topic` is a list)
    if topic:
        df = df[df["Topic"].isin(topic)]

    # Filter by selected programming languages
    if language:
        df = df[df["Programming_Language"].isin(language)]

    df.index = range(1, len(df) + 1)

    # Display filtered data
    with st. expander("To View the selectled filter data "):
        st.dataframe(df)

    # Selectbox for different analysis options
    question = st.selectbox("", [
        "1. The Most Used Programming Language is:",
        "2. The Top 10 Repositories with the Highest Number of Stars:",
        "3. The Top 10 Repositories with the Highest Number of Forks:",
        "4. The Top 10 Repositories with the Highest Number of Open Issues:",
        "5. Which Topic is Having the Highest Number of Repositories:"
    ])
    df = pd.read_sql("SELECT * FROM repositories", connection)
    # Analysis based on user selection
    if question == "1. The Most Used Programming Language is:":
        df_count = df["Programming_Language"].value_counts().reset_index()
        df_count.columns = ["Programming_Language", "Count"]
        st.write(f"The most popular programming language is {df_count['Programming_Language'].iloc[0]}")

        fig = px.pie(df_count, names="Programming_Language", values="Count", 
                     color="Programming_Language", title="Distribution of Programming Languages")
        st.plotly_chart(fig)

        language = st.selectbox("Select the Programming Language to get the details", df["Programming_Language"].unique())
        if language:
            filtered_df = df[df["Programming_Language"] == language]
            filtered_df.index = range(1, len(filtered_df) + 1)
            with st.expander(f"View repository details for {language}:"):
                st.dataframe(filtered_df)

    if question == "2. The Top 10 Repositories with the Highest Number of Stars:":
        df_top_stars = df.sort_values(by=["Number_of_Stars"], ascending=False).head(10)
        df_top_stars.index = range(1, len(df_top_stars) + 1)

        fig = px.line(df_top_stars, x='Repository_Name', y='Number_of_Stars',
                      title="Top 10 Repositories with the Highest Number of Stars",
                      markers=True, hover_data=["Repository_Name", "Number_of_Stars", 
                                                "Topic", "Programming_Language", "Owner"])
        st.plotly_chart(fig)

        with st.expander("View data for the top 10 repositories with the highest stars:"):
            st.dataframe(df_top_stars)

    if question == "3. The Top 10 Repositories with the Highest Number of Forks:":
        df_top_forks = df.sort_values(by='Number_of_Forks', ascending=False).head(10)
        df_top_forks.index = range(1, len(df_top_forks) + 1)

        fig = px.bar(df_top_forks, x='Repository_Name', y='Number_of_Forks',
                     title="Top 10 Repositories with the Highest Number of Forks",
                     hover_data=["Repository_Name", "Number_of_Forks", 
                                 "Topic", "Programming_Language", "Owner"])
        st.plotly_chart(fig)

        with st.expander("View data for the top 10 repositories with the highest forks:"):
            st.dataframe(df_top_forks)

    if question == "4. The Top 10 Repositories with the Highest Number of Open Issues:":
        df_top_opens = df.sort_values(by='Number_of_Open_Issues', ascending=False).head(10)
        df_top_opens.index = range(1, len(df_top_opens) + 1)

        fig = px.line(df_top_opens, x='Repository_Name', y='Number_of_Open_Issues', markers=True,
                      title="Top 10 Repositories with the Highest Number of Open Issues",
                      hover_data=["Repository_Name", "Number_of_Open_Issues", 
                                  "Topic", "Programming_Language", "Owner"])
        st.plotly_chart(fig)

        with st.expander("View data for the top 10 repositories with the highest open issues:"):
            st.dataframe(df_top_opens)

    if question == "5. Which Topic is Having the Highest Number of Repositories:":
        df_topic_count = df["Topic"].value_counts().reset_index()
        df_topic_count.columns = ["Topic", "Count"]

        fig = px.pie(df_topic_count, names="Topic", values="Count", 
                     color="Topic", title="Distribution of Repositories by Topic")
        st.plotly_chart(fig)

        topic_selected = st.selectbox("Select the topic to get the details", df_topic_count["Topic"].tolist())
        if topic_selected:
            filtered_topic_df = df[df["Topic"] == topic_selected]
            filtered_topic_df.index = range(1, len(filtered_topic_df) + 1)
            with st.expander(f"View repository details for {topic_selected}:"):
                st.dataframe(filtered_topic_df)
if select_fun=="App Info":
    st.write(f"""
# GitHub Repository Data App

This app contains three pages: **["App Info", "ANALYSIS", "Document"]**.

- In the **App Info** section, you will find an explanation of how the app works.
- The **ANALYSIS** section you will see all repository data by dataframe and visualization by selecting the filter option.

### Key Features:
1. **Filter Repositories:**
   - Users can filter displayed repositories by selecting topics and programming languages using multi-select widgets.
   - The DataFrame updates based on selected filters, and the filtered data is displayed in a table.

2. **Repository Analysis:**
   - Users can choose from predefined questions related to repository analysis.
   - Each question triggers specific queries to retrieve relevant data from the database.

3. **Visualizations:**
   - Visualizations (such as pie charts, line, and bar graphs) represent analysis results using Plotly.

4. **Detailed Insights:**
   - Detailed information about selected repositories or topics can be expanded for further insights.

The app provides an interactive interface for users to effectively explore and analyze GitHub repository data.
""")


if select_fun == "Document":
    # Ensure that the background image URL is correct
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9k3IMbzEHywRlzzmSTHJHZmDyWW14imxmyg&s");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0); /* Set the sidebar to be transparent */
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Add content below the background with white text and a white outline
    st.markdown('''
        <p style="color:white; font-size:20px; text-shadow: 
        -1px -1px 0 rgba(255, 255, 255, 0.8),  
        1px -1px 0 rgba(255, 255, 255, 0.8),
        -1px 1px 0 rgba(255, 255, 255, 0.8),
        1px 1px 0 rgba(255, 255, 255, 0.8);">
        Click the link below to open the document for the GitHub Data Dive project:
        </p>
    ''', unsafe_allow_html=True)

    # Add the link to the document
    # Add the link to the document with contrasting color to blue
    st.markdown('<a href="https://docs.google.com/document/d/1ESrkCz83axBA1bmhC6TmDm2z0tfRO70P/edit?usp=drive_link&ouid=114769012768804268922&rtpof=true&sd=true" style="color: #F36F15; font-size: 25px;">Open GitHub Data Drive Project Document</a>', unsafe_allow_html=True)


    # Footer
    footer = """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
            text-align: center;
            padding: 10px;
        }
        </style>
        <div class="footer">
            <p>Created by Vignesh Varathan | GitHub Data Dive Project | 
            <a href="mailto:vigneshvrthn@gmail.com">vigneshvrthn@gmail.com</a> | 
            <a href="https://wa.me/9360776848?text=Hi" target="_blank">WhatsApp: 9360776848</a></p>
        </div>
    """

    st.markdown(footer, unsafe_allow_html=True)
