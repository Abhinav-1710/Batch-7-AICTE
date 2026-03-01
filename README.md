# 🧠 AI-Powered Study Buddy  
## Batch-7-AICTE 

An AI-based web application developed as part of the AICTE Batch-7 program.  
The system helps students summarize notes, ask questions, and generate quizzes automatically using Artificial Intelligence.

---

## 📌 Project Overview

The AI-Powered Study Buddy is a web application built using Streamlit and Natural Language Processing (NLP) techniques.

It allows users to:
- Upload academic PDF notes
- Generate AI-based summaries
- Ask context-based questions
- Attempt automatically generated MCQ quizzes

This project demonstrates practical implementation of AI in education.

---

## 🚀 Features

### 📄 1. AI Summarization
Generates concise summaries from long PDF documents using a pre-trained BART transformer model.

### ❓ 2. Semantic Search
Uses Sentence Transformers and cosine similarity to retrieve relevant answers based on context.

### 🧠 3. MCQ Quiz Generator
Creates multiple-choice questions dynamically from uploaded content and evaluates user performance with scoring.

---

## 🛠️ Technologies Used

- Python 3.10
- Streamlit
- Hugging Face Transformers
- Sentence Transformers
- Scikit-learn
- NLTK
- PyPDF2

---

## ⚙️ Installation & Setup

1️⃣ Clone the repository: https://github.com/YOUR-USERNAME/Batch-7-AICTE.git
2️⃣ Navigate to project folder: cd Batch-7-AICTE
3️⃣ Create virtual environment: python -m venv venv
4️⃣ Activate virtual environment: venv\Scripts\activate
5️⃣ Install dependencies: pip install -r requirements.txt
6️⃣ Run the application:
streamlit run app.py

The application will run at:
http://localhost:8501

---

## 📊 System Workflow

1. User uploads PDF file.
2. Text is extracted using PyPDF2.
3. Sentences are tokenized using NLTK.
4. AI models process the content:
   - Summarization using BART
   - Semantic search using embeddings
   - MCQ generation using rule-based logic
5. Results are displayed through an interactive Streamlit interface.

---

## 🎯 Future Scope

- Chatbot-style interaction
- Multi-document upload support
- Flashcard-based learning mode
- Cloud deployment using Streamlit Cloud

---

## 👨‍💻 Author

Abhinav Saini  
Batch-7 AICTE 

---

## 📄 License

This project is developed for academic purposes under AICTE Batch-7.
🔥 IMPORTANT

Replace:

YOUR-USERNAME

With your actual GitHub username.


