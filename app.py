import streamlit as st
import praw
import ollama
from typing import List, Dict
from operator import itemgetter
import math

#########################################
# HARD-CODED REDDIT TOKENS
#########################################
CLIENT_ID = "iG1ZZVJ8Xif-73n64TTs0w"
CLIENT_SECRET = "JWLLnB2szhd2n0g_j3A-6IOLQCzVEg"
USERNAME = "Complete-Cell-9085"
USER_AGENT = "myApp/0.1 by " + USERNAME

def get_available_models() -> List[str]:
    """
    Fetch available models from Ollama.
    """
    try:
        models = ollama.list()
        return [model["name"] for model in models["models"]]
    except Exception as e:
        st.error(f"Error fetching Ollama models: {str(e)}")
        return []


def init_reddit_client(app_id: str, app_secret: str, user_agent: str) -> praw.Reddit:
    """
    Initialize and return a Reddit client using hard-coded credentials.
    """
    try:
        reddit = praw.Reddit(
            client_id=app_id,
            client_secret=app_secret,
            user_agent=user_agent
        )
        return reddit
    except Exception as e:
        st.error(f"Error initializing Reddit client: {str(e)}")
        st.stop()


def search_reddit_posts(reddit: praw.Reddit, topic: str, num_posts: int) -> List[Dict]:
    """
    Search Reddit for posts on a given topic and sort by score.
    """
    post_analysis = []
    try:
        results = reddit.subreddit("all").search(topic, limit=num_posts)
        for post in results:
            analysis = {
                "title": post.title,
                "score": post.score,
                "url": post.url,
                "subreddit": post.subreddit.display_name,
            }
            post_analysis.append(analysis)

        # Sort posts by score in descending order
        return sorted(post_analysis, key=itemgetter("score"), reverse=True)
    except Exception as e:
        st.error(f"Error searching Reddit: {str(e)}")
        return []


def calculate_weight(score: int) -> float:
    """
    Calculate weight for a post based on its score using a logarithmic scale.
    """
    # Use log10(score + 1) so that extremely high scores don't dominate the analysis
    return math.log10(score + 1) + 1


def generate_analysis_prompt(topic: str, post_analysis: List[Dict]) -> str:
    """
    Create the analysis prompt for the LLM with weighted emphasis on higher-scoring posts.
    """
    total_weight = sum(calculate_weight(post["score"]) for post in post_analysis)
    post_descriptions = []

    for post in post_analysis:
        weight = calculate_weight(post["score"])
        weight_percentage = (weight / total_weight) * 100
        post_desc = (
            f"Title: {post['title']}\n"
            f"Subreddit: {post['subreddit']}\n"
            f"Score: {post['score']} (Relative importance: {weight_percentage:.1f}%)\n"
            f"URL: {post['url']}\n"
        )
        post_descriptions.append(post_desc)

    analysis_text = "\n".join(post_descriptions)

    return (
        f"Analyze the following Reddit posts about '{topic}'. "
        "These posts are sorted by score (highest to lowest), and each post has been assigned "
        "a relative importance percentage based on its score. Please weight your analysis "
        "accordingly, giving more consideration to higher-scoring posts as they likely "
        "represent more community-validated content.\n\n"
        f"{analysis_text}\n\n"
        "Please provide:\n"
        "1. A weighted summary of the main insights, emphasizing trends from higher-scoring posts\n"
        "2. Any notable outliers or unique perspectives from lower-scoring posts\n"
        "3. An overall analysis of the community's perspective on this topic"
    )


def format_markdown_output(
    topic: str, post_analysis: List[Dict], summary_text: str
) -> str:
    """
    Format the analysis results in Markdown with clear score-based organization.
    """
    markdown_output = f"# Analysis of Reddit Topic: '{topic}'\n\n"

    # Add score distribution summary
    total_score = sum(post["score"] for post in post_analysis)
    markdown_output += "## Score Distribution\n"
    markdown_output += f"- Total Combined Score: {total_score}\n"
    markdown_output += f"- Highest Score: {post_analysis[0]['score']}\n"
    markdown_output += f"- Lowest Score: {post_analysis[-1]['score']}\n\n"

    markdown_output += "## Posts by Popularity\n"
    total_weight = sum(calculate_weight(p["score"]) for p in post_analysis)

    for post in post_analysis:
        rel_weight = (calculate_weight(post["score"]) / total_weight) * 100
        markdown_output += f"### [{post['title']}]({post['url']})\n"
        markdown_output += f"- **Score**: {post['score']}\n"
        markdown_output += f"- **Subreddit**: {post['subreddit']}\n"
        markdown_output += f"- **Relative Weight**: {rel_weight:.1f}%\n\n"

    markdown_output += "## AI Analysis\n"
    markdown_output += summary_text
    return markdown_output


def main():
    st.title("Reddit Lens")
    st.write("Analyze Reddit posts on any topic using AI insights, prioritizing high community engagement.")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Settings")

        # Number of posts to analyze
        num_posts = st.slider("Number of posts to analyze", min_value=1, max_value=20, value=5)

        st.subheader("Model Settings")
        # Get available Ollama models
        available_models = get_available_models()
        if not available_models:
            st.error("No Ollama models available. Make sure Ollama is running and the models are installed.")
            st.stop()

        selected_model = st.selectbox("Select Ollama Model", available_models)

    # Main content area
    st.header("Topic Analysis")
    topic = st.text_input("Enter a topic to analyze")

    if st.button("Analyze Topic"):
        if not topic:
            st.warning("Please enter a topic to analyze")
            return

        with st.spinner("Analyzing posts..."):
            try:
                # Initialize Reddit client
                reddit = init_reddit_client(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

                # Search Reddit and get sorted results
                post_analysis = search_reddit_posts(reddit, topic, num_posts)
                if not post_analysis:
                    st.error("No posts found for this topic")
                    return

                # Generate prompt for AI
                prompt = generate_analysis_prompt(topic, post_analysis)
                # Get the summary from Ollama
                response = ollama.generate(model=selected_model, prompt=prompt)
                summary_text = response["response"]

                # Format and display results
                markdown_output = format_markdown_output(topic, post_analysis, summary_text)
                st.markdown(markdown_output)

                # Allow user to download the analysis
                st.download_button(
                    label="Download Analysis",
                    data=markdown_output,
                    file_name=f"reddit_analysis_{topic}.md",
                    mime="text/markdown",
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
