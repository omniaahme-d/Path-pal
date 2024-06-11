import streamlit as st
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY='AIzaSyCnx6R_y3535kNSuaLlXPZS0o0Q1WHdkA8'
genai.configure(api_key=GOOGLE_API_KEY)

def to_textt(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '> ', predicate=lambda _: True)


def generate_recommendations(input_text):
    # Check if input text is empty
    if not input_text.strip():
        return "Sorry, I have no information."

    model = genai.GenerativeModel('gemini-pro')
    prompt = model.generate_content(input_text)
    prompt = to_textt(prompt.text)
    return prompt

def showROADMAP():
    st.title("Computer Science Roadmap Recommendation System")

    # Collect user input (current knowledge level, interests, goals)
    interests = st.text_input("The field you Interested in:")
    current_knowledge = st.text_input("Current knowledge level:")
    goals = st.text_input("Your goals in the future:")

    # Check if any required field is empty
    if not current_knowledge.strip() or not interests.strip() or not goals.strip():
        st.warning("Please fill in all required fields.")
        return

    # Generate recommendation prompt based on user input
    input_text = f"I am interested in {interests}. My current knowledge level is {current_knowledge}. " \
                 f"My goals are {goals}. " \
                 f"Based on this, can you recommend a roadmap for me?"  \
                 f"Please make sure to be strict with your answer and tell me EXACTLY what should i learn " \
                 f"give me the steps of the roadmap in Summary " \


    if st.button("Generate Recommendations"):
        recommendations = generate_recommendations(input_text)
        # Output recommendations in a friendly format
        st.subheader("Recommended Roadmap:")
        st.markdown(recommendations)