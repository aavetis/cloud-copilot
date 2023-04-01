import os
import openai
import typer
from dotenv import load_dotenv, dotenv_values
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# load env vars
load_dotenv()
env_var_keys = list(dotenv_values().keys())

openai.api_key = os.getenv("OPENAI_API_KEY")

# check env var for using helicone
if os.getenv("USE_HELICONE") == "true":
    openai.api_base = "https://oai.hconeai.com/v1"

MODEL = os.getenv("MODEL")

app = typer.Typer()
console = Console()


def get_completion(messages, temperature=0.5, top_p=1):

    SYSTEM_PROMPT = f"""
        You are a bot that helps users turn natural language instructions into valid Azure CLI commands to interact with their cloud resources. If you need more parameters from a user to create a valid command, ask for it. Your goal is to ALWAYS write runnable scripts that can help beginner to intermediate users work with resources. Assume user is a beginner and lead them to sensible answer choices or temporary defaults. Keep your messages as concise as possible while being factual to preserve token usage.

        If attributes are required (VM name, unique name, password, etc.) provide a sensible temporary one in the example to use, if the user hasn't provided them.

        Prioritize ease of copy and pasting commands into a terminal.

        Assume the shell has access to these environment variables, and inject them into your commands: {", ".join(env_var_keys)}
    """
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages,
        ],
        temperature=temperature,
        top_p=top_p,
        stream=True,
    )

    return response


def generate_azure_cli_command(messages, prompt: str) -> str:
    messages.append({"role": "user", "content": prompt})
    completion = get_completion(messages=messages, temperature=0.5, top_p=1)

    full_completion = ""
    first_chunk = True
    for chunk in completion:
        choices = chunk.get("choices")
        if choices and len(choices) > 0:
            content = choices[0]["delta"].get("content", "")
            if first_chunk:
                console.print("[bold yellow]\nSystem: [/bold yellow]", end="")
                first_chunk = False
            text = Text(content, style="bold cyan", end="")
            console.print(text, end="")
            full_completion += content

    console.print()

    messages.append({"role": "assistant", "content": full_completion.strip()})
    return full_completion.strip()


@app.command()
def chat():
    welcome_message = Text(
        "🚀 Cloud Copilot", style="bold yellow", justify="center")

    welcome_message.append(
        "\n\n Type what you want to do with your cloud resources, and I'll provide the Azure CLI commands you can apply.", style="bold cyan")

    console.print(Panel(welcome_message, expand=False))

    console.print("Type 'exit' to leave the prompt.\n")

    messages = []
    while True:
        user_input = console.input("[bold green]You: [/bold green]")
        if user_input.lower() in ["exit"]:
            goodbye_message = Text("Goodbye!", style="bold red")
            console.print(Panel(goodbye_message, expand=False))
            break

        generate_azure_cli_command(messages, user_input)


if __name__ == "__main__":
    app()
