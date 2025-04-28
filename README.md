# TeslaSolar_Analysis

**Overview**  
This project analyzes Tesla Solar customer feedback scraped from Reddit.  
Using Large Language Models (LLMs), the posts are dynamically categorized into major customer topics like system performance issues, installation delays, customer support concerns, and positive experiences.

The results are visualized in an interactive **Streamlit** dashboard for easy exploration and insight generation.

---

## Project Workflow

1. **Data Collection**  
   - Reddit posts related to Tesla Solar were scraped.
   - Combined `title` and `text` to create full post content.

2. **Data Cleaning**  
   - Filled missing values.
   - Removed extremely short or junk posts.

3. **Dynamic Categorization (LLM-driven)**  
   - Posts were sent to an LLM (GPT-3.5-turbo) to dynamically assign a meaningful topic label.
   - Categories were cleaned and grouped for dashboard clarity.

4. **Dashboard Visualization**  
   - A **Streamlit** app was built to:
     - Visualize the distribution of posts by category
     - Allow category selection to view related posts
     - Search posts by keywords

---

## Key Features

- **End-to-End Pipeline**: From raw Reddit data ➔ LLM categorization ➔ cleaned dashboard.
- **Dynamic Topic Modeling**: No hard-coded categories; categories discovered based on real post content.
- **Interactive Dashboard**: Easily explore Tesla Solar customer topics.
- **LLM-Powered Insights**: Categorization powered by GPT models for deeper semantic understanding.

---

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TeslaSolar_Analysis.git
   cd TeslaSolar_Analysis
