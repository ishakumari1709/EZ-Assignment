from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# Load summarizer (used for both summary + question generation)
def load_summarizer():
    return pipeline("summarization", model="google/flan-t5-small")

# Load question-answering model (used for Ask Anything + answer checking)
def load_qna():
    model_name = "distilbert-base-uncased-distilled-squad"
    return pipeline("question-answering", model=model_name, tokenizer=model_name)

# Load embedder (optional: for memory or search-based features)
def load_embedder():
    model = "sentence-transformers/all-MiniLM-L6-v2"
    return pipeline("feature-extraction", model=model)
