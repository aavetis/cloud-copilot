# Cloud Copilot

**_Super beta and unofficial!_**

Cloud Copilot is a command-line interface (CLI) tool that allows users to interact with cloud resources using natural language input. The tool is built with Python and uses OpenAI's GPT-3.5 turbo chat model to generate cloud CLI commands from the user's input.

Currently, Cloud Copilot supports Azure by default, but it can be easily extended to work with other cloud providers, such as AWS or GCP.

## Things to add

- Include more cloud providers
- Look up embedded CLI docs for additional factuality, grounding, and updates
- Markdown rendering with Rich (while still supporting streaming responses)

Please [create an issue](https://github.com/aavetis/cloud-copilot/issues) for any other suggestions.

## Installation

1. Clone the repository

2. Create a virtual environment and activate it (suggested)

```
python -m venv venv
source venv/bin/activate # For Linux or macOS
.\venv\Scripts\activate # For Windows
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Copy the `.env.example` file to `.env` - add your OpenAI API key and other environment variables:

```
cp .env.example .env
```

## Usage

Run the Cloud Copilot CLI tool using the following command:

```
python main.py
```
