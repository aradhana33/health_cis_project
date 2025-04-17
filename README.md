# 🇨🇦 Canadian Health & Income Dashboard (Django Project)

This project is a full-stack data analytics application that explores and visualizes key hypotheses using Canadian Health Survey and Canadian Income Survey datasets. It uses Django on the backend and presents insights through interactive dashboards.
---
## Project Summary

We built a robust analytics pipeline that:
- Merges and processes real-world data from two national surveys (CIS & CHS)
- Tests multiple social and economic hypotheses
- Presents results in a visually engaging, user-friendly dashboard

---
## Hypotheses Explored

1. **Gender Pay Gap**  
   > Do males earn consistently more than females across provinces and age groups?

2. **Province-wise Health vs Income**  
   > Is there a correlation between income levels and self-reported health in different provinces?

3. **Work Hours vs Mental Health**  
   > Do longer work hours correlate with poorer mental health?

4. **Education vs Earnings**  
   > How does educational attainment affect income across age groups?

5. **Government Assistance Impact**  
   > What role does government support play in reported health and income stability?

---

## Tech Stack

- **Backend:** Django 4.x, Django REST Framework
- **Frontend:** Chart.js, Bootstrap, HTML5/CSS3
- **Data Processing:** Pandas, NumPy, MySQL
- **Visualization:** Chart.js, Matplotlib, Seaborn (pre-processing)
- **Deployment:** Localhost / PythonAnywhere / Heroku (optional)

---

## 🧪 Features

- Cleaned & merged datasets using `REF_DATE` and `COORDINATE` fields
- APIs to serve hypothesis-specific datasets
- Fully dynamic chart rendering with province filters
- Modular dashboard for interactive exploration
- Exportable visualizations for research reporting

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/health-cis-dashboard.git
   cd health-cis-dashboard
2. Create & Activate Virtual Environment
  python -m venv venv
  source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install Requirements
  pip install -r requirements.txt

4. Run Migrations
  python manage.py migrate

5. Load Data (optional: via custom management command)
  python manage.py load_combined_health_income
   
6.Start the Server
  python manage.py runserver
