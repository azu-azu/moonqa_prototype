# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_pdf_path():
    return os.path.join("data", "about_moon.pdf")

def get_index_path():
    return os.path.join("index", "faiss_index")
