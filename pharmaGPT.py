import openai
import os
from typing import List, Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(messages: List[dict]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_system_message(content: str) -> dict:
    return {"role": "system", "content": content}

def create_user_message(content: str) -> dict:
    return {"role": "user", "content": content}

def interact_with_gpt(system_message: str, user_message: str) -> str:
    messages = [
        create_system_message(system_message),
        create_user_message(user_message)
    ]
    return chat_with_gpt(messages)

def extract_prescription_info(prescription_text: str) -> str:
    return interact_with_gpt(
        "You are an AI that helps pharmacists analyze prescriptions.",
        f"Analyze the prescription and list essential details in concise bullet points without any conversational elements: {prescription_text}"
    )

def get_drug_information(drug_name: str) -> str:
    return interact_with_gpt(
        "You are an AI that provides drug information.",
        f"Provide concise bullet points about the drug, focusing on factual information without conversational elements: {drug_name}"
    )

def validate_prescription(prescription_text: str) -> str:
    return interact_with_gpt(
        "You are an AI that validates prescriptions for errors.",
        f"Review the prescription for errors and list them in factual bullet points, avoiding conversational language: {prescription_text}"
    )

def check_drug_interactions(drug_list: List[str]) -> str:
    drug_list_str = ", ".join(drug_list)
    return interact_with_gpt(
        "You are an AI that checks for drug interactions.",
        f"Identify interactions between the following drugs and summarize in concise bullet points, omitting conversational language: {drug_list_str}"
    )

def search_drug_or_condition(query: str) -> str:
    return interact_with_gpt(
        "You are an AI that helps pharmacists search for drug information and conditions.",
        f"Search for factual information about the given query and present in concise bullet points, avoiding conversational elements: {query}"
    )