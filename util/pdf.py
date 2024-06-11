import streamlit as st
from PyPDF2 import PdfReader
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY='AIzaSyCnx6R_y3535kNSuaLlXPZS0o0Q1WHdkA8'
genai.configure(api_key=GOOGLE_API_KEY)

def to_textt(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '> ', predicate=lambda _: True)

def get_pdf_text(pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text


def summary_pdf(text_from_pdf):
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Generate Summary for "+ text_from_pdf
    summary = model.generate_content(prompt)
    summary = to_textt(summary.text)
    return summary

def showPDF():
    st.title("PathPal PDF Summarizer")
    pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            summary=summary_pdf(raw_text)  
            st.write(summary)
      
        