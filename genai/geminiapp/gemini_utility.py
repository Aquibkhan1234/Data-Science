import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash")
    response =gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result


def embeddings_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model = embedding_model,
                                    content = input_text,
                                    task_type='retrieval_document')
    embedding_list = embedding["embedding"]
    return embedding_list

def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result




