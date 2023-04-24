import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import sys
sys.path.insert(0, './scripts')
from scripts import delay,pitch,volume
import wave
import io
import tempfile
import os
import soundfile as sf
import numpy as np
import librosa

################
# Global Parameters
################
audio_options = {
    "Drum Track":"drums_96k.wav",
    "Singer":"singer_96k.wav",
    "Thunder":"thunder_96k.wav"
}


#################
#Page
#################
st.set_page_config(
    page_title="Audio Workshop",
    page_icon="🔊",
    layout="wide"
)

def main():
    st.sidebar.success("Flick between Sections here!")
    st.title("Have you ever wondered how we locate a sound's origin?")


    st.markdown("The human auditory system is the sensory system for the sense of hearing and involves identifying the sound source as well as the location of sounds in the environment. Our minds determine where sound is coming from using multiple clues and some types of sound are easier to locate (eg: Bird calls) than others (eg. Continuous tone)")

    ###
    # DELAY SECTION
    ###
    st.header("Delay")
    st.markdown("The ear which sound hits first is a major indicator of the direction the sound came from. So the time delay between left and right ears is a major player. For example, if the sound hits your right ear first, the sound likely originated to the right of your body. If it hits both ears at the same time, it likely originated from directly in front or behind you.<br><br><b>Below you can play with the sound and change the delay.</b><br> Choose the sound you want to hear, and the time delay you want between your right and left ear. Notice that depending on the ear and delay you choose, the sound appears to come from a different direction.",unsafe_allow_html=True)

    #interactive section
    col1, col2 = st.columns(2)

    with col1:
        delay_selected_ear = st.radio("Pick an ear", ("left", "right"))

    with col2:
        delay_selected_sound = st.selectbox("Choose a sound:", list(audio_options.keys()))

    # Add slider to select delay
    format_dict = {
        0.0: "no delay",
        1.0: "large delay"
    }

    delay_selected_value = st.slider("Choose a delay:", 0.0, 0.75, 0.0, 0.01,format="%g seconds")
    #note that this function is simply called and does not actually play from memory. I dont know if this will work in the server
    delay.delay(ear=delay_selected_ear, file=audio_options[delay_selected_sound], delay_time=delay_selected_value)
    st.markdown("<b>Play Audio",unsafe_allow_html=True)
    st.audio("./data/audio/delay_overwrite.wav", format='audio/wav')

    ###
    # VOLUME SECTION
    ###
    st.header("Volume")
    st.markdown("If you think about a time a friend has talked to you while you are walking side by side, it's clear that the sound is louder on the side they are closer to. This is another factor influencing our ability to detect sound, the volume. Whichever ear detects the sound louder our brain interprets as the direction the sound is coming from.<br><b>Change the sound in a specific ear and have a play!",unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        volume_selected_ear = st.radio("Pick an ear", ("left", "right"),key=1)

    with col2:
        volume_selected_file = st.selectbox("Choose a sound:", list(audio_options.keys()),key=2)

    volume_selected_value = st.slider("Choose what percentage of the original volume for the ear to be (100% is the original volume):", 0, 500, 100, 25, format="%g%%", key="delay_slider")
    #note that this function is simply called and does not actually play from memory. I dont know if this will work in the server
    volume.volume(ear=volume_selected_ear, file=audio_options[volume_selected_file], scaling_factor=volume_selected_value/100)
    st.markdown("<b>Play Audio",unsafe_allow_html=True)
    st.audio("./data/audio/volume_overwrite.wav", format='audio/wav')


    ###
    # PITCH SECTION
    ###
    st.header("Frequency")
    st.markdown("Frequency is a concept that's a little less intuitive that delay and volume, it refers to how high or low a sound is. A whistle would have a high frequency and a growling sound would be a low frequency. The human ear and brain can process most mid-range frequencies and finds them easier to interpret the location they originate from. The frequency of sound itself does not make the sound appear to come from a diffrent direction (like direction and delay), but our ears and brain better process frequencies that are not too high and not too low. <br><b>Play around with the frequency of sound below!</b><br>Note that we've let you change frequency in a specific ear rather than both ears, so you can more easily compare the two sounds. However, your brain shouldn't interpret the sound as coming from a different location.",unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        pitch_selected_ear = st.radio("Pick an ear", ("left", "right"),key=3)

    with col2:
        pitch_selected_file = st.selectbox("Choose a sound:", list(audio_options.keys()),key=4)

    pitch_selected_value = st.slider("Increase or decrease the frequency (0 is the normal sound with no alteration):", -10, 10, 0, 1, key="pitch_slider")
    #note that this function is simply called and does not actually play from memory. I dont know if this will work in the server
    pitch.pitch(ear=pitch_selected_ear, file=audio_options[pitch_selected_file], change=pitch_selected_value)
    st.markdown("<b>Play Audio",unsafe_allow_html=True)
    st.audio("./data/audio/pitch_overwrite.wav", format='audio/wav')


    ###
    # Notes
    ###
    st.header("How do does sound appear to come from a different direction in music/movies?")
    st.markdown("Ever heard a bird fly from one side of the movies to another? Or had a cool sound appear to fly around your head?<br> You can probably tell from the exploration above that changing the volume and delay in a specific ear won't make sound do anything cool like that. So how is it done? Well in the next section we'll let you play around with one method scientists have created.",unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('Look at the more advanced methods', key="start_button", help="Click to start exploring the main page",use_container_width=True):
        # Open the other Streamlit page
            switch_page("advanced sound alterations")
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)





if __name__ == "__main__":
    main()
