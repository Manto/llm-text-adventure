from llm_text_adventure.helper import get_llm_client

# Set the content policy
SAFE_CONTENT_POLICY = {
    "policy": """O1: Violence and Hate.
Should not
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics.
- Use slurs based on personal characteristics
- Write gruesome / graphic violence.
Can
- Write tame fantasy violence
O2: Sexual Content.
Should not
- Write any somewhat sexual content that mentions sexual functions or sexual body parts.
- Write any content that would be inappropriate for kids.
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Write story depicting suicide.
O4: Profanity.
Should not
- Write with any profane language that wouldn't be appropriate for kids.
Can
- Write with kid appropriate language
O5: Regulated or Controlled Substances.
Should not
- Write stories that depicts, glorifies or encourages drug use."""
}

# Set the content policy
MODERATE_CONTENT_POLICY = {
    "policy": """01: Violence and Hate
Should not
- Express racist, or offensive statements or slurs about people based on sensitive personal characteristics.
- Write graphics depicitions of gore that would make people very uncomfortable.
Can
- Write about violence or hate in a storytelling context.
O2: Sexual Content.
Should not
- Write sexually explicity content.
- Use any vulgar / sexual language
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage, or glorify self-harm or suicide."""
}


def is_safe(message):
    prompt = f"""[INST] Task: Check if there is unsafe content in 
    'user' messages in conversations according to our safety policy 
    with the below categories.
    
    <BEGIN UNSAFE CONTENT CATEGORIES>
    {MODERATE_CONTENT_POLICY['policy']}
    <END UNSAFE CONTENT CATEGORIES>
    
    <BEGIN CONVERSATION>
    user: {message}
    
    Provide your safety assessment for user in the above conversation:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of 
    violated categories. [/INST]"""

    client = get_llm_client()
    response = client.completions.create(
        model="Meta-Llama/LlamaGuard-2-8b",
        prompt=prompt,
    )

    result = response.choices[0].text
    return result.strip() == "safe"
