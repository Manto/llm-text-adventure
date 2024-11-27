from together import Together
from llm_text_adventure.helper import get_together_api_key

MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
CLIENT = Together(api_key=get_together_api_key())


def make_completions(messages, temperature=0.4):
    output = CLIENT.chat.completions.create(
        model=MODEL, messages=messages, temperature=temperature
    )

    result = output.choices[0].message.content
    return result
