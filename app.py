import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.distance import great_circle
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# =====================
# Load Data Safely
# =====================
@st.cache_data
def load_data():
    try:
        stations_clean = pd.read_csv(r"cleaned_csv_datasets\stations_clean.csv")
    except Exception as e:
        st.error(f"⚠️ Error loading stations data: {e}")
        stations_clean = pd.DataFrame()

    try:
        trains_clean = pd.read_csv(r"cleaned_csv_datasets\trains_clean.csv")
    except Exception as e:
        st.error(f"⚠️ Error loading trains data: {e}")
        trains_clean = pd.DataFrame()

    try:
        schedules_clean = pd.read_csv(r"cleaned_csv_datasets\schedules_clean.csv")
    except Exception as e:
        st.error(f"⚠️ Error loading schedules data: {e}")
        schedules_clean = pd.DataFrame()

    return stations_clean, trains_clean, schedules_clean


stations_clean, trains_clean, schedules_clean = load_data()

# =====================
# Streamlit App Layout
# =====================
st.set_page_config(page_title="Indian Railways EDA", layout="wide")
st.title("🚆 Indian Railways - Exploratory Data Analysis")

tabs = st.tabs(["Stations", "Trains", "Schedules", "Geospatial Analysis", "Network & Downloads"])

# =====================
# Stations Tab
# =====================
with tabs[0]:
    st.header("Station Analysis")
    if stations_clean.empty:
        st.info("No station data available.")
    else:
        try:
            st.write(f"📊 **Dataset Shape:** {stations_clean.shape[0]} rows × {stations_clean.shape[1]} columns")

            st.subheader("Station Overview")
            st.dataframe(stations_clean.head(10))

            # 1. Top States by Station Count
            states_count = stations_clean.groupby("state")["station_code"].count().sort_values(ascending=False)
            st.subheader("Top States by Station Count")
            st.plotly_chart(px.bar(states_count.head(15).reset_index().rename(columns={'station_code':'stations'}),
                                   x='state', y='stations'))

            # 2. Zone-wise Distribution of Stations
            st.subheader("Stations per Zone")
            zone_count = stations_clean['zone'].value_counts().reset_index()
            zone_count.columns = ['zone', 'stations']
            st.plotly_chart(px.pie(zone_count, values='stations', names='zone', title="Stations by Zone"))

            # 3. Top 20 Cities by Stations
            st.subheader("Top 20 Cities with Most Stations")
            city_count = stations_clean.groupby("address")["station_code"].count().sort_values(ascending=False).head(20)
            st.plotly_chart(px.bar(city_count.reset_index().rename(columns={'station_code':'stations'}),
                                   x='address', y='stations'))

            # 4. State vs Zone Heatmap
            st.subheader("Stations Heatmap (State vs Zone)")
            heatmap_df = stations_clean.groupby(['state', 'zone']).size().reset_index(name='count')
            st.plotly_chart(px.density_heatmap(heatmap_df, x="zone", y="state", z="count",
                                               title="State vs Zone Station Distribution"))
        except Exception as e:
            st.error(f"⚠️ Error in Stations tab: {e}")

# =====================
# Trains Tab
# =====================
with tabs[1]:
    st.header("Train Analysis")
    if trains_clean.empty:
        st.info("No train data available.")
    else:
        try:
            st.write(f"📊 **Dataset Shape:** {trains_clean.shape[0]} rows × {trains_clean.shape[1]} columns")

            st.subheader("Distribution of Train Types")
            if "train_type" in trains_clean.columns:
                types_count = trains_clean['train_type'].value_counts().reset_index()
                types_count.columns = ['train_type', 'count']
                st.plotly_chart(px.bar(types_count, x='train_type', y='count'))
            else:
                st.warning("⚠️ 'train_type' column not found in trains dataset.")

            # 2. Trains per Zone
            if "zone" in trains_clean.columns:
                st.subheader("Trains per Zone")
                zone_count = trains_clean['zone'].value_counts().reset_index()
                zone_count.columns = ['zone', 'count']
                st.plotly_chart(px.bar(zone_count, x='zone', y='count'))
            else:
                st.warning("⚠️ 'zone' column not found in trains dataset.")

            # 3. Distance Distribution
            if "distance_km" in trains_clean.columns:
                st.subheader("Journey Distances")
                st.plotly_chart(px.histogram(trains_clean, x='distance_km', nbins=50,
                                             title="Train Distance Distribution (km)"))
            else:
                st.warning("⚠️ 'distance_km' column not found in trains dataset.")

            # 4. Speed Distribution
            if "avg_speed" in trains_clean.columns:
                st.subheader("Average Speeds")
                st.plotly_chart(px.histogram(trains_clean, x='avg_speed', nbins=50,
                                             title="Average Speed Distribution (km/hr)"))
            else:
                st.warning("⚠️ 'avg_speed' column not found in trains dataset.")
        except Exception as e:
            st.error(f"⚠️ Error in Trains tab: {e}")

# =====================
# Schedules Tab
# =====================
with tabs[2]:
    st.header("Schedule Analysis")
    if schedules_clean.empty:
        st.info("No schedules data available.")
    else:
        try:
            st.write(f"📊 **Dataset Shape:** {schedules_clean.shape[0]} rows × {schedules_clean.shape[1]} columns")

            # 1. Busiest Stations
            busiest = schedules_clean.groupby('station_name')['train_number'].count().sort_values(ascending=False)
            st.subheader("Busiest Stations (Top 20)")
            st.plotly_chart(px.bar(busiest.head(20).reset_index().rename(columns={'train_number': 'halts'}),
                                   x='station_name', y='halts'))

            # 2. Stops per Train
            stops = schedules_clean.groupby('train_number')['station_code'].count().sort_values(ascending=False)
            st.subheader("Stops per Train")
            st.plotly_chart(px.histogram(stops.reset_index().rename(columns={'station_code': 'stops'}),
                                         x='stops', nbins=30))

            # 3. Average Halt Times
            if "halt_min" in schedules_clean.columns:
                st.subheader("Average Halt Times per Station")
                halt_avg = schedules_clean.groupby('station_name')['halt_min'].mean().nlargest(20)
                st.plotly_chart(px.bar(halt_avg.reset_index(), x='station_name', y='halt_min'))

                st.subheader("Distribution of Halt Times (minutes)")
                st.plotly_chart(px.histogram(schedules_clean, x='halt_min', nbins=40))
            else:
                st.warning("⚠️ 'halt_min' column not found in schedules dataset.")

            # 5. Day-wise Train Operations
            if "day" in schedules_clean.columns:
                st.subheader("Train Frequency by Day")
                day_count = schedules_clean['day'].value_counts().reset_index()
                day_count.columns = ['day', 'count']
                st.plotly_chart(px.bar(day_count, x='day', y='count'))

            # 6. Arrival/Departure
            if "arrival_time" in schedules_clean.columns:
                st.subheader("Arrival Time Distribution")
                st.plotly_chart(px.histogram(schedules_clean, x='arrival_time', nbins=24))
            if "departure_time" in schedules_clean.columns:
                st.subheader("Departure Time Distribution")
                st.plotly_chart(px.histogram(schedules_clean, x='departure_time', nbins=24))

            # 8. Top 10 Trains by Stops
            top_trains = stops.head(10).reset_index().rename(columns={'station_code': 'stops'})
            st.subheader("Top 10 Trains with Maximum Stops")
            st.plotly_chart(px.bar(top_trains, x='train_number', y='stops'))

            # 9. Train Timings Scatter
            if {"departure_time", "arrival_time"}.issubset(schedules_clean.columns):
                st.subheader("Arrival vs Departure Time Scatter")
                st.plotly_chart(px.scatter(schedules_clean, x='departure_time', y='arrival_time'))

            # 10. Sample Schedule Table
            st.subheader("Sample Schedule Data")
            st.dataframe(schedules_clean.head(20))
        except Exception as e:
            st.error(f"⚠️ Error in Schedules tab: {e}")

# =====================
# Geospatial Tab
# =====================
with tabs[3]:
    st.header("Geospatial Analysis")
    try:
        if not stations_clean.empty and {"latitude", "longitude"}.issubset(stations_clean.columns):
            # 1. Stations Map
            st.subheader("📍 Railway Stations on Map")
            stations_map = stations_clean.dropna(subset=["latitude", "longitude"])
            if not stations_map.empty:
                st.map(stations_map[["latitude", "longitude"]])
            else:
                st.warning("No valid station coordinates available for mapping.")

            # 2. Distance Calculator
            st.subheader("🛤️ Distance Calculator Between Stations")
            station_list = stations_clean['station_name'].dropna().unique()
            start_station = st.selectbox("Select Start Station", station_list, key="start_station")
            end_station = st.selectbox("Select End Station", station_list, key="end_station")
            if st.button("Calculate Distance"):
                try:
                    loc1 = stations_clean[stations_clean['station_name'] == start_station][["latitude", "longitude"]].values[0]
                    loc2 = stations_clean[stations_clean['station_name'] == end_station][["latitude", "longitude"]].values[0]
                    distance = great_circle(loc1, loc2).kilometers
                    st.success(f"Distance between **{start_station}** and **{end_station}** is: {distance:.2f} km")
                except Exception as e:
                    st.error(f"Error calculating distance: {e}")

            # 3. Station Density Heatmap
            st.subheader("🌍 Station Density Heatmap")
            stations_heatmap = stations_clean.dropna(subset=["latitude", "longitude"])
            if not stations_heatmap.empty:
                m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
                HeatMap(data=stations_heatmap[["latitude", "longitude"]].values, radius=8).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.warning("No valid station coordinates available for Heatmap.")

            # 4. Train Route Visualization
            st.subheader("🚆 Train Route Visualization")
            if not trains_clean.empty and not schedules_clean.empty:
                if "train_number" in trains_clean.columns and "train_number" in schedules_clean.columns:
                    train_number = st.selectbox("Select Train Number", trains_clean["train_number"].unique())
                    route_stations = schedules_clean[schedules_clean["train_number"] == train_number]["station_code"].unique()
                    route_coords = stations_clean[stations_clean["station_code"].isin(route_stations)][["latitude","longitude"]].values
                    if len(route_coords) > 1:
                        m2 = folium.Map(location=[stations_clean["latitude"].mean(), stations_clean["longitude"].mean()], zoom_start=5)
                        folium.PolyLine(route_coords, color="blue", weight=3, opacity=0.8).add_to(m2)
                        for lat, lon in route_coords:
                            folium.CircleMarker([lat, lon], radius=4, color="red", fill=True).add_to(m2)
                        st_folium(m2, width=700, height=500)
                    else:
                        st.warning("Not enough data to plot this route.")
                else:
                    st.warning("⚠️ 'train_number' column not found in both datasets.")
    except Exception as e:
        st.error(f"⚠️ Error in Geospatial tab: {e}")

# =====================
# Network & Downloads Tab
# =====================
with tabs[4]:
    st.header("Network & Downloads")
    try:
        if not stations_clean.empty:
            st.download_button("⬇️ Download Stations CSV",
                               stations_clean.to_csv(index=False).encode('utf-8'), "stations_clean.csv","text/csv")
        if not trains_clean.empty:
            st.download_button("⬇️ Download Trains CSV",
                               trains_clean.to_csv(index=False).encode('utf-8'), "trains_clean.csv","text/csv")
        if not schedules_clean.empty:
            st.download_button("⬇️ Download Schedules CSV",
                               schedules_clean.to_csv(index=False).encode('utf-8'), "schedules_clean.csv","text/csv")

        # Add Report Downloads
        try:
            with open("assets\Indian Railways Data Analysis Report.pdf", "rb") as f:
                st.download_button("📄 Download Report (PDF)", f, "Final_Report.pdf")
        except Exception as e:
            st.warning(f"PDF Report not available: {e}")

        try:
            with open("assets\Indian Railways Data Analysis Report.docx", "rb") as f:
                st.download_button("📄 Download Report (DOCX)", f, "Final_Report.docx")
        except Exception as e:
            st.warning(f"DOCX Report not available: {e}")
    except Exception as e:
        st.error(f"⚠️ Error in Network & Downloads tab: {e}")
