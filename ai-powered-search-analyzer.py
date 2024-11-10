import openai
import requests
# Add your API keys here
BING_API_KEY = 'YOUR_BING_API_KEY'
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
# Set the API key for OpenAI
openai.api_key = OPENAI_API_KEY
def fetch_bing_results(query):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "count": 10}
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    response.raise_for_status()
    return [result['snippet'] for result in response.json().get('webPages', {}).get('value', [])]
def fetch_google_results(query):
    params = {
        "key": GOOGLE_API_KEY,
        "cx": "YOUR_CUSTOM_SEARCH_ENGINE_ID",  # Google Custom Search Engine ID
        "q": query
    }
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    response.raise_for_status()
    return [item['snippet'] for item in response.json().get('items', [])]
def analyze_results_with_openai(bing_results, google_results):
    combined_results = "\n".join(bing_results + google_results)
    prompt = f"Here are some search results for a query:\n\n{combined_results}\n\nProvide a detailed summary of the most relevant information."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()
# Get search query from the user
query = input("Enter your search query: ")
# Fetch Bing and Google results
bing_results = fetch_bing_results(query)
google_results = fetch_google_results(query)
# Analyze and summarize the results
summary = analyze_results_with_openai(bing_results, google_results)
print("\nSummary of Search Results:\n", summary)
