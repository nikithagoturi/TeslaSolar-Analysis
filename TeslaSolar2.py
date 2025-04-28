#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import openai

# Setup
st.set_page_config(page_title="Tesla Solar Analysis", layout="wide")

# Load your final CSV
df = pd.read_csv('tesla_solar_reddit_posts_GroupLabeled.csv')

# Setup OpenAI API key (add yours here)
openai.api_key = 'your-openai-api-key'

# Generate summary if not already there
def summarize_post(post_text):
    prompt = f"Summarize the following Reddit post into 1-2 sentences, highlighting the main issue or event:\n\n{post_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=60
    )
    return response['choices'][0]['message']['content'].strip()

if 'summary' not in df.columns:
    df['summary'] = df['content'].apply(summarize_post)

# Sentiment Analysis
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

df['sentiment'] = df['content'].apply(get_sentiment)

# Sentiment Drilldown
def negative_subcategory(text):
    text = text.lower()
    if 'delay' in text or 'late' in text:
        return 'Delivery/Installation Delay'
    elif 'support' in text or 'service' in text:
        return 'Customer Service Frustration'
    elif 'cancel' in text or 'cancellation' in text:
        return 'Order Cancellation Issues'
    elif 'performance' in text or 'output' in text:
        return 'System Performance Problems'
    elif 'leak' in text or 'roof' in text:
        return 'Roof Quality Issues'
    else:
        return 'Other Negatives'

def positive_subcategory(text):
    text = text.lower()
    if 'installation' in text or 'installed' in text:
        return 'Smooth Installation'
    elif 'output' in text or 'production' in text:
        return 'High Solar Output'
    elif 'support' in text or 'service' in text:
        return 'Good Customer Service'
    elif 'bill' in text or 'savings' in text:
        return 'Energy Bill Savings'
    elif 'hurricane' in text or 'storm' in text:
        return 'Good Resilience in Bad Weather'
    else:
        return 'Other Positives'

df['negative_subcategory'] = df.apply(lambda row: negative_subcategory(row['content']) if row['sentiment'] == 'Negative' else None, axis=1)
df['positive_subcategory'] = df.apply(lambda row: positive_subcategory(row['content']) if row['sentiment'] == 'Positive' else None, axis=1)

# Title
st.title('Tesla Solar Customer Feedback Analysis Dashboard')

st.markdown("""
Welcome to the Tesla Solar customer sentiment and feedback analysis!  
This dashboard dynamically categorizes real Tesla Solar Reddit discussions to uncover insights about system performance, installation experiences, service concerns, and customer happiness.
""")

st.markdown("---")

# Sidebar
st.sidebar.header('Dashboard Controls')
view_option = st.sidebar.radio("Choose view:", ['Overall Analysis', 'Category Analysis', 'Search Posts'])

# Overall view
if view_option == 'Overall Analysis':
    st.header('Distribution of Posts by Category')
    category_counts = df['dashboard_category'].value_counts()
    
    fig, ax = plt.subplots()
    category_counts.plot(kind='bar', color='steelblue', ax=ax)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Number of Posts')
    st.pyplot(fig)

    st.markdown("---")

    st.header('Overall Sentiment Distribution')
    sentiment_counts = df['sentiment'].value_counts()
    
    fig2, ax2 = plt.subplots()
    sentiment_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightskyblue'], ax=ax2)
    plt.ylabel('')
    st.pyplot(fig2)

    st.markdown("---")

    # Drilldown inside Negative Sentiment
    if 'Negative' in sentiment_counts.index:
        st.header('Breakdown of Negative Posts')
        neg_drill = df['negative_subcategory'].value_counts()

        fig3, ax3 = plt.subplots()
        neg_drill.plot(kind='bar', color='lightcoral', ax=ax3)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig3)

        st.markdown("### Explore Negative Subcategories")
        for subcat in neg_drill.index:
            subcat_posts = df[(df['sentiment'] == 'Negative') & (df['negative_subcategory'] == subcat)]

            with st.expander(f"{subcat} ({len(subcat_posts)} posts)"):
                for idx, row in subcat_posts.iterrows():
                    st.write(f"{row['summary']}")

    st.markdown("---")

    # Drilldown inside Positive Sentiment
    if 'Positive' in sentiment_counts.index:
        st.header('Breakdown of Positive Posts')
        pos_drill = df['positive_subcategory'].value_counts()

        fig4, ax4 = plt.subplots()
        pos_drill.plot(kind='bar', color='lightgreen', ax=ax4)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig4)

        st.markdown("### Explore Positive Subcategories")
        for subcat in pos_drill.index:
            subcat_posts = df[(df['sentiment'] == 'Positive') & (df['positive_subcategory'] == subcat)]

            with st.expander(f"{subcat} ({len(subcat_posts)} posts)"):
                for idx, row in subcat_posts.iterrows():
                    st.write(f"{row['summary']}")

    st.markdown("---")

    # Drilldown inside Neutral Sentiment
    if 'Neutral' in sentiment_counts.index:
        st.header('Breakdown of Neutral Posts')
        neutral_posts = df[df['sentiment'] == 'Neutral']

        with st.expander(f"Neutral Posts ({len(neutral_posts)} posts)"):
            for idx, row in neutral_posts.iterrows():
                st.write(f"{row['summary']}")

    st.markdown("---")

    st.markdown("### Key Insight Summary")
    st.success(f"Top Category: {category_counts.idxmax()} ({category_counts.max()} posts)")
    st.success(f"Overall Customer Sentiment: {sentiment_counts.idxmax()}")

# Category view
elif view_option == 'Category Analysis':
    st.header('Explore Posts by Category')
    selected_category = st.selectbox('Select a Category', df['dashboard_category'].unique())

    filtered_posts = df[df['dashboard_category'] == selected_category]

    st.subheader(f"Summarized Posts under **{selected_category}**:")

    for idx, row in filtered_posts.iterrows():
        st.write(f"{row['summary']}")
        
    st.markdown("---")
    st.header(f'Word Cloud for {selected_category}')
    category_text = ' '.join(filtered_posts['content'].tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(category_text)
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.imshow(wordcloud, interpolation='bilinear')
    ax5.axis('off')
    st.pyplot(fig5)

# Search view
else:
    st.header('Search Posts')
    search_keyword = st.text_input('Enter a keyword to search:')

    if search_keyword:
        search_results = df[df['content'].str.contains(search_keyword, case=False, na=False)]
        st.write(f"### Posts containing **{search_keyword}**:")
        for idx, row in search_results.iterrows():
            st.write(f"- {row['summary']}")
            with st.expander("See Full Post"):
                st.write(row['content'])


# In[ ]:




