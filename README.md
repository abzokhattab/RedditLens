# RedditLens 
**RedditLens**  is a Streamlit application that retrieves and analyzes Reddit posts on a given topic using the Reddit API. It then generates a weighted summary of community insights using a locally running large language model (LLM) through [Ollama](https://ollama.ai/) .
## Features 
 
- **Topic-Specific Reddit Fetch** : Enter any keyword or phrase to gather relevant posts from across Reddit.
 
- **Weighted Analysis** : Sort and rank results based on logarithmically scaled scores, ensuring high-engagement posts receive greater emphasis without overshadowing niche insights.
 
- **Local LLM Integration** : If you have Ollama running, the tool can generate automated summaries of the top posts.
 
- **Markdown Output** : A clear, structured Markdown report is displayed and can be downloaded directly.


---


## Prerequisites 
 
1. **Python 3.7+**
 
2. **[Streamlit](https://streamlit.io/) **  (install via `pip install streamlit`)
 
3. **[praw](https://pypi.org/project/praw/) **  for Reddit API access (install via `pip install praw`)
 
4. **[Ollama](https://ollama.ai/) **  for local LLM inference


---


## Installation 
 
1. **Clone or Download this Repository** 

```bash
git clone https://github.com/abzokhattab/RedditLens.git
cd redditlens
```
 
2. **Install Required Python Packages** 

```bash
pip install -r requirements.txt
```
(If a `requirements.txt` file is provided, otherwise install individually: `pip install streamlit praw`)
 
3. **Install Ollama and at least one model** 
Installation instructions for Ollama may differ based on your operating system. For most Unix-like systems:

```bash
curl https://ollama.ai/install.sh | sh
```

Then, pull a language model (e.g., Llama 2):


```bash
ollama pull llama2
```


---


## Configuration 

### Reddit API Credentials 

By default, the application has some test credentials set in the code, but you are strongly encouraged to use your own:
 
1. Visit [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) .
 
2. Click **Create another app**  and fill out the required details (script type).
 
3. **Note down your Client ID and Client Secret** .
 
4. In `app.py` (or wherever your code references them), update the variables:

```python
APP_ID = "your_client_id_here"
APP_SECRET = "your_client_secret_here"
USER_AGENT = "your_user_agent"
```


---


## Usage 
 
1. **Start the Ollama service**  (in a separate terminal window or tab):

```bash
ollama serve
```
 
2. **Run the Streamlit application**  from the project directory:

```bash
streamlit run app.py
```
 
3. **Access the Web App** 
After a few moments, a local URL (e.g., `http://localhost:8501`) will appear in your terminal. Open that URL in your browser.


---


## Application Flow 
 
1. **Input**  
  - **Topic** : Enter any topic or phrase in the text field (e.g., “Sustainable Fashion,” “Remote Work,” etc.).
 
  - **Number of Posts** : Select how many Reddit posts to retrieve (1–20).
 
  - **Model Selection** : If multiple Ollama models are installed, pick the one you want to use for summaries.
 
2. **Processing** 
  - The application calls the Reddit API using your provided or default credentials.

  - It retrieves the specified number of posts, computes a logarithmic weight for each post based on its score, and sorts them in descending order.
 
3. **Output**  
  - **Score Distribution** : Shows total combined score, highest and lowest scores.
 
  - **Posts by Popularity** : Renders each post with its score, subreddit, and relative weight.
 
  - **AI Analysis**  (if Ollama is running): Summarizes the top community sentiments, outliers, and overall trends.
 
4. **Download**  
  - A **Download Analysis**  button allows you to save the Markdown report for offline viewing or further distribution.


---


## POC 



https://github.com/user-attachments/assets/772a98bf-371f-41e3-b9ac-4c27a73b095b




## License 
This project is released under the [MIT License]() . Feel free to use or modify the code according to the terms of the license.

