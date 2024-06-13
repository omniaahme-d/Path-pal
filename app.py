import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container

from util.pdf import showPDF
from util.text import showText
from util.chat import showCHAT
from util.roadmap import showROADMAP

import re
import firebase_admin
from firebase_admin import credentials, auth, firestore, initialize_app

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("full-3b000-f0ebc523667e.json")
    initialize_app(cred, {
    "apiKey": "AIzaSyBH1D-S1XLbU7F6cPDhtXYB41j_NUTGSEo",
    "authDomain": "full-3b000.firebaseapp.com",
    "projectId": "full-3b000",
    "storageBucket": "full-3b000.appspot.com",
    "messagingSenderId": "944891255895",
    "appId": "1:944891255895:web:ca3d9ef1610020d025d712",
    "measurementId": "G-MTNGZF70NL"
    })

# Function to validate email format
def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.match(pattern, email)

def Home():
    hide_img_fs = '''
    <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        /*[data-testid="stAppViewContainer"] {
            background-image: linear-gradient(to bottom right, rgb(44, 93, 135), white);
        }*/
        /* Removal of deploy and settings of streamlit header section */
        /* [data-testid="stHeader"] {display: none} */ 
        .stApp a:first-child {
            display: none;
        }
            
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
    </style>
    '''
    col1, col2, col3 , col4 , col5 = st.columns(5)
    with col2:
        st.image('imgs/main.svg', width=340)
    st.markdown(hide_img_fs, unsafe_allow_html=True)

    # navigation bar
    selected = option_menu(
        menu_title = None,
        options = ["Home", "Text", "PDF", "Chatbot","Roadmap"],
        icons = [None, 'card-text', 'filetype-pdf', 'chat-square-dots'],
        menu_icon = 'cast',
        default_index = 0,
        orientation='horizontal',
    )

    # Each option in the navigation bar
    # Home page
    if selected == "Home":
        #st.title("PathPal")
        st.write("A set of tools to assist students")
        col11, col12 = st.columns(2)
        with col11:
            st.markdown("Welcome! What's your plan?🤖")

    # Text Summarization
    elif selected == "Text":
        showText()

    # PDF Summarization
    elif selected == "PDF":
        showPDF()

    # CHATBOT
    elif selected == "Chatbot":
        showCHAT()

    # Roadmap
    elif selected == "Roadmap":
        showROADMAP()
        
def sign_up():
    db = firestore.client()
    st.subheader('Sign Up')
    email = st.text_input('Email')
    password1 = st.text_input('Password', type='password')
    password2 = st.text_input('Confirm Password', type='password')

    if st.button('Sign Up'):
        if not validate_email(email):
            st.error('Invalid email format!')
        elif len(password1) < 6:
            st.error('Password should be at least 6 characters long!')
        elif password1 != password2:
            st.error('Passwords do not match!')
        else:
            try:
                # Create a new user in Firebase Authentication
                user = auth.create_user(
                    email=email,
                    password=password1,
                )
                st.success('Account created successfully!')

                # Store user info in session
                st.session_state.user_email = email

                # Save the new user's email to Firestore
                doc_ref = db.collection('users').document(user.uid)
                doc_ref.set({
                    'email': email,
                    # Add any other user info you'd like to save
                })
            except auth.EmailAlreadyExistsError:
                st.error('Email already exists!')

# Feedback page# Feedback page
def feedback():
    st.subheader('Feedback')

    user_email = st.session_state.get('user_email', None)

    if user_email:  # Check if user is logged in
        db = firestore.client()
        st.title("Feedback")
        with st.form("my_form"):
            st.write("Is this website helpful?")
            feedback_rating = st.slider("Rate from 1 to 5", 1, 5)
            sentence = st.text_input("Message:")
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            feedback_data = {
                "email": user_email,
                "rating": feedback_rating,
                "message": sentence,
            }
            db.collection("user_feedback").add(feedback_data)
            st.success("Feedback submitted successfully!")
    else:
        st.error("Please log in or sign up to provide feedback.")

# Initialize a session state variable for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# Login page
def login():
    st.subheader('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        try:
            user = auth.get_user_by_email(email)
            st.success('Login successful!')
            st.session_state.user_email = email  # Set user_email in session state
            st.session_state.logged_in = True  # Update login status
        except auth.UserNotFoundError:
            st.error('Invalid email or password!')

# Navigation
# Function to read SVG file and return its content
def get_svg_image(svg_path):
    with open(svg_path, "r") as svg_file:
        return svg_file.read()

# Path to your logo SVG image
logo_path = "imgs/logo.svg"
# Get the SVG content
logo_svg = get_svg_image(logo_path)
# Modify the SVG content to include a width attribute
# Replace '100px' with the desired width
logo_svg = logo_svg.replace('<svg', '<svg width="200px" height="200px"')

# Create the HTML for the SVG logo
logo_html = f"""
<div style="text-align: center; padding: 0px 0;">
    {logo_svg}
</div>
"""

# Insert the SVG logo at the top of the sidebar
st.sidebar.markdown(logo_html, unsafe_allow_html=True)
# Navigation
nav = st.sidebar.radio('Navigation', ['Login','Sign Up', 'Feedback'])

if nav == 'Login' and not st.session_state.logged_in:
    login()
elif nav == 'Sign Up':
    sign_up()
elif nav == 'Feedback':
    feedback()

# Call Home() only when user is logged in and not in 'Sign Up' or 'Feedback' page
if st.session_state.logged_in and nav != 'Sign Up' and nav != 'Feedback':
    Home()
