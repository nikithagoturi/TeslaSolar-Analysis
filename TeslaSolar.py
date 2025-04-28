#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your final CSV
df = pd.read_csv('tesla_solar_reddit_posts_labeled2.csv')

# Title
st.title('Tesla Solar Customer Feedback Dashboard')

st.markdown("""
This dashboard analyzes Tesla Solar customer discussions scraped from Reddit posts.
The posts have been dynamically categorized using an LLM into major themes.
""")

# Show overall category distribution
st.header('Distribution of Posts by Topic')

category_counts = df['dashboard_category'].value_counts()

# Bar chart
fig, ax = plt.subplots()
category_counts.plot(kind='bar', color='skyblue', ax=ax)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Select a category
st.header('View Posts by Category')

selected_category = st.selectbox('Select a Category', category_counts.index)

# Filter posts
filtered_posts = df[df['dashboard_category'] == selected_category]

st.write(f"### Posts under **{selected_category}**:")
for idx, row in filtered_posts.iterrows():
    st.write(f"- {row['content']}")

# (Optional) Search by keyword
st.header('Search Posts')
search_keyword = st.text_input('Enter a keyword to search:')

if search_keyword:
    search_results = df[df['content'].str.contains(search_keyword, case=False, na=False)]
    st.write(f"### Posts containing **{search_keyword}**:")
    for idx, row in search_results.iterrows():
        st.write(f"- {row['content']}")


# In[ ]:




