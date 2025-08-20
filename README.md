# 🤖📊 AI vs Human Content Analysis Dashboard

Welcome to the **AI vs Human Content Analysis** mini project! This project lets you explore and compare engagement metrics between AI-generated and human-written content using an interactive dashboard and automated analysis reports.

---

## 🚀 Project Overview

- **Goal:** Analyze how AI-generated content (e.g., ChatGPT articles, LinkedIn posts) performs in terms of engagement compared to human-written content.
- **Key Question:** _Does AI-generated content get more or less engagement (likes, comments, shares) than human-created content?_
- **Tech Stack:** Python, Streamlit, Plotly, Pandas, Matplotlib, Seaborn, python-docx

---

## ✨ Features

- 📈 **Interactive Dashboard:**
  - Filter by date, author type (AI/Human), and content type
  - Visualize engagement trends, comparisons, and breakdowns
  - KPI cards for likes, comments, shares, and engagement score
- 📑 **Automated Analysis Report:**
  - Generates a Word report with key findings and recommendations
- 📂 **Sample Dataset:**
  - `ai_vs_human_content_dataset.csv` with real engagement data for both AI and human posts

---

## 🗂️ Dataset Structure

| Column         | Description                                 |
|---------------|---------------------------------------------|
| Post_ID       | Unique identifier for each post              |
| Author_Type   | 'AI' or 'Human'                             |
| Content_Type  | Type of content (e.g., Career Tip, Learning)|
| Likes         | Number of likes                             |
| Comments      | Number of comments                          |
| Shares        | Number of shares                            |
| Date          | Date of post (DD-MM-YYYY)                   |
| Word_Count    | Number of words in the post                 |
| Engagement_Score | Likes + 2×Comments + 3×Shares           |

---

## 🛠️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Run

### 1. 🚦 Launch the Dashboard

- **Start the Streamlit dashboard:**
  ```bash
  streamlit run dashboard.py
  ```
- **What happens:**
  - Your browser will open the dashboard automatically.
  - Use the sidebar to filter by date, author type, and content type.
  - Explore KPIs, charts, and trends interactively!

### 2. 📝 Generate the Analysis Report (Word Doc)

- **Run the analysis script:**
  ```bash
  python dashboard_analysis_report.py
  ```
- **What happens:**
  - A file named `AI_vs_Human_Content_Analysis_Report.docx` will be created in your project folder.
  - Open it in MS Word to read the executive summary, findings, and recommendations.

### 3. 📄 (Optional) Extract Project Documentation

- **Extract text from the project docx file:**
  ```bash
  python read_project_doc.py
  ```
- **What happens:**
  - The script will extract text from the project docx and save it as `project_doc.txt` for easy reading.

---

## 📊 Example Visualizations

- Bar chart: Average engagement (AI vs Human)
- Line chart: Engagement trend over time
- Pie chart: Share of total engagement by author type
- Box plot: Engagement by content type

---

## 💡 Insights & Next Steps

- Use this project to showcase your data analysis and dashboarding skills.
- Try adding more data, new visualizations, or advanced analytics!

---

## 🙌 Credits

- Inspired by real-world social media analytics and the impact of AI on content creation.

---

## 📝 License

This project is for educational and portfolio use. Feel free to adapt and share!
