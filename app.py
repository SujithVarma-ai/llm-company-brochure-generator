import os
import json
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI
from urllib.parse import urljoin, urlparse


MODEL = "llama3.2"

OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

response = ollama.chat.completions.create(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)
print(response.choices[0].message.content)

links = fetch_website_links("https://edwarddonner.com/")
print(links)

# First - make sure which links are relevant for a brochure about the company and which are not.
link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

print(get_links_user_prompt("https://edwarddonner.com/"))


def select_relevant_links(url):
    response = ollama.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    return links
    
print(select_relevant_links("https://edwarddonner.com/"))  

def select_relevant_links(url):
    print(f"Selecting relevant links for {url} by calling {MODEL}")
    response = ollama.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    return links

print(select_relevant_links("https://edwarddonner.com/"))
print(select_relevant_links("https://en.wikipedia.org/wiki/Artificial_intelligence"))


# Second - making brochure
def fetch_page_and_all_relevant_links(url):

    content = fetch_website_contents(url)

    relevant_links = select_relevant_links(url)

    result = f"## Landing Page:\n\n{content}\n## Relevant Links:\n"

    base_domain = urlparse(url).netloc

    for link in relevant_links['links']:

        try:

            full_url = urljoin(url, link["url"])

            parsed = urlparse(full_url)

            # Skip external domains
            if parsed.netloc != base_domain:
                print(f"Skipping external link: {full_url}")
                continue

            print(f"Fetching: {full_url}")

            result += f"\n\n### Link: {link['type']}\n"

            result += fetch_website_contents(full_url)

        except Exception as e:

            print(f"Skipping {link['url']} because: {e}")

    return result

print(fetch_page_and_all_relevant_links("https://en.wikipedia.org/wiki/Artificial_intelligence")[:1000])

brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000] 
    return user_prompt

print(get_brochure_user_prompt("Artificial Intelligence", "https://en.wikipedia.org/wiki/Artificial_intelligence")[:1000])

def create_brochure(company_name, url):
    print(f"Creating brochure for {company_name} by calling {MODEL}")
    response = ollama.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )
    brochure = response.choices[0].message.content
    return brochure

print(create_brochure("Artificial Intelligence", "https://en.wikipedia.org/wiki/Artificial_intelligence"))

# Final 

def stream_brochure(company_name, url):
    stream = ollama.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )
    for chunk in stream:

        content = chunk.choices[0].delta.content or ''

        print(content, end='', flush=True)

    print()
    stream_brochure(
    "Artificial Intelligence",
    "https://en.wikipedia.org/wiki/Artificial_intelligence"
)
