# Builds world data

from llm_text_adventure.helper import save_world
from llm_text_adventure.llm import make_completions
import json

BUILDER_SYSTEM_PROMPT = f"""
You are a award-winning dystopian sci-fi novelist. You have been tasked with creating a new world for an interactive story.
"""


def build():
    world = {
        "description": """In the year 2055, humanity stands at a crossroads. The world we once knew has been reshaped by the relentless march of climate change and technological progress. Coastal cities are threatened by frequent floods exacerbated by rising seas, their former inhabitants now unwelcome wanderers in a world grown hostile to the displaced. Europe shivers under an unprecedented deep freeze, while tropical regions are battered by near-constant storms.

The promise of artificial intelligence, once heralded as our salvation, has proven a double-edged sword. Robots and automation have revolutionized industry and daily life, but at a steep environmental cost. The pursuit of ever-more-powerful AI has accelerated climate change, even as it fails to achieve the long-sought goal of artificial general intelligence.

In this brave new world, productivity soars while birthrates plummet. An aging population finds itself increasingly obsolete, retreating into virtual realities and AI companionship. The gap between the tech-savvy elite and those left behind widens daily. Despite unprecedented technological marvels, famine and disease still plague many corners of the globe.

Humanity finds itself paralyzed, caught between complacency and fear. Some cling desperately to the familiar, while others lose themselves in digital escapes. Tensions simmer as nations close their borders to climate refugees, sparking conflicts and humanitarian crises. Yet beneath the surface, a deeper tension builds – a growing realization that something must change. In this world of environmental chaos and technological wonder, a few dare to ask: can we reclaim our humanity and forge a new path forward? Or are we doomed to be swept away by the very forces we've unleashed?
""",
        "mood": "hard-boiled pulp-fiction novel",
        "style": "show don't tell, use mix of short-and-medium length sentences, keep paragraphs very short",
    }

    NUM_CITIES = 3

    city_prompt = f"""
Create {NUM_CITIES} different cities for a dystopian sci-fi world described below.
For each city generate a description based on the world it's in.
Describe important leaders, cultures, history of the city.\

{get_sub_world_prompt(world)}

Generate your response as a strictly formatted JSON object with the following structure, without any additional text wrapping like ```:
{{
  "name": "<city_name>",
  "description": "<city_description>"
}}"""

    cities_output = make_completions(
        [
            {"role": "system", "content": BUILDER_SYSTEM_PROMPT},
            {"role": "user", "content": city_prompt},
        ]
    )

    cities = json.loads(cities_output)
    cities = {city["name"]: city for city in cities}

    for city in cities.values():
        create_locations(world, city)

    for city in cities.values():
        for location in city["locations"].values():
            create_npcs(world, city, location)

    world["cities"] = cities

    save_world(world, "world.json")


def get_sub_world_prompt(world):
    return f"""
The description of the world is:
{world['description']}
"""


def get_sub_city_prompt(city):
    return f"""
The locations are inside the city of {city['name']}.
The description of the city is:
{city['description']}
"""


def get_sub_location_prompt(location):
    return f"""
The characters are located in {location['name']}.
The description of the location is:
{location['description']}
"""


def get_location_prompt(world, city, count=3):
    return f"""
Create {count} different locations for a dystopian sci-fi world.

{get_sub_city_prompt(city)}

{get_sub_world_prompt(world)}

Generate your response as a strictly formatted JSON object with the following structure, without any additional text wrapping like ```:
{{
  "name": "<location_name>",
  "description": "<location_description>"
}}"""


def create_locations(world, city):
    print(f'\nCreating locations for city: {city["name"]}...')

    locations_output = make_completions(
        [
            {"role": "system", "content": BUILDER_SYSTEM_PROMPT},
            {"role": "user", "content": get_location_prompt(world, city)},
        ]
    )

    locations = json.loads(locations_output)
    # Convert list of locations to a dictionary
    locations = {location["name"]: location for location in locations}
    city["locations"] = locations


def get_npc_prompt(world, city, location, count=3):
    return f"""
Create {count} different characters based on the world, city \
and location they're in. Describe the character's appearance and \
profession, as well as their deeper pains and desires.

{get_sub_location_prompt(location)}

{get_sub_city_prompt(city)}

{get_sub_world_prompt(world)}

Generate your response as a strictly formatted JSON object with the following structure, without any additional text wrapping like ```:
{{
  "name": "<character_name>",
  "description": {
    "appearance": "<character_appearance>",
    "profession": "<character_profession>",
    "pain": "<character_pain>",
    "desire": "<character_desire>"
  }
}}"""


def create_npcs(world, city, location):
    print(f'\nCreating characters for the location of: {location["name"]}...')
    npc_output = make_completions(
        messages=[
            {"role": "system", "content": BUILDER_SYSTEM_PROMPT},
            {"role": "user", "content": get_npc_prompt(world, city, location)},
        ],
    )

    npcs = json.loads(npc_output)
    # Convert list of npcs to a dictionary
    npcs = {npc["name"]: npc for npc in npcs}
    location["npcs"] = npcs


build()
