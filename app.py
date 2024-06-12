import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container

from util.pdf import showPDF
from util.text import showText
#from util.chat import showCHAT
from util.roadmap import showROADMAP
# page title and icon
st.set_page_config(page_title="PathPal", page_icon='🤖')
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
    st.image('imgs/main.png', width=360)
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
        with stylable_container(
            key='markdown_container',
            css_styles="""
            {
                background-color: #ADD8E6;
                border: 3px solid #cccccc;
                border-radius: 1em;
                padding: 10px 70px;
            }"""
        ):
            st.markdown("Welcome! What's your plan?")

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
