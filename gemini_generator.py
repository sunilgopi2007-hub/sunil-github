import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
class GeminiDocumentGenerator:
    def generate_document(self, data: dict) -> str:
        key=os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env and restart the backend.")
        model_name=os.getenv("GEMINI_MODEL","gemini-1.5-pro")
        genai.configure(api_key=key)
        model=genai.GenerativeModel(model_name)
        prompt=f"""Draft a clearly structured {data['document_type']} using these details.
Parties: {data['parties']}
Effective date: {data['effective_date']}
Jurisdiction: {data['jurisdiction']}
Terms (semicolon-separated where applicable): {data['terms']}

Use a title, numbered clauses, definitions where useful, signature blocks, and placeholders for missing details.
Do not invent facts, statutes, or guarantees of enforceability. Mark uncertain or jurisdiction-dependent provisions for lawyer review.
Include a brief note that this is a draft for review, not legal advice."""
        try:
            response=model.generate_content(prompt)
            result=getattr(response,"text","").strip()
            if not result: raise RuntimeError("The AI returned an empty response. Try again.")
            return result
        except Exception as e:
            raise RuntimeError(f"Gemini request failed: {e}") from e
