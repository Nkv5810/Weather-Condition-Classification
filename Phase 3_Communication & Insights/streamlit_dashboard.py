import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Set page to wide mode
st.set_page_config(layout="wide")
import matplotlib.dates as mdates

# Load the icons into variables
snow_icon_path = 'snow-icon.png'
rain_icon_path = 'rain-icon.png'
clear_sky_icon_path = 'clear-sky-icon.png'
cloud_icon_path = 'cloud-icon.png'

# Map the weather condition labels to the icon file paths
icon_paths = {
    'Snow': snow_icon_path,
    'Rain': rain_icon_path,
    'Clear': clear_sky_icon_path,
    'Clouds': cloud_icon_path,
}

# Function to display the weather icon for a given condition
def display_weather_icon(condition, container):
    icon_path = icon_paths.get(condition, None)
    if icon_path:
        container.image(icon_path, width=60, use_column_width=True)


def plot_dual_axis_chart(data, temperature_col, humidity_col, date_col):
    fig, ax1 = plt.subplots()

    # Ensure the date column is in datetime format
    data[date_col] = pd.to_datetime(data[date_col])

    # Plotting Temperature
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature', color=color)
    ax1.plot(data[date_col], data[temperature_col], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Formatting x-axis to show only daily dates
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # Creating a second y-axis for Humidity
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Humidity', color=color)
    ax2.plot(data[date_col], data[humidity_col], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Temperative and Humidity Over Time")

    fig.tight_layout()  # To ensure the layout is organized
    return fig

def plot_wind_speed_chart(data, date_col, wind_speed_col):
    fig, ax = plt.subplots()
    ax.plot(data[date_col], data[wind_speed_col], color='tab:green')
    ax.set_xlabel('Date')
    ax.set_ylabel('Wind Speed')
    ax.set_title('Wind Speed Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_pressure_chart(data, date_col, pressure_col):
    fig, ax = plt.subplots()
    ax.plot(data[date_col], data[pressure_col], color='tab:purple')
    ax.set_xlabel('Date')
    ax.set_ylabel('Pressure')
    ax.set_title('Pressure Changes Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# Load Data
df = pd.read_csv('../Phase 2_Data Analysis/Part 1_Data Preprocessing/train_data_processed.csv')  
forecast_df = pd.read_csv('../Phase 2_Data Analysis/Part 3_Predictive Analytics/forecast_data.csv')

# Convert 'DateTime' column to datetime
df['DateTime'] = pd.to_datetime(df['DateTime'])
forecast_df["DateTime"] = pd.to_datetime(forecast_df["DateTime"])

# Streamlit Title
st.title('Weather Forecast Dashboard')

# # City Selection
# selected_city = st.selectbox('Select a City', df['City_Name'].unique())  # Replace 'city_column'

# # Filter Data Based on Selected City
# city_data = df[df['City_Name'] == selected_city]  # Replace 'city_column'

# # Create a row with two columns with 80% and 20% width
# col1, col2 = st.columns([10, 1])

# # Use the first column (col1) to display the current weather conditions
# with col1:
selected_city = st.selectbox('Select a City', df['City_Name'].unique())
city_data = df[df['City_Name'] == selected_city]
city_data_sorted = city_data.sort_values(by='DateTime')


# Plotting
fig_dual = plot_dual_axis_chart(city_data, 'Temperature', 'Humidity', 'DateTime')  # Replace column names

# Wind Speed Chart
fig_wind_speed = plot_wind_speed_chart(city_data, 'DateTime', 'Wind_Speed')

# Pressure Chart
fig_pressure = plot_pressure_chart(city_data, 'DateTime', 'Pressure')

col1, col2, col3, col4 = st.columns([0.28, 0.28, 0.28, 0.16])

with col1:
    st.pyplot(fig_dual)

with col2:
    st.pyplot(fig_wind_speed)

with col3:
    st.pyplot(fig_pressure)

with col4:
    # Display the select box for choosing the forecast date
    forecast_dates = forecast_df['DateTime'].unique()
    forecast_dates = sorted(forecast_dates)  # Sort the dates

    selected_forecast_date = st.selectbox('Select a Date for Forecast', forecast_dates)

    # Filter forecast data based on the selected date
    forecast_data_for_date = forecast_df[
        (forecast_df['DateTime'] == selected_forecast_date) & 
        (forecast_df['City_Name'] == selected_city)
    ]

    # Assuming you want to display the first available forecast for the selected date
    if not forecast_data_for_date.empty:
        forecast_row = forecast_data_for_date.iloc[0]

        # Create a layout with an additional column for horizontal space
        space_col, image_col = st.columns([1, 2])  # Adjust the ratio as needed

        # Display the icon in the image_col
        with image_col:
            st.image(icon_paths[forecast_row['Weather_Description']], width=75)  # Adjust the width as needed

        space_col, image_col = st.columns([1, 4])
        

        with image_col:
            st.write(f"Weather Status: {forecast_row['Weather_Description']}")



st.subheader("Previous 5 day Weather Condition with 3 hours Interval")
# Calculate the number of columns needed based on the number of timestamps
num_of_timestamps = city_data_sorted['DateTime'].nunique()
cols = st.columns(num_of_timestamps)

# Display the icons with timestamps in a horizontal layout
for i, (index, row) in enumerate(city_data_sorted.iterrows()):
    with cols[i]:
        # Display icon
        display_weather_icon(row['Weather_Description'], st)
        
        st.markdown("<div style='border-right: 5px dotted black; height: 60px;'></div>", unsafe_allow_html=True)
        # Display timestamp rotated 90 degrees using Markdown with custom font size
        timestamp = row['DateTime'].strftime('%Y-%m-%d %H:%M')
        st.markdown(f"<div style='writing-mode: vertical-rl; transform: rotate(200deg); font-size: 14px;'>{timestamp}</div>", unsafe_allow_html=True)