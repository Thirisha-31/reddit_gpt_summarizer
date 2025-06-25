import streamlit as st
import praw
import openai

# UI
st.title("Reddit GPT Summarizer")
reddit_url = st.text_input("Enter Reddit post URL")

if reddit_url:
    # Setup Reddit
    reddit = praw.Reddit(
        client_id=st.secrets["reddit"]["client_id"],
        client_secret=st.secrets["reddit"]["client_secret"],
        username=st.secrets["reddit"]["username"],
        password=st.secrets["reddit"]["password"],
        user_agent=st.secrets["reddit"]["user_agent"]
    )

    openai.api_key = st.secrets["openai"]["api_key"]

    try:
        submission = reddit.submission(url=reddit_url)
        submission.comments.replace_more(limit=0)
        top_comments = [comment.body for comment in submission.comments[:5]]

        prompt = "Summarize the following Reddit comments:\n" + "\n".join(top_comments)

        with st.spinner("Summarizing with GPT..."):
            client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
            )


        st.subheader("💬 GPT Summary")
        st.write(response.choices[0].message.content)


    except Exception as e:
        st.error(f"Error: {e}")
