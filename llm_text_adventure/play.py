import gradio as gr
from llm_text_adventure.helper import load_world
from llm_text_adventure.llm import make_completions
import random

demo = None  # added to allow restart


def start_game(main_loop, share=False):
    # added code to support restart
    global demo
    # If demo is already running, close it first
    if demo is not None:
        demo.close()

    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=800, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(
            placeholder="What do you do next?", container=False, scale=7
        ),
        title="Dystopian Adventure Game",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
    )
    demo.launch(share=share, server_name="0.0.0.0")


world = load_world("world.json")
# Select a random element from the list of cities
current_city = random.choice(list(world["cities"].values()))
current_location = random.choice(list(current_city["locations"].values()))
character = random.choice(list(current_location["npcs"].values()))

game_state = {
    "world": world["description"],
    "current_city": current_city,
    "current_location": current_location,
    "character": character["description"],
}


def main_loop(message, history):
    return run_action(message, history, game_state)


def run_action(message, history, game_state):

    if message == "start game":
        ## Start the game
        system_prompt = """You are an AI Game master. Your job is to create a 
start to an adventure based on the world, kingdom, town and character 
a player is playing as. 
Instructions:
You must only use 2-4 sentences \
Write in second person. For example: "You are Jack" \
Write in present tense. For example "You stand at..." \
First describe the character and their backstory. \
Then describes where they start and what they see around them."""

        world_info = f"""
World:
{world}

City:
{current_city}

Location:{current_location}
"""
        result = make_completions(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": world_info + "\nYour Start:"},
            ]
        )
        return result

    system_prompt = f"""You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.\

You must on only write 1-3 sentences in response.
Your writing style is {world['style']}.
The mood of the story is {world['mood']}.
Always write in second person present tense.
Ex. (You look north and see...)"""

    world_info = f"""
World:
{world}

City:
{current_city}

Location:{current_location}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info},
    ]
    for action in history:
        messages.append({"role": "assistant", "content": action[0]})
        messages.append({"role": "user", "content": action[1]})

    messages.append({"role": "user", "content": message})
    result = make_completions(messages)
    return result


start_game(main_loop)
