# 🚆 Indian Railways EDA & Visualization

> ✨ An interactive data analysis and visualization tool to explore the vast Indian Railways network.

---

## 🌟 Why I Built This

I often wondered:

* ❓ *How large and connected is the Indian Railways network?*
* ❓ *Which stations are the busiest and most important?*
* ❓ *How do train routes and schedules reveal hidden patterns?*

To answer these, I built this project.
👉 It transforms raw railway datasets into **insightful visualizations, interactive maps, and downloadable reports** — making exploration fun and data-driven.

---

## 🔎 Features

✅ **Stations Analysis**

* Top states, zones, and cities by station count
* Interactive heatmaps (State vs Zone)

✅ **Trains Analysis**

* Distribution of train types, zones, distances, and speeds

✅ **Schedules Analysis**

* Busiest stations, stops per train
* Halt times, frequency by day, arrival/departure distributions

✅ **Geospatial Analysis**

* Stations on map
* Distance calculator between two stations
* Station density heatmap
* Route visualization for any train number

✅ **Downloads**

* Download **Stations, Trains, Schedules datasets**
* One-click access to final reports (📄 PDF, 📝 DOCX)

---

## 🚀 Live Demo

👉 [**Streamlit App**](https://indian-railways-eda-report.streamlit.app/)

---

## 📂 Project Structure

```
📦 indian-railways-eda
 ┣ 📂 assets                  # Final reports (PDF, DOCX)
 ┣ 📂 data                    # Cleaned CSV datasets (stations, trains, schedules)
 ┣ 📜 app.py                  # Streamlit app
 ┣ 📜 Indian_railways.ipynb   # Jupyter Notebook (EDA)
 ┣ 📜 requirements.txt        # Dependencies
 ┗ 📜 README.md               # Documentation
```

---

## ⚡ Quick Start

Clone this repo and run locally:

```bash
# 1. Clone the repo
git clone https://github.com/Tom-1508/indian-railways-eda.git
cd indian-railways-eda

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```

---

## 📊 Example Insights

* 🏙️ Delhi, Mumbai, and Kolkata dominate in station density
* 🚄 Train speeds cluster in certain ranges depending on type/zone
* ⏱️ Busiest stations handle hundreds of halts daily
* 🗺️ Train routes can be visualized dynamically across India

---

## 📜 Reports  

📄 [Download PDF Report](assets/Indian%20Railways%20Data%20Analysis%20Report.pdf)  
📝 [Download DOCX Report](assets/Indian%20Railways%20Data%20Analysis%20Report.docx)  


---

## 💡 Tech Stack

* **Python** (pandas, numpy, plotly, folium, geopy)
* **Streamlit** for interactive dashboards
* **Plotly & Folium** for visualizations/maps
* **ReportLab & python-docx** for reports

---

## 🤝 Contribution

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Submit a Pull Request 🚀

---

## 🌍 Connect

🔗 GitHub: [Tom-1508](https://github.com/Tom-1508)
🔗 Live App: [Streamlit App](https://indian-railways-eda-report.streamlit.app/)

---

📌 *A project that blends data science curiosity with the heartbeat of India — its railways.* ❤️🚆

---
