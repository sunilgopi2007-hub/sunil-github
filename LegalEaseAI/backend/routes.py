import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

load_dotenv()

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str
    jurisdiction: str = "Not specified"


@router.post("/generate")
async def generate_document(payload: DocumentRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing GEMINI_API_KEY in environment."
        )

    model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    if model_name.startswith("models/"):
        model_name = model_name.replace("models/", "")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)

        prompt = f"""
Draft a professional {payload.document_type} for the following parties and terms.

Parties involved:
{payload.parties}

Terms and conditions:
{payload.terms}

Effective date: {payload.effective_date}
Jurisdiction: {payload.jurisdiction}

Requirements:
- Use clear legal drafting language
- Include headings and numbered clauses where appropriate
- Make the document internally consistent
- Be concise but complete
- Return only the final document text without markdown fences or commentary
""".strip()

        response = model.generate_content(prompt)
        document = getattr(response, "text", None)

        if not document:
            raise HTTPException(
                status_code=500,
                detail="The AI model did not return any content."
            )

        return {"document": document.strip()}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}"
        ) from exc
