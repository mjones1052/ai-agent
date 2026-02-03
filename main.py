import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
import prompts
from functions.call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("Key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=prompts.system_prompt)
)


if args.verbose == True:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, verbose=True)
            if function_call_result.parts is None:
                raise Exception("No parts in function call result")
            elif function_call_result.parts[0].function_response is None:
                raise Exception("No function response in function call result part")
            elif function_call_result.parts[0].function_response.response is None:
                raise Exception("No response in function response")
            else:
                call_results = function_call_result.parts[0]
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
                
    else:
        print(response.text)
else:
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, verbose=False)
            if function_call_result.parts is None:
                raise Exception("No parts in function call result")
            elif function_call_result.parts[0].function_response is None:
                raise Exception("No function response in function call result part")
            elif function_call_result.parts[0].function_response.response is None:
                raise Exception("No response in function response")
            else:
                call_results = function_call_result.parts[0]
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)