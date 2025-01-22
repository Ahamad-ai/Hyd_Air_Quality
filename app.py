import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Load the data
@st.cache_data  # Cache data to speed up reruns
def load_data():
    """Loads the air quality data from CSV files and combines them.

    Returns:
        pandas.DataFrame: A DataFrame containing the combined air quality data.
    """

    years = range(2016, 2024)
    dfs = {}

    for year in years:
        file_path = f'Data/hyd_air_quality_{year}.csv'
        df = pd.read_csv(file_path)
        df['Year'] = year
        dfs[year] = df

    # Combine all dataframes
    combined_df = pd.concat(dfs.values(), ignore_index=True)

    # Melt the dataframe to long format
    melted_df = pd.melt(
        combined_df, id_vars=['Month', 'Year'], var_name='Location', value_name='AQI')

    # Convert Month to datetime
    melted_df['Date'] = pd.to_datetime(
        melted_df['Year'].astype(str) + '-' + melted_df['Month'], format='%Y-%b')

    # Sort by date
    melted_df = melted_df.sort_values('Date')

    return melted_df

# Load data using the cached function
melted_df = load_data()

# Streamlit app title
st.title("Hyderabad Air Quality Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio(
    "Go to", ("Overview", "Annual Trends", "Seasonal Patterns",
              "Month-to-month Variations", "Location Comparison",
              "Pollution Hotspots", "Time Series", "Correlation Analysis",
              "AQI Distribution", "Yearly Average Trend", "AQI Category Analysis"))


# Page content based on user selection
if selected_page == "Overview":
    st.header("Overview")
    st.write(
        "This app provides insights into air quality trends in Hyderabad from 2016 to 2023. Use the sidebar to navigate through different types of analysis.")

elif selected_page == "Annual Trends":
    st.header("Annual Air Quality Trends")
    fig_annual = px.box(melted_df, x='Year', y='AQI',
                        title='Annual Air Quality Trends')
    st.plotly_chart(fig_annual)
    st.write(
        "*How to Use:* This box plot visualizes the distribution of AQI values for each year. Observe the median (middle line), quartiles (box edges), and outliers (points outside the whiskers) to understand how air quality has changed over the years.")

elif selected_page == "Seasonal Patterns":
    st.header("Seasonal Air Quality Patterns")
    fig_seasonal = px.box(
        melted_df, x='Month', y='AQI', color='Year', title='Seasonal Air Quality Patterns')
    st.plotly_chart(fig_seasonal)
    st.write(
        "*How to Use:* This box plot displays the variation in AQI across different months, with each year represented by a different color. Look for patterns or trends that repeat annually, indicating potential seasonal influences on air quality.")

elif selected_page == "Month-to-month Variations":
    st.header("Month-to-month Air Quality Variations")
    fig_monthly = px.line(melted_df.groupby(['Date', 'Year'])['AQI'].mean(
    ).reset_index(), x='Date', y='AQI', color='Year', title='Monthly Air Quality Variations')
    st.plotly_chart(fig_monthly)
    st.write(
        "*How to Use:* This line graph illustrates the average monthly AQI values over time. It helps visualize how air quality fluctuates throughout the year and identify periods with higher or lower pollution levels.")

elif selected_page == "Location Comparison":
    st.header("Air Quality Comparison Across Locations")
    fig_locations = px.box(
        melted_df, x='Location', y='AQI', title='Air Quality Comparison Across Locations', height=600)
    fig_locations.update_xaxes(tickangle=45)
    st.plotly_chart(fig_locations)
    st.write(
        "*How to Use:* This box plot compares the distribution of AQI values for different locations within Hyderabad. Analyze the median, quartiles, and outliers to identify locations with better or worse air quality.")

elif selected_page == "Pollution Hotspots":
    st.header("Pollution Hotspots Heatmap")
    pivot_df = melted_df.pivot_table(
        values='AQI', index='Location', columns='Year', aggfunc='mean')
    fig_heatmap = px.imshow(
        pivot_df, title='Pollution Hotspots Heatmap', height=600)
    fig_heatmap.update_layout(coloraxis_colorscale='tealrose')
    st.plotly_chart(fig_heatmap)
    st.write(
        "*How to Use:* This heatmap provides a visual representation of average AQI levels for different locations across the years. Darker shades indicate higher pollution levels, making it easy to identify potential hotspots.")

elif selected_page == "Time Series":
    st.header("Air Quality Time Series by Location")
    fig_timeseries = go.Figure()

    for location in melted_df['Location'].unique():
        df_location = melted_df[melted_df['Location'] == location]
        fig_timeseries.add_trace(go.Scatter(
            x=df_location['Date'], y=df_location['AQI'], mode='lines', name=location))

    fig_timeseries.update_layout(
        title='Air Quality Time Series by Location', xaxis_title='Date', yaxis_title='AQI', height=550)
    st.plotly_chart(fig_timeseries)
    st.write(
        "*How to Use:* This interactive line graph displays the AQI values for each location over time. Use the legend to select specific locations and observe how their air quality has evolved.")

elif selected_page == "Correlation Analysis":
    st.header("Correlation Heatmap of Air Quality Across Locations")
    correlation_df = melted_df.pivot_table(
        values='AQI', index='Date', columns='Location')
    correlation_matrix = correlation_df.corr()
    fig_correlation = px.imshow(
        correlation_matrix, title='Correlation Heatmap of Air Quality Across Locations',color_continuous_scale="RdYlGn_r")
    st.plotly_chart(fig_correlation)
    st.write(
        "*How to Use:* This correlation heatmap visualizes the relationships between AQI values at different locations. Positive correlations (closer to 1, brighter shades) suggest similar air quality trends, while negative correlations (closer to -1, darker shades) indicate inverse relationships.")

elif selected_page == "AQI Distribution":
    st.header("Distribution of AQI Values by Location")
    fig_distribution = px.histogram(
        melted_df, x='AQI', color='Location', title='Distribution of AQI Values by Location', height=600)
    st.plotly_chart(fig_distribution)
    st.write(
        "*How to Use:* This histogram shows the frequency distribution of AQI values for each location. Analyze the shape, center, and spread of the distributions to understand the typical AQI range and potential outliers for different areas.")

elif selected_page == "Yearly Average Trend":
    st.header("Yearly Average AQI Trend")
    yearly_avg = melted_df.groupby('Year')['AQI'].mean().reset_index()
    fig_yearly_trend = px.line(
        yearly_avg, x='Year', y='AQI', title='Yearly Average AQI Trend')
    st.plotly_chart(fig_yearly_trend)
    st.write(
        "*How to Use:* This line graph depicts the overall trend in average AQI values over the years. Observe whether there's an increasing, decreasing, or fluctuating trend, indicating potential long-term changes in air quality.")

elif selected_page == "AQI Category Analysis":
    st.header("AQI Category Analysis")

    # Define the AQI categories and their corresponding ranges
    aqi_categories = {
        "GOOD": (0, 50),
        "SATISFACTORY": (51, 100),
        "MODERATE": (101, 200),
        "POOR": (201, 300),
        "VERY POOR": (301, 400),
        "SEVERE": (401, float("inf")),
    }

    # Create a dropdown to select the AQI category
    selected_category = st.selectbox(
        "Select AQI Category", list(aqi_categories.keys()))

    # Filter the data based on the selected category
    lower_bound, upper_bound = aqi_categories[selected_category]
    filtered_df = melted_df[(
        melted_df["AQI"] >= lower_bound) & (melted_df["AQI"] <= upper_bound)]

    # Display the cities, months, and years when the selected category was observed
    st.write(
        f"*Cities, Months, and Years for AQI Category {selected_category}:*")
    st.write(filtered_df[["Location", "Month", "Year"]])

    # Prepare data for the bar chart
    chart_data = filtered_df.groupby(
        ["Location", "Year"]).size().unstack(fill_value=0)

    # Display the bar chart
    st.bar_chart(chart_data)
    st.write(
        "*How to Use:* Select an AQI category from the dropdown to see the distribution of that category across different locations and years. The table shows the specific months and years when the selected category was observed.")