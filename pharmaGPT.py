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
        f"Analyze the prescription and provide only factual bullet points, make sure that you dont include any conversational aspect in the response: {prescription_text}"
    )

def get_drug_information(drug_name: str) -> str:
    return interact_with_gpt(
        "You are an AI that provides drug information.",
        f"Provide factual bullet points about the drug, make sure that you dont include any conversational aspect in the response: {drug_name}"
    )

def validate_prescription(prescription_text: str) -> str:
    return interact_with_gpt(
        "You are an AI that validates prescriptions for errors.",
        f"Identify errors in the prescription and provide factual bullet points, make sure that you dont include any conversational aspect in the response: {prescription_text}"
    )

def check_drug_interactions(drug_list: List[str]) -> str:
    drug_list_str = ", ".join(drug_list)
    return interact_with_gpt(
        "You are an AI that checks for drug interactions.",
        f"Check for interactions between these drugs and provide factual bullet points, make sure that you dont include any conversational aspect in the response: {drug_list_str}"
    )
    
def search_drug_or_condition(query: str) -> str:
    return interact_with_gpt(
        "You are an AI that helps pharmacists search for drug information and conditions.",
        f"Search and provide factual bullet points: {query}, make sure that you dont include any conversational aspect in the response"
    )
