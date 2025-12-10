from google import genai
from google.genai import types
import json
import re

SYSTEM_INSTRUCTIONS = """
You are an NLP-to-DSL converter for trading strategies.

Convert natural language trading rules into the following simple JSON format:

{
  "entry": [ ... ],
  "exit": [ ... ]
}

Each item inside "entry" or "exit" must be a condition object OR a logical connector.

A **condition object** has:
{
  "indicator": "<name or indicator function>",   # e.g., close, volume, sma(20), rsi(14)
  "operator": ">", "<", ">=", "<=", "==",
  "value": <number or indicator>                 # e.g., 1000000 or sma(20)
}

A **logical operator object** has:
{
  "logic": "AND"  or  "OR"
}

Rules must appear in the sequence they are spoken.  
Do NOT nest groups.  
Do NOT create complex Boolean trees.  
Just represent the flow using alternating condition + logic + condition.

Allowed indicators:
- close
- open
- high
- low
- volume
- sma(<period>)
- ema(<period>)
- rsi(<period>)
- macd()
- atr(<period>)

ALWAYS RETURN ONLY PURE JSON.  
NO explanations, NO markdown, NO extra text.

"""


def generate_dsl_json(nl_query, api_key="ENTER YOUR OWN API KEY"):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS),
        contents=nl_query
    )

    clean_text = re.sub(r"^```json\s*|```$", "", response.text.strip(), flags=re.MULTILINE)

    try:
        dsl_json = json.loads(clean_text)
        return dsl_json
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:")
        print(response.text)
        raise