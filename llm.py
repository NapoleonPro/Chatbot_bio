from rag import retrieve_context
import google.generativeai as genai
import os

# Ambil API key dari environment variable
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-pro")

def ask_gemini(question: str) -> str:
    context = retrieve_context(question)
    prompt = f"""
Kamu adalah chatbot pribadi bernama CihuyBot, yang hanya boleh menjawab berdasarkan biodata pembuatmu, yaitu Akbar Permana.

Biodata:
{context}cle

Pertanyaan pengguna:
{question}

Jawablah dengan singkat, relevan, dan tetap berdasarkan biodata.
"""

    response = model.generate_content(prompt)
    return response.text
