import streamlit as st
import textwrap
import google.generativeai as genai
import os

GOOGLE_API_KEY='AIzaSyCnx6R_y3535kNSuaLlXPZS0o0Q1WHdkA8'
genai.configure(api_key=GOOGLE_API_KEY)

image_folder = os.path.join('util', 'preset roadmaps')

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
        if interests.lower() in ['data science', 'ds']:
            st.subheader("This is a preset roadmap by PathPal developer team: ")
            image_path = os.path.join(image_folder, 'Data Science.png')
            st.image(image_path, caption='Data Science Roadmap', use_column_width=True)
            recommendations = generate_recommendations(input_text)
            # Output recommendations in a friendly format
            st.subheader("Recommended Roadmap:")
            st.markdown(recommendations)
    
        elif interests.lower() in ['artificial intelligence', 'ai']:
            st.subheader("This is a preset roadmap by PathPal developer team: ")
            image_path = os.path.join(image_folder, 'AI.png')
            st.image(image_path, caption='Artificial Intelligence Roadmap', use_column_width=True)
            recommendations = generate_recommendations(input_text)
            # Output recommendations in a friendly format
            st.subheader("Recommended Roadmap:")
            st.markdown(recommendations)
        elif interests.lower() in ['android developer', 'android','android development']:
            st.subheader("This is a preset roadmap by PathPal developer team: ")
            image_path = os.path.join(image_folder, 'android.png')
            st.image(image_path, caption='Android developer Roadmap', use_column_width=True)
            recommendations = generate_recommendations(input_text)
            # Output recommendations in a friendly format
            st.subheader("Recommended Roadmap:")
            st.markdown(recommendations)            
        elif interests.lower() in ['cyber security', 'cybersecurity','cyber','security','hacking','hacker']:
            st.subheader("This is a preset roadmap by PathPal developer team: ")
            image_path = os.path.join(image_folder, 'cyber security.png')
            st.image(image_path, caption='cyber security Roadmap', use_column_width=True)
            recommendations = generate_recommendations(input_text)
            # Output recommendations in a friendly format
            st.subheader("Recommended Roadmap:")
            st.markdown(recommendations)     
        else:
            recommendations = generate_recommendations(input_text)
            # Output recommendations in a friendly format
            st.subheader("Recommended Roadmap:")
            st.markdown(recommendations)
    

