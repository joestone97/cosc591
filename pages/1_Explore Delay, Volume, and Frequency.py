import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import sys
import soundfile as sf
import numpy as np
sys.path.insert(0, './scripts')
from scripts import delay,pitch,volume #note backend and front end are separated

################
# Global Parameters
################
audio_options = {
    "Drum Track":"drums_96k.wav",
    "Singer":"singer_96k.wav",
    "Thunder":"thunder_96k.wav"
}


#################
# Page
#################
st.set_page_config(
    page_title="Audio Workshop",
    page_icon="🔊",
    layout="wide"
)

def main():
    ####
    # Sidebar
    ####
    st.sidebar.success("Flick between Sections here!")

    ####
    # Main panel
    ####
    st.title("Have you ever wondered how we locate a sound's origin?")
    st.markdown("The human auditory system is the sensory system for the sense of hearing and involves identifying the sound source as well as the location of sounds in the environment. Our minds determine where sound is coming from using multiple clues and some types of sound are easier to locate (eg: Bird calls) than others (eg. Continuous tone)")

    ###
    # DELAY SECTION
    ###
    def on_delay_selected_ear_change(ear="left"):
        """function used to force trigger of backend script when input changes (bug fix)"""
        delay.delay(ear=ear, file=audio_options[delay_selected_sound], delay_time=delay_selected_value/1000)
    
    def on_delay_selected_sound_change(sound="Drum Track"):
        """function used to force trigger of backend script when input changes (bug fix)"""
        delay.delay(ear=delay_selected_ear, file=audio_options[sound], delay_time=delay_selected_value/1000)

    st.header("Delay")
    st.markdown("The ear which sound hits first is a major indicator of the direction the sound came from. So the time delay between left and right ears is a major player. For example, if the sound hits your right ear first, the sound likely originated to the right of your body. If it hits both ears at the same time, it likely originated from directly in front or behind you.<br><br><b>Below you can play with the sound and change the delay.</b><br> Choose the sound you want to hear, and the time delay you want between your right and left ear. Notice that depending on the ear and delay you choose, the sound appears to come from a different direction.",unsafe_allow_html=True)

    #Interactive section's widgets
    col1, col2 = st.columns(2)
    with col1:
        delay_selected_ear = st.radio("Select an ear", ("left", "right"),  on_change=on_delay_selected_ear_change)
    with col2:
        delay_selected_sound = st.selectbox("Choose a sound:", list(audio_options.keys()), on_change=on_delay_selected_sound_change)
    format_dict = {
        0.0: "no delay",
        1.0: "large delay"
    }

    #audio widget and initial backend trigger
    delay_selected_value = st.slider("Choose a delay:", 0.0, 1.0, 0.0, 0.01,format="%g milliseconds")
    delay.delay(ear=delay_selected_ear, file=audio_options[delay_selected_sound], delay_time=delay_selected_value/1000)
    st.markdown("<b>Play Audio",unsafe_allow_html=True)
    st.audio("./data/audio/delay_overwrite.wav", format='audio/wav')

    ###
    # VOLUME SECTION
    ###
    def volume_selected_ear_change(ear="left"):
        """function used to force trigger of backend script when input changes (bug fix)"""
        volume.volume(ear=ear, file=audio_options[volume_selected_file], scaling_factor=volume_selected_value/100)

    def volume_selected_sound_change(sound="Drum Track"):
        """function used to force trigger of backend script when input changes (bug fix)"""
        volume.volume(ear=volume_selected_ear, file=audio_options[sound], scaling_factor=volume_selected_value/100)

    st.header("Volume")
    st.markdown("If you think about a time a friend has talked to you while you are walking side by side, it's clear that the sound is louder on the side they are closer to. This is another factor influencing our ability to detect sound, the volume. Whichever ear detects the sound louder our brain interprets as the direction the sound is coming from.<br><b>Change the sound in a specific ear and have a play!",unsafe_allow_html=True)

    #Interactive section's widgets
    col1, col2 = st.columns(2)
    with col1:
        volume_selected_ear = st.radio("Select an ear", ("left", "right"),key=1,  on_change=volume_selected_ear_change)
    with col2:
        volume_selected_file = st.selectbox("Choose a sound:", list(audio_options.keys()),key=2,  on_change=volume_selected_sound_change)

    #audio widget and initial backend trigger
    volume_selected_value = st.slider("Choose what percentage of the original volume for the ear to be (100% is the original volume):", 0, 500, 100, 25, format="%g%%", key="delay_slider")
    volume.volume(ear=volume_selected_ear, file=audio_options[volume_selected_file], scaling_factor=volume_selected_value/100)
    st.markdown("<b>Play Audio",unsafe_allow_html=True)
    st.audio("./data/audio/volume_overwrite.wav", format='audio/wav')


    ###
    # FREQUENCY SECTION
    ###
    st.header("Frequency")
    st.markdown('''Spectral content refers to the different frequencies that make up a sound.
        Different things that make sounds (like a violin or a piano) have different ways of making those frequencies.
        For example, a violin and a piano can play the same note, but they sound different because the way they make that note is not the same.
        The human auditory system can analyse the spectral content of a sound and use it to identify and distinguish different sounds as well as the direction of a sound.
        For example, when a sound reflects off our ears, it can create a spectral notch or peak at a particular frequency, which can help the brain determine the direction of the sound source.''',
        unsafe_allow_html=True
        )

    #Interactive section's widgets
    col1, col2 = st.columns(2)
    with col1:
        pitch_selected_ear = st.radio("Select an ear", ("left", "right"),key=3)
    with col2:
        pitch_selected_file = st.selectbox("Choose a sound:", list(audio_options.keys()),key=4)
    pitch_selected_value = st.slider("Increase or decrease the frequency (frequencies above this frequency will be filtered out, so you can't hear them):", 20, 20000, 3000, 10, key="pitch_slider")

    #audio widget and initial backend trigger
    pitch.apply_lowpass_filter(ear=pitch_selected_ear, wave_file=audio_options[pitch_selected_file], cutoff_freq=pitch_selected_value, order=2)
    st.markdown("<b>Play Audio",unsafe_allow_html=True)
    st.audio("./data/audio/pitch_overwrite.wav", format='audio/wav')

    ###
    # Conclusion / navigation button
    ###
    st.header("How does sound appear to come from a different direction in music/movies?")
    st.markdown("Ever heard a bird fly from one side of the movies to another? Or had a cool sound appear to fly around your head?<br> You can probably tell from the exploration above that changing the volume and delay in a specific ear won't make sound do anything cool like that. So how is it done? Well in the next section we'll let you play around with one method scientists have created.",unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('Look at the more advanced methods', key="start_button", help='Click look at the "Advanced Sound Alterations" page',use_container_width=True):
        # Open the other Streamlit page
            switch_page("advanced sound alterations")


if __name__ == "__main__":
    main()
