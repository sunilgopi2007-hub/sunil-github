
import os
import requests
import streamlit as st
from dotenv import load_dotenv

from exporters import to_docx, to_pdf

# Load environment variables from project root
load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

# Header
st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Generate, edit and download legal document drafts "
    "using Google Gemini AI."
)

st.warning(
    "AI-generated documents may contain errors. "
    "Have a qualified lawyer review your document "
    "before signing or relying on it."
)

st.divider()

# Document input form
with st.form("document_form"):

    st.header("Enter Document Details")

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement (NDA)",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "Other"
        ]
    )

    if document_type == "Other":
        document_type = st.text_input(
            "Enter Document Type"
        )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example: Jane Doe (Provider), "
            "ABC Ltd. (Client)"
        )
    )

    terms = st.text_area(
        "Terms and Conditions",
        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Delivery by agreed deadline"
        ),
        height=150
    )

    effective_date = st.text_input(
        "Effective Date",
        placeholder="Example: 10 October 2026"
    )

    jurisdiction = st.text_input(
        "Jurisdiction (Optional)",
        placeholder="Example: Tamil Nadu, India"
    )

    submitted = st.form_submit_button(
        "Generate Document",
        type="primary",
        use_container_width=True
    )

# Generate document
if submitted:

    if not all([
        document_type.strip(),
        parties.strip(),
        terms.strip(),
        effective_date.strip()
    ]):
        st.error(
            "Please fill in all required fields."
        )

    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
            "jurisdiction": (
                jurisdiction.strip()
                or "Not specified"
            )
        }

        with st.spinner(
            "Generating your legal document..."
        ):
            try:
                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload,
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()

                st.session_state["draft"] = (
                    result["document"]
                )

                st.success(
                    "Document generated successfully!"
                )

            except requests.exceptions.HTTPError:
                try:
                    detail = response.json().get(
                        "detail",
                        response.text
                    )
                except ValueError:
                    detail = response.text

                st.error(
                    f"Backend error: {detail}"
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI. "
                    "Please start your backend."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "Request timed out. Please try again."
                )

            except Exception as error:
                st.error(
                    f"Unexpected error: {error}"
                )

# Editable preview and downloads
if "draft" in st.session_state:

    st.divider()
    st.header("Document Preview")

    st.info(
        "Review the generated content carefully. "
        "You can edit it below before downloading."
    )

    edited_text = st.text_area(
        "Edit Document",
        value=st.session_state["draft"],
        height=500,
        key="document_editor"
    )

    st.subheader("Download Document")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download TXT",
            data=edited_text.encode("utf-8"),
            file_name="legalease_draft.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="Download DOCX",
            data=to_docx(edited_text),
            file_name="legalease_draft.docx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            use_container_width=True
        )

    with col3:
        st.download_button(
            label="Download PDF",
            data=to_pdf(edited_text),
            file_name="legalease_draft.pdf",
            mime="application/pdf",
            use_container_width=True
        )