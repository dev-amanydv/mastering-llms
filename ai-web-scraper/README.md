<div align="center">

# AI Web Scraper & Summarizer

A powerful, lightweight Python tool that scrapes website content and generates concise, professional summaries using local LLMs (Ollama) or cloud APIs.

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-black?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration)

</div>

---

## Features

- **Intelligent Summarization:** Uses advanced LLMs (like Qwen 2.5) to digest complex web content.
- **Local Privacy:** Run entirely offline with Ollama for maximum data privacy.
- **Cloud Ready:** Compatible with OpenAI-style APIs (Groq, OpenAI, etc.).
- **Clean Extraction:** Automatically filters out ads, navigation, and boilerplate noise.
- **CLI Interface:** Simple, easy-to-use command line interface.

## Prerequisites

- **Python 3.10+**: Ensure you have Python installed.
- **Ollama**: Required for local inference (recommended).

## Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/web-scraper.git
    cd web-scraper
    ```

2.  **Set Up Virtual Environment**

    ```bash
    # Create virtual environment
    python -m venv .venv

    # Activate it
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

##  Usage

### Option 1: Run Locally with Ollama (Free & Private)

This is the default configuration. It requires running the Ollama server locally.

1.  **Install Ollama:** Download and install from [ollama.com](https://ollama.com/).
2.  **Pull the Model:** The project defaults to `qwen2.5-coder:3b`. Run this command in your terminal:

    ```bash
    ollama pull qwen2.5-coder:3b
    ```

    _(Note: You can change the model in `main.py` if you prefer another one like `llama3` or `mistral`)_

3.  **Start the Scraper:**
    Make sure Ollama is running, then execute:

    ```bash
    python main.py
    ```

4.  **Enter URL:** Paste any website URL when prompted, and watch the AI summarize it!

### Option 2: Run with API Keys (OpenAI, Groq, etc.)

If you prefer using a cloud provider for faster inference or better models, you can configure the script to use an API key.

1.  **Open `main.py`** in your code editor.
2.  **Update the Configuration Constants** at the top of the file:

    ```python
    # Example for OpenAI
    OLLAMA_MODEL = "gpt-4o-mini"
    OLLAMA_BASE_URL = "https://api.openai.com/v1"
    API_KEY = "sk-your-openai-api-key-here"
    ```

    Or for **Groq**:

    ```python
    OLLAMA_MODEL = "llama3-70b-8192"
    OLLAMA_BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = "gsk-your-groq-api-key-here"
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## Project Structure

```
├── main.py          # Entry point & AI integration logic
├── scraper.py       # Web scraping & content cleaning logic
├── requirements.txt # Python dependencies
└── README.md        # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
