# AI Company Brochure Generator

An AI-powered Company Brochure Generator that analyzes company websites and automatically creates professional business brochures using local Large Language Models (LLMs) through Ollama.

* Ollama
* Llama 3.2
* OpenAI Compatible API
* Python
* Web Scraping

## Features

* Extracts website links
* Detects relevant and non-relevant company pages
* Fetches company website content
* Generates professional AI brochures
* Runs fully locally using Ollama

## Tech Stack

* Python
* Ollama
* OpenAI Python SDK
* BeautifulSoup
* Local LLMs

## Installation

```bash
pip install openai python-dotenv beautifulsoup4 requests
```

Install Ollama:

https://ollama.com

Pull model:

```bash
ollama pull llama3.2
```

Run:

```bash
python ollamacompanybrochure.py
```
## Screenshot

![App Screenshot](https://github.com/SujithVarma-ai/llm-company-brochure-generator/blob/main/Screenshot%202026-05-26%20195820.png)
![App Screenshot](https://github.com/SujithVarma-ai/llm-company-brochure-generator/blob/main/Screenshot%202026-05-26%20195933.png)
![App Screenshot](https://github.com/SujithVarma-ai/llm-company-brochure-generator/blob/main/Screenshot%202026-05-26%20200153.png)
![App Screenshot](https://github.com/SujithVarma-ai/llm-company-brochure-generator/blob/main/Screenshot%202026-05-26%20200240.png)
![App Screenshot](https://github.com/SujithVarma-ai/llm-company-brochure-generator/blob/main/Screenshot%202026-05-26%20200317.png)


## Example

Input:

* Company Name
* Website URL

Output:

* AI-generated business brochure

## Future Improvements

* Streamlit UI
* Gradio Chat Interface
* Multi-model support
* PDF brochure export
* RAG integration
