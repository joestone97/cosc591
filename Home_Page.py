import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Audio Workshop",
    page_icon="🔊",
    layout="wide"
)

def main():
    st.sidebar.success("Flick between Sections here!")

    st.title("Directional Hearing Workshop")
    st.markdown("Welcome to the Directional Hearing Workshop! This website lets high school students explore three key factors that impact a human's ability to detect sound:")
    # Add dot points for delay, volume, and pitch
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
    # Add image
    st.image("data/images/home_page.png", use_column_width=True)

    st.markdown("""Rather than reading a textbook, here you will be able to play around with pre-recorded sounds and see how they impact your ability to detect the location of sounds.<br><br><b>Remember to use earbuds or headphones!</b><br>""", unsafe_allow_html=True)

    # Add button to start exploring
    m = st.markdown("""
        <style>
        .stButton > button:first-child {
            color: rgb(204, 49, 49);
            padding:15px 80px;
            font-size:20px
        }
        </style>""", unsafe_allow_html=True)


    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('Start Exploring!', key="start_button", help="Click to start exploring the main page",use_container_width=True):
        # Open the other Streamlit page
            switch_page("explore delay, volume, and frequency")
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


    # Add footer
    st.markdown('<hr><p style="text-align:center">Directional Hearing Workshop - Created for a UNE Data Science Project</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
