import streamlit as st
import textwrap
import google.generativeai as genai
import os
import pyrebase

# Initialize pyrebase
firebase_config = {
    "apiKey": "AIzaSyBH1D-S1XLbU7F6cPDhtXYB41j_NUTGSEo",
    "authDomain": "full-3b000.firebaseapp.com",
    "projectId": "full-3b000",
    "storageBucket": "full-3b000.appspot.com",
    "messagingSenderId": "944891255895",
    "appId": "1:944891255895:web:ca3d9ef1610020d025d712",
    "measurementId": "G-MTNGZF70NL",
    "databaseURL":"https://full-3b000.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()

# Configure Google Generative AI
GOOGLE_API_KEY = 'AIzaSyCnx6R_y3535kNSuaLlXPZS0o0Q1WHdkA8'
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
    interests = st.text_input("The field you are interested in:")
    current_knowledge = st.text_input("Current knowledge level:")
    goals = st.text_input("Your goals in the future:")

    # Check if any required field is empty
    if not current_knowledge.strip() or not interests.strip() or not goals.strip():
        st.warning("Please fill in all required fields.")
        return

    # Generate recommendation prompt based on user input
    input_text = f"I am interested in {interests}. My current knowledge level is {current_knowledge}. " \
                 f"My goals are {goals}. " \
                 f"Based on this, can you recommend a roadmap for me? " \
                 f"Please make sure to be strict with your answer and tell me EXACTLY what should I learn. " \
                 f"Give me the steps of the roadmap in summary."

def file_exists_in_firebase_storage(file_name):
    # Get a reference to the storage service
    storage = firebase.storage()

    # Get the list of all files
    all_files = storage.list_files()

    # Check if file_name exists in all_files
    for file in all_files:
        if file.name == file_name:
            return True

    return False


def showROADMAP():
    st.title("Computer Science Roadmap Recommendation System")

    interests = st.text_input("The field you are interested in:")
    current_knowledge = st.text_input("Current knowledge level:")
    goals = st.text_input("Your goals in the future:")

    if not current_knowledge.strip() or not interests.strip() or not goals.strip():
        st.warning("Please fill in all required fields.")
        return

    input_text = f"I am interested in {interests}. My current knowledge level is {current_knowledge}. " \
                 f"My goals are {goals}. " \
                 f"Based on this, can you recommend a roadmap for me? " \
                 f"Please make sure to be strict with your answer and tell me EXACTLY what should I learn. " \
                 f"Give me the steps of the roadmap in summary."


    if st.button("Generate Recommendations"):
        st.subheader("This is a preset roadmap by PathPal developer team:")

        image_path_on_cloud = f"{interests}.png"
        image_path_local = f"C:/Users/Ahmed/Desktop/gp/PathPal with Gemini API/"

        # Check if the file exists in Firebase Storage
        if file_exists_in_firebase_storage('Img/'+image_path_on_cloud):
            # Download the image from Firebase Storage
            storage.child('Img/'+image_path_on_cloud).download(path=image_path_local, filename=image_path_on_cloud)

            # Display the image in Streamlit
            st.image(image_path_local+image_path_on_cloud, caption=f'{interests} Roadmap', use_column_width=True)
        else:
            st.error("The requested roadmap image does not exist in Firebase Storage.")


        recommendations = generate_recommendations(input_text)
        st.subheader("Recommended Roadmap:")
        st.markdown(recommendations)
