import streamlit as st
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY='AIzaSyCnx6R_y3535kNSuaLlXPZS0o0Q1WHdkA8'
genai.configure(api_key=GOOGLE_API_KEY)

def to_textt(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '> ', predicate=lambda _: True)




def showText():
    st.title("Text Summarizer")

    text_to_summarize = st.text_area("Enter your text", "", height=200)

    if st.button("Generate Summary"):
        with st.status('Summarization in progress...') as status:
            model = genai.GenerativeModel('gemini-pro')
            prompt = "Generate Summary "+text_to_summarize
            summary = model.generate_content(prompt)
            summary = to_textt(summary.text)
            st.write(summary)
            status.update(label='Summarization complete!', state='complete', expanded=True)
            st.download_button('Save as a file',data=summary,file_name='txt_summarized.txt')
