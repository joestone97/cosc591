"""
Front-end - Home page
The following script creates the home page for the web application and handles front-end 
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Audio Workshop",
    page_icon="🔊",
    layout="wide"
)

def main():
    ####
    # sidebar
    ####
    st.sidebar.success("Flick between Sections here!")#add green text to the side bar to indicate the intended use (Ron's request)

    ####
    # main panel
    ####
    st.title("Directional Hearing Workshop")
    st.markdown("Welcome to the Directional Hearing Workshop! This website lets high school students explore three key factors that impact a human's ability to detect sound:")
    st.markdown(
        """
        <style>
        .bullet-points > * {
            line-height: 1;
        }
        </style>
        <div class='bullet-points'>
        <ul>
        <li>Delay</li>
        <li>Volume</li>
        <li>Frequency</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image("data/images/home_page.png", use_column_width=True)
    st.markdown("""Rather than reading a textbook, here you will be able to play around with pre-recorded sounds and see how they impact your ability to detect the location of sounds.""", unsafe_allow_html=True)
    st.markdown("""<div style = 'font-size: 24px;'><b>Remember to use earbuds or headphones!</b><br></div>""", unsafe_allow_html=True)

    #  Navigation button
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('Start Exploring!', key="start_button", help='Click to navigate to "Explore Delay, Volume and Frequency" page',use_container_width=True):
        # Open the other Streamlit page
            switch_page("explore delay, volume, and frequency")

    ####
    # Footer
    ####
    st.markdown('<hr><p style="text-align:center">Directional Hearing Workshop - Created for a UNE Data Science Project</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
