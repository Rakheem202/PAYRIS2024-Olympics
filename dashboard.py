import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from datetime import datetime, timedelta

st.set_page_config(page_title="FUN OLYMPICS", page_icon=":sports_medal:",layout="wide")

st.title(":swimmer: FUN OLYMPICS 2024")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Path to CSV file
default_file = "mock_paris2024.csv"

# Cache the data loading function to improve performance
@st.cache_data(ttl=10)
def load_data(file_path):
    return pd.read_csv(file_path, encoding="ISO-8859-1")

# Load data
df = load_data(default_file)


# Sidebar
# Get the current directory and construct the path to the logo image
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "Emblem.png")

st.sidebar.image(logo_path, caption="PAYRIS2024", use_column_width=True)

# Filter options
country_filter = st.sidebar.multiselect("Filter by Country", options=df['Country'].unique())
sport_filter = st.sidebar.multiselect("Filter by Sport", options=df['Sport'].unique())


# Filter data based on selections
filtered_df = df.copy()
if country_filter:
    filtered_df = filtered_df[filtered_df['Country'].isin(country_filter)]
if sport_filter:
    filtered_df = filtered_df[filtered_df['Sport'].isin(sport_filter)]

# Split the layout into three columns
col1, col2, col3 = st.columns(3)

# Convert 'Timestamp' column to datetime
filtered_df['Timestamp'] = pd.to_datetime(filtered_df['Timestamp'])

#---------------METRICS---------------------------
with col1:
        total_viewers = len(filtered_df)
        avg_visit_duration = filtered_df['Visit Duration'].mean()

        st.metric("Total Viewers", total_viewers)
        st.metric("Average Visit Duration (min)", round(avg_visit_duration, 2))

with col2:
     num_visits = len(df)
     peak_viewership_hour = filtered_df['Timestamp'].dt.hour.mode()[0]

     st.metric("Number of Visits to the Website", num_visits)
     st.metric("Peak Viewership Hour", f"{peak_viewership_hour}:00")


with col3:
      total_watch_time = filtered_df['Visit Duration'].sum()
      st.metric("Total Watch Time", f"{total_watch_time / 3600:.2f} hours")

with col3:
      viewers_retention_rate = avg_visit_duration/ total_viewers * 100 if total_viewers > 0 else 0
      st.metric("Viewers Retention Rate (%)", round(viewers_retention_rate, 2))

#---------------------------------VISUALS----------------------

with col1:
      sport_time_df = filtered_df.groupby(['Sport', 'Timestamp']).size().reset_index(name='Counts')
      sport_time_fig = px.area(sport_time_df, x='Timestamp', y='Counts', color='Sport',
                        title='Viewership for Different Sports Over Time')
      st.plotly_chart(sport_time_fig, use_container_width=True)



with col2:
      # Get top 5 viewed sports
    top_sports = filtered_df.groupby('Sport').size().reset_index(name='Viewership Counts').nlargest(10, 'Viewership Counts')
    # Display top 5 viewed sports in a table
    st.subheader("Top Viewed Sports")
    st.table(top_sports)


with col3:
    # Group data by country and count the number of viewers
    country_viewers_df = filtered_df.groupby('Country').size().reset_index(name='Viewership Counts')
    # Load a world map with Plotly
    world_map = px.choropleth(country_viewers_df, locations='Country', locationmode='country names', color='Viewership Counts',
                           hover_name='Country', color_continuous_scale=px.colors.sequential.Plasma,
                           title='Geographic Viewership Distribution')

    # Display the map
    st.plotly_chart(world_map, use_container_width=True)

with col1:
     # Group data by response code and count the number of occurrences
    response_code_counts = filtered_df['Response Code'].value_counts()

    # Create a bar chart for response code distribution
    response_code_fig = px.bar(x=response_code_counts.index, y=response_code_counts.values,
                           labels={'x': 'Response Code', 'y': 'Count'}, title='Distribution of Response Codes')
    response_code_fig.update_xaxes(type='category')
    st.plotly_chart(response_code_fig, use_container_width=True)

with col2:
    # Group data by age group and count the number of viewers
    age_group_counts = filtered_df['Age Group'].value_counts().sort_index()

    # Create a line chart for age group distribution
    age_group_fig = px.line(x=age_group_counts.index, y=age_group_counts.values,
                        labels={'x': 'Age Group', 'y': 'Number of Viewers'}, title='Distribution of Viewers by Age Group')
    age_group_fig.update_xaxes(type='category')
    st.plotly_chart(age_group_fig, use_container_width=True)


with col3:
    # Group data by event type and count the number of viewers
    event_counts = filtered_df['Event'].value_counts()

    # Create a pie chart for event distribution
    event_pie_fig = px.pie(names=event_counts.index, values=event_counts.values,
                       title='Distribution of Viewers by Event Type')
    st.plotly_chart(event_pie_fig, use_container_width=True) 

# Refresh the page every 10 seconds
time.sleep(10)
st.experimental_rerun()