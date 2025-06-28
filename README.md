# EZ-Assignment
# Smart Assistant for Research Summarization

This project is an AI-powered assistant that reads uploaded documents (PDF/TXT), understands their content, and performs advanced tasks like summarization, contextual question answering, and logic-based reasoning.

## Features

### Document Upload
- Supports both `.pdf` and `.txt` formats.
- Suitable for structured English documents like research papers, reports, and manuals.

### Auto Summary
- Automatically generates a concise summary (up to 150 words) after document upload.

### Two Interaction Modes
1. Ask Anything  
   - Users can ask free-form questions based on the uploaded document.  
   - The assistant answers with relevant content extracted from the document, with justifications.

2. Challenge Me  
   - The assistant generates 3 logic-based or comprehension-focused questions from the document.  
   - Users answer, and the assistant evaluates their responses and provides explanations.

### Contextual Answering
- All answers are grounded in the uploaded document.
- No hallucination or fabricated information.
- Justifications are included using snippets from the document.

## Architecture

Frontend: Streamlit  
Backend: Transformers-based models from Hugging Face  

Components:
- Document Upload using `fitz` (PyMuPDF) for PDFs and direct reading for TXTs.
- Summarization using `DistilBART`.
- Question Answering using `DistilBERT`.
- Sentence Embedding using `MiniLM`.

## File Structure

```
project/
│
├── streamlit_app.py      # Streamlit frontend and UI logic
├── train.py              # Model loading (summarizer, QnA, embedder)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/smart-research-assistant.git
cd smart-research-assistant
```

### Step 2: Create and Activate a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate     # On Windows
source .venv/bin/activate  # On macOS/Linux
```

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

If you face issues with `fitz`, install it using:

```bash
pip install PyMuPDF
```

### Step 4: Run the App

```bash
streamlit run streamlit_app.py
```

## Models Used

| Task               | Model Name                                  |
|--------------------|----------------------------------------------|
| Summarization      | sshleifer/distilbart-cnn-12-6                |
| Question Answering | distilbert-base-uncased-distilled-squad     |
| Embedding          | sentence-transformers/all-MiniLM-L6-v2      |

All models are downloaded via the Hugging Face `transformers` and `sentence-transformers` libraries.

## Evaluation Criteria Mapping

| Evaluation Area                      | Implemented |
|--------------------------------------|-------------|
| Response Quality & Justification     | Yes         |
| Reasoning Mode Functionality         | Yes         |
| UI/UX and Smooth User Flow           | Yes         |
| Code Structure and Documentation     | Yes         |
| Creativity and Bonus Features        | Partial     |
| Minimal Hallucination & Context Use  | Yes         |

## Bonus Features (Partially Implemented)

- Document snippet justifications in all responses.
- Memory-based follow-up and answer highlighting planned.

## Optional Demo (If Applicable)

You can record a 2–3 minute walkthrough using Loom or YouTube and add the link here.

## License

This project is built for educational and evaluation purposes as part of the EZ assignment.
