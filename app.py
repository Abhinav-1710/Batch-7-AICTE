from transformers import pipeline
import streamlit as st
import PyPDF2
import nltk
import numpy as np
import random
import re
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

st.set_page_config(page_title="AI Study Buddy")

st.title("🧠 AI-Powered Study Buddy")
st.write("Upload your study notes and ask questions!")

uploaded_file = st.file_uploader("Upload your PDF notes", type="pdf")

# ------------------------------
# Load Embedding Model
# ------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ------------------------------
# Load Summarizer Model
# ------------------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# ------------------------------
# PDF Text Extraction
# ------------------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


# ------------------------------
# CLEAN WORD FILTER
# ------------------------------
def clean_word(word):
    word = re.sub(r'[^a-zA-Z]', '', word)
    return word


# ------------------------------
# IMPROVED MCQ GENERATOR
# ------------------------------
def generate_quiz(sentences, num_questions=3):
    questions = []

    usable_sentences = [s for s in sentences if len(s.split()) > 8]

    if len(usable_sentences) == 0:
        return []

    selected = random.sample(
        usable_sentences,
        min(num_questions, len(usable_sentences))
    )

    for sentence in selected:
        words = [clean_word(w) for w in sentence.split()]
        words = [w for w in words if len(w) > 4]

        if len(words) < 4:
            continue

        answer_word = random.choice(words)

        question_text = sentence.replace(answer_word, "_____")

        wrong_options = random.sample(
            [w for w in words if w != answer_word],
            3
        )

        options = wrong_options + [answer_word]
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer_word
        })

    return questions


# ------------------------------
# MAIN LOGIC
# ------------------------------
if uploaded_file:

    st.success("File uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)
    sentences = sent_tokenize(text)

    st.subheader("📄 Extracted Text Preview:")
    st.write(text[:500])

    # --------------------------
    # AI SUMMARY SECTION
    # --------------------------
    st.divider()

    if st.button("📝 Generate AI Summary"):
        with st.spinner("Generating AI Summary..."):
            summary = summarizer(
                text[:2000],
                max_length=150,
                min_length=50,
                do_sample=False
            )
            st.subheader("📌 AI Generated Summary:")
            st.write(summary[0]['summary_text'])

    # --------------------------
    # SEMANTIC SEARCH SECTION
    # --------------------------
    st.divider()

    query = st.text_input("❓ Ask a question from your notes")

    if query:

        sentence_embeddings = model.encode(sentences)
        query_embedding = model.encode([query])

        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            sentence_embeddings
        )[0]

        top_indices = similarities.argsort()[-3:][::-1]

        st.subheader("📌 Most Relevant Answers (Semantic Search):")

        found = False
        for i in top_indices:
            if similarities[i] > 0.3:
                st.write(f"• {sentences[i]}")
                found = True

        if not found:
            st.write("No strong relevant answer found.")

    # --------------------------
    # REAL MCQ QUIZ SYSTEM
    # --------------------------
    st.divider()

    if st.button("🧠 Generate Quiz"):
        st.session_state.quiz = generate_quiz(sentences)
        st.session_state.submitted = False

    if "quiz" in st.session_state and len(st.session_state.quiz) > 0:

        st.subheader("📚 Quiz Time")

        score = 0

        for i, q in enumerate(st.session_state.quiz):

            st.write(f"### Q{i+1}: {q['question']}")

            user_answer = st.radio(
                f"Choose your answer for Q{i+1}:",
                q["options"],
                key=f"q_{i}"
            )

            if st.session_state.submitted:
                if user_answer == q["answer"]:
                    st.success("Correct ✅")
                    score += 1
                else:
                    st.error(f"Wrong ❌ | Correct answer: {q['answer']}")

            st.write("---")

        if not st.session_state.submitted:
            if st.button("✅ Submit Quiz"):
                st.session_state.submitted = True
                st.rerun()

        if st.session_state.submitted:
            st.subheader(f"🎯 Your Score: {score} / {len(st.session_state.quiz)}")

            if st.button("🔄 Reset Quiz"):
                st.session_state.clear()
                st.rerun()