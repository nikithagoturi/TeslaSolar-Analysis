# TeslaSolar_Analysis

🔗 **Live Dashboard Link**: [Open Tesla Solar Dashboard](https://teslasolar-analysis-cbq4e5eznn8pncenutczqo.streamlit.app/)

---

## Overview

This project analyzes Tesla Solar customer feedback scraped from Reddit between **January 2025 and April 28, 2025**.  
Using Large Language Models (LLMs), the posts are dynamically categorized into major customer topics like system performance issues, installation delays, customer support concerns, and positive experiences.

The results are visualized in an interactive **Streamlit** dashboard for easy exploration and insight generation.

---

## Project Workflow

1. **Data Collection**  
   - Reddit posts related to Tesla Solar were scraped.
   - Data collected from **January 2025 to April 28, 2025**.
   - Script: [`Data_Collection.ipynb`](Data_Collection.ipynb) — contains full Reddit scraping code.

2. **Data Preprocessing and Categorization**  
   - Combined `title` and `text` fields to create full post content.
   - Summarized posts using GPT-3.5-turbo for easier readability.
   - Dynamically categorized posts into meaningful topics using GPT.
   - Grouped messy LLM-generated categories into clean dashboard groups.
   - Script: [`Data_Preprocessing.ipynb`](Data_Preprocessing.ipynb) — contains full GPT categorization and summarization code.

3. **Dashboard Visualization**  
   - A **Streamlit** app was built to:
     - Visualize the distribution of posts by category
     - Drill down by Positive, Negative, Neutral sentiments
     - Explore posts by subcategories inside each sentiment group
     - View summaries and expand to full posts
     - Search posts by keywords

---

## Key Features

- **End-to-End Pipeline**: From raw Reddit data ➔ LLM categorization ➔ cleaned dashboard visualization.
- **Dynamic Topic Modeling**: Categories discovered based on real Reddit content (not manually hardcoded).
- **Post Summarization**: Each post summarized for quicker analysis.
- **Sentiment Analysis**: Posts analyzed as Positive, Neutral, or Negative, with subcategory breakdowns.
- **Interactive Dashboard**: Allows filtering, searching, and drilling down into customer feedback.
- **LLM-Powered Insights**: GPT-3.5 used for dynamic labeling and summarization.
