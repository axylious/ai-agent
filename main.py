import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


def generateContent(msg):
    return client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=msg,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )


def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    res = generateContent(messages)

    if res.usage_metadata:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("API request failed to retrieve usage_data")
    for function_call in res.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
    print(res.text)


if __name__ == "__main__":
    main()
