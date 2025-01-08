import json
import pdb
import concurrent.futures

from htmlrag import clean_html
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import parse_obj_as

from form_obj import FormField, FormScraper
from prompts import prompts, Prompts

model = ChatOllama(model='llama3.1', temperature=0, format="json")
output_parser = PydanticOutputParser(pydantic_object=FormScraper)


def parse_response_to_formfields(response_json):
    print("Parsing response JSON into FormField objects.")
    forms_dict = {}
    for i, json_obj in enumerate(response_json):
        print(f"Processing form {i}.")
        fields = json_obj['fields']
        forms_dict[i] = []
        for field in fields:
            print(f"Parsing field: {field}")
            field_obj = parse_obj_as(FormField, field)
            forms_dict[i].append(field_obj)
    print("Finished parsing response JSON.")
    return forms_dict


def get_response_json(content):
    print("Extracting JSON from response content.")
    try:
        response_json = json.loads(content)
        if 'forms' in response_json:
            print("'forms' key found in response JSON.")
            return response_json['forms']
        return response_json
    except Exception as e:
        print(f"Error parsing JSON content: {e}")
        return None


def validate_response(response_json, original_forms):
    print("Validating response JSON structure against the original forms.")
    if 'forms' not in response_json:
        for original_form, response_form in zip(original_forms, response_json):
            original_fields = {field['id']: field for field in original_form['fields']}
            response_fields = {field['id']: field for field in response_form['fields']}
            for field_id, original_field in original_fields.items():
                if field_id not in response_fields:
                    print(f"Missing field: {field_id}")
                    return False
                response_field = response_fields[field_id]
                for key in original_field:
                    if key != "value" and original_field[key] != response_field.get(key):
                        print(f"Field mismatch on {key} for field {field_id}")
                        return False
    print("Validation successful.")
    return True


def get_response_to_forms(forms, prompt_type):
    print(f"Generating response for prompt type: {prompt_type}")
    prompt_template = prompts.get_prompt(prompt_type)
    print(f"Prompt template: {prompt_template}")
    prompt = PromptTemplate(
        template=prompt_template,
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    chain = prompt | model
    attempt = 0
    max_attempts = 3

    while attempt < max_attempts:
        print(f"Attempt {attempt + 1} of {max_attempts}")
        try:
            response = chain.invoke({"forms": forms})
            print("Response received from the model.")
            response_json = get_response_json(response.content)
            if response_json is None or not validate_response(response_json, forms):
                print("Validation failed or response is invalid. Retrying...")
                attempt += 1
                continue
            print("Response successfully validated.")
            return response_json
        except Exception as e:
            print(f"Error during chain invocation: {e}")
            attempt += 1
    print("Falling back to default values.")
    return forms


def initialize_key(key):
    key_types = ["name", "placeholder"]
    for type_ in key_types:
        try:
            if isinstance(key, dict):
                key = key[type_].lower()
            else:
                key = key.lower()
            return
        except:
            continue


def find_in_nested_json(key, data):
    print(f"Searching for key: {key} in nested JSON.")
    try:
        initialize_key(key)
        if isinstance(data, dict):
            for k, v in data.items():
                if k.lower() == key:
                    print(f"Key found: {key}, value: {v}")
                    return v
                if isinstance(v, (dict, list)):
                    found = find_in_nested_json(key, v)
                    if found is not None:
                        return found
        elif isinstance(data, list):
            for item in data:
                found = find_in_nested_json(key, item)
                if found is not None:
                    return found
        return None
    except Exception as e:
        print(f"Error during key search: {e}")
        return None


def extract_value_from_answer(content):
    print("Extracting value from model answer.")
    try:
        parsed_content = json.loads(content)
        extracted_value = parsed_content.get("value")
        print(f"Extracted value: {extracted_value}")
        return extracted_value
    except Exception as e:
        print(f"Error extracting value: {e}")
        return ''


def fill_form_json(response_forms, prompt_type="fill",
                   resume_jsonfile_path=r"C:\Users\אביב\Desktop\works\Chrome-Extentions\Auto-Form-Filler-ai\data.json"):
    print("Filling forms with data from resume JSON.")
    prompt_template = prompts.get_prompt(prompt_type)
    print(f"Prompt template: {prompt_template}")
    prompt = PromptTemplate(template=prompt_template)
    chain = prompt | model

    with open(resume_jsonfile_path, 'r') as f:
        resume_json = json.load(f)
    print("Resume JSON loaded successfully.")

    for form in response_forms:
        print(f"Processing form: {form}")
        fields = form['fields']
        for field in fields:
            print(f"Processing field: {field}")
            value = find_in_nested_json(field, resume_json)
            if value is not None:
                print(f"Value found for field: {value}")
                field['value'] = value
            else:
                print("No value found. Querying the model.")
                answer = chain.invoke({
                    'field': field,
                    'user_data': resume_json
                })
                field['value'] = extract_value_from_answer(answer.content)
                print(f"Field updated with value: {field['value']}")
    print("Form filling completed.")


def run_with_timeout(func, timeout, *args, **kwargs):
    """
    Run a function with a timeout.
    :param func: Function to run
    :param timeout: Timeout in seconds
    :param args: Positional arguments for the function
    :param kwargs: Keyword arguments for the function
    :return: Result of the function or None if it times out
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            print(f"Function '{func.__name__}' timed out after {timeout} seconds.")
            return None


def get_name_for_field(field_text, field_html):
    content = None
    if len(field_text.split()) > 5:
        content = field_text
    else:
        content = clean_html(field_html)

    return model.invoke(prompts.get_prompt(prompt_type="extract_name").format(content=content))
