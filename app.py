import pandas as pd
import streamlit as st
import openai
import PyPDF2

st.set_page_config(page_title="Flashcard Generator", layout="wide")

st.title("📚 LLM Flashcard Generator")

openai.api_key = "YOUR_API_KEY"  # Replace with your key or load from .env

input_method = st.radio("Select input method:", ["Paste Text", "Upload File"])

content = ""

if input_method == "Paste Text":
    content = st.text_area("Enter your educational content below:")
else:
    file = st.file_uploader("Upload a .txt or .pdf file")
    if file:
        if file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            content = " ".join([page.extract_text() for page in reader.pages])
        else:
            content = file.read().decode("utf-8")

if st.button("Generate Flashcards"):
    if content:
        with st.spinner("Generating flashcards..."):
            prompt = f"Generate 10 Q&A flashcards from the following content:\n{content}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            flashcards = response['choices'][0]['message']['content']
            st.subheader("📇 Flashcards:")
            st.markdown(flashcards)
    else:
        st.warning("Please enter or upload some content first.")

flashcards_list = [
    {"Question": "What is AI?", "Answer": "AI stands for Artificial Intelligence."},
    {"Question": "Define LLM.", "Answer": "LLM means Large Language Model."},
]

df = pd.DataFrame(flashcards_list)
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download as CSV",
    data=csv,
    file_name='flashcards.csv',
    mime='text/csv',
)
prompt = f"""
Generate 10 flashcards from the text below.
For each flashcard, include:
- Question
- Answer
- Difficulty (Easy, Medium, Hard)

Text:
{content}
"""
for i, card in enumerate(flashcards_list):
    q = st.text_input(f"Edit Question {i+1}", value=card['Question'])
    a = st.text_area(f"Edit Answer {i+1}", value=card['Answer'])
    flashcards_list[i]['Question'] = q
    flashcards_list[i]['Answer'] = a

prompt = f"""
Generate 10 flashcards from this content. Group them under topic headings.

Content:
{content}
"""
# ### Topic: AI Basics
# Q: What is AI?
# A: ...

# ### Topic: Machine Learning
# Q: What is supervised learning?
# A: ...
