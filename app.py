import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.markdown(
    "This application is a streamlit dashboard use to analysis the sentiment of tweets")

DATA_URL = ("tweets.csv")


@st.cache(persist=True)
def load_data(data_url):
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data


data = load_data(DATA_URL)

st.sidebar.subheader("Show random tweet")

random_tweet = st.sidebar.radio(
    'Sentiment', ('positive', "negative", "neutral"))

sb = st.sidebar
sbm = st.sidebar.markdown

ran_tweet = data.query('airline_sentiment == @random_tweet')

sb.markdown(data.query('airline_sentiment == @random_tweet')[
    ["text"]].sample(n=1).iat[0, 0])


sbm("### Number of tweets by sentiment")
select = sb.selectbox('Visualization type', [
                      'Histogram', 'Pie chart'], key='1')

sentiment_count = data['airline_sentiment'].value_counts()


sentiment_count = pd.DataFrame(
    {'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not sb.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment',
                     y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("when and where are the users tweeting from?")
hour = st.sidebar.slider("Hour of Day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("### Tweets locations based on the time of day")
    i = (len(modified_data), hour, (hour+1) % 24)
    st.markdown(f"{i} tweets between {i}:00")
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")

choice = st.sidebar.multiselect(
    "Pick airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment',
                              histfunc='count', color='airline_sentiment', facet_col='airline_sentiment',
                              labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)
