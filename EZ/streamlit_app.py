import streamlit as st
import fitz  # PyMuPDF
import nltk
import random
from nltk.tokenize import sent_tokenize

from train import load_summarizer, load_qna, load_embedder


nltk.download('punkt')

# Load models once
summarizer = load_summarizer()
qna = load_qna()
embedder = load_embedder()

# Extract text from PDF or TXT
def extract_text(file):
    ext = file.name.split('.')[-1]
    if ext == 'pdf':
        doc = fitz.open(stream=file.read(), filetype='pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        return text
    elif ext == 'txt':
        return file.read().decode('utf-8')
    return ""

# Generate summary
def get_summary(text):
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ''
    for chunk in chunks:
        result = summarizer(chunk, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
        summary += result + ' '
        if len(summary.split()) > 150:
            break
    return ' '.join(summary.split()[:150])

# Answer question with justification
def answer_question(question, context):
    answers = []
    for para in context:
        result = qna(question=question, context=para)
        if result['score'] > 0.4:
            answers.append((result['answer'], result['score'], para))
    if not answers:
        return "❗ I couldn’t find a confident answer."
    best = sorted(answers, key=lambda x: x[1], reverse=True)[0]
    return f"📌 **Answer**: {best[0]}\n\n📖 *Supported by*: “{best[2][:300]}...”"

# Generate logic/comprehension questions
def generate_questions(sentences, count=3):
    questions = []
    for sent in random.sample(sentences, count * 2):
        prompt = f"Generate a comprehension question based on: {sent}"
        q = summarizer(prompt, max_length=50, min_length=15, do_sample=False)[0]['summary_text']
        if '?' in q:
            questions.append((q, sent))
        if len(questions) >= count:
            break
    return questions

# Streamlit UI
st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("📚 Smart Research Assistant")
st.markdown("Upload a document (PDF or TXT) and choose a mode to interact with your assistant.")

uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    doc_text = extract_text(uploaded_file)
    if doc_text.strip():
        st.success("✅ Document processed successfully!")

        # Summary
        summary = get_summary(doc_text)
        st.subheader("🔍 Auto Summary (≤150 words)")
        st.write(summary)

        sentences = sent_tokenize(doc_text)
        st.subheader("🧠 Choose an Interaction Mode")
        mode = st.radio("Select mode:", ["Ask Anything", "Challenge Me"])

        if mode == "Ask Anything":
            user_question = st.text_input("🔎 Ask a question based on the document:")
            if user_question:
                response = answer_question(user_question, sentences)
                st.markdown(response)

        elif mode == "Challenge Me":
            st.info("Try answering 3 logic/comprehension questions from the document.")
            questions = generate_questions(sentences)
            for i, (q, context) in enumerate(questions):
                user_ans = st.text_input(f"Q{i+1}: {q}")
                if user_ans:
                    result = qna(question=q, context=context)
                    correct = result['answer'].lower() in user_ans.lower()
                    if correct:
                        st.success(f"✅ Correct! | Expected: {result['answer']}")
                    else:
                        st.error(f"❌ Incorrect. Expected: {result['answer']}")
                    st.caption(f"📖 From: “{context[:300]}...”")
    else:
        st.warning("⚠️ Could not read any content from the uploaded file.")
else:
    st.info("📂 Please upload a PDF or TXT file to begin.")

