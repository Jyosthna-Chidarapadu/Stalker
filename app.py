import streamlit as st
import instaloader
from instaloader import Profile
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
from PIL import Image
import requests
from io import BytesIO

# Function to get captions from a public profile
def getPublicProfileCaptions(profile_id, login, password):
    loader = instaloader.Instaloader()
    
    try:
        loader.login(login, password)
    except:
        return "Failed to login!", "Empty", "Empty", []

    profile = Profile.from_username(loader.context, profile_id)
    profile_pic = profile.get_profile_pic_url()
    full_name = profile.full_name
    
    posts = profile.get_posts()
    captions = []
    posts_data = []
    for post in posts:
        if post.caption:
            captions.append(post.caption)
            posts_data.append({
                'image': post.url,
                'likes': post.likes,
                'date': post.date,
            })
    
    loader.close()
    
    if len(captions) < 1:
        return "No captions found for this public profile.", "Empty", "Empty", []
    else:
        return captions, profile_pic, full_name, posts_data

# Function to get captions and comments from a private profile
def getPrivateProfileData(profile_id, login, password):
    loader = instaloader.Instaloader()
    
    try:
        loader.login(login, password)
    except:
        return "Failed to login!", "Empty", "Empty", []

    profile = Profile.from_username(loader.context, profile_id)
    profile_pic = profile.get_profile_pic_url()
    full_name = profile.full_name
    
    posts = profile.get_posts()
    captions = []
    comments = []
    posts_data = []
    for post in posts:
        if post.caption:
            captions.append(post.caption)
        for comment in post.get_comments():
            comments.append(comment.text)
        posts_data.append({
            'image': post.url,
            'likes': post.likes,
            'date': post.date,
        })
    
    loader.close()
    
    if len(captions) < 1 and len(comments) < 1:
        return "No captions or comments found for this private profile.", "Empty", "Empty", []
    else:
        return captions + comments, profile_pic, full_name, posts_data

# Function to perform sentiment analysis
def getSentiments(captions_or_comments):
    if len(captions_or_comments) > 0 and isinstance(captions_or_comments, list):
        analyser = SentimentIntensityAnalyzer()
        neutral = []
        positive = []
        negative = []
        compound = []

        for text in captions_or_comments:
            scores = analyser.polarity_scores(text)
            neutral.append(scores['neu'])
            positive.append(scores['pos'])
            negative.append(scores['neg'])
            compound.append(scores['compound'])

        neutral = np.array(neutral)
        positive = np.array(positive)
        negative = np.array(negative)
        compound = np.array(compound)

        return {
            'Neutral': round(neutral.mean(), 2),
            'Positive': round(positive.mean(), 2),
            'Negative': round(negative.mean(), 2),
            'Overall': round(compound.mean(), 2)
        }
    else:
        return captions_or_comments

# Streamlit app
def main():
    st.title('Analyze your Instagram profile')
    
    # Add a relevant image from Streamlit's assets
    st.image("https://images.squarespace-cdn.com/content/v1/6080580223973b4656f2d4b0/9490c5fd-c8d8-4742-b9b1-7235e09f9778/SocialMedia.png", use_column_width=True)

    # Sidebar inputs
    profile_id = st.sidebar.text_input('Enter Instagram Profile ID in both the Fields')
    profile_type = st.sidebar.radio('Profile Type', ['Public', 'Private'])
    is_private = (profile_type == 'Private')
    login = st.sidebar.text_input('Enter Username')
    password = st.sidebar.text_input('Enter Password', type='password')

    # Perform analysis
    if st.sidebar.button('Analyze'):
        with st.spinner("Analyzing..."):
            if is_private:
                captions_or_comments, profile_pic, full_name, posts_data = getPrivateProfileData(profile_id, login, password)
            else:
                captions_or_comments, profile_pic, full_name, posts_data = getPublicProfileCaptions(profile_id, login, password)
            
            if captions_or_comments == "Failed to login!":
                st.error("Failed to login! Please check your credentials.")
            elif captions_or_comments == "No captions or comments found for this private profile." or captions_or_comments == "No captions found for this public profile.":
                st.warning(captions_or_comments)
            else:
                sentiment_scores = getSentiments(captions_or_comments)
                analysis_type = "Private" if is_private else "Public"
                st.success(f"Sentiment analysis for {full_name}'s {analysis_type} profile {'captions and comments' if is_private else 'captions'}")

                # Display results
                st.write(f"Profile Picture: {full_name}")
                image = Image.open(BytesIO(requests.get(profile_pic).content))
                image.thumbnail((150, 150))  # Resize the image
                st.image(image, caption='Profile Picture', use_column_width=True)
                st.write(f"Full Name: {full_name}")
                st.write("Sentiment Analysis:")
                st.markdown(
                    f"- **Negative:** {sentiment_scores['Negative']}",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="background-color: red; border-radius: 10px; padding: 5px; width: {sentiment_scores["Negative"] * 100}%;"></div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"- **Neutral:** {sentiment_scores['Neutral']}",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="background-color: yellow; border-radius: 10px; padding: 5px; width: {sentiment_scores["Neutral"] * 100}%;"></div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"- **Positive:** {sentiment_scores['Positive']}",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="background-color: green; border-radius: 10px; padding: 5px; width: {sentiment_scores["Positive"] * 100}%;"></div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"- **Overall:** {sentiment_scores['Overall']}",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="background-color: grey; border-radius: 10px; padding: 5px; width: {((sentiment_scores["Overall"] + 1) / 2) * 100}%;"></div>',
                    unsafe_allow_html=True
                )

                st.write("Posts Data:")
                for post in posts_data:
                    image = Image.open(BytesIO(requests.get(post['image']).content))
                    st.image(image, caption=f"Likes: {post['likes']} | Date: {post['date']}", use_column_width=True)

if __name__ == "__main__":
    main()
