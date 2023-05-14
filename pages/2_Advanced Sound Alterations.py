#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************
# import libraries
# ********************
import streamlit as st
import numpy as np
import wave
import io
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import sys
from streamlit_extras.switch_page_button import switch_page

sys.path.insert(0, './scripts')
from scripts import hrtf

# ********************
# Global parameters
# ********************
audio_file_options = [ 'Drums','Sine Wave', 'Bird', 'Dog', 'Singer', 'Thunder']
hrir_options = ['Subject 1', 'Subject 2', 'Subject 3']
azimuth_options = [*range(0,360,5)]
elevation_options = [-57, -30, -15, 0, 15, 30, 45, 60, 75]
# ********************
# Front-end functions
# ********************
def azimuth_to_unit_circle(azimuth):
    unit_circle_degrees = (90 - azimuth) % 360
    return unit_circle_degrees

def degrees_to_radians(degrees):
    """
    Converts degrees to radians.

    Parameters:
    degrees (float): The angle in degrees.

    Returns:
    float: The angle in radians.
    """
    radians = degrees * np.pi / 180
    return radians

def azimuth_diagram(azimuth):

    # load image
    img = Image.open('./data/images/top_down_head_01.png')

    # Angle in radians
    radians = degrees_to_radians(degrees = azimuth_to_unit_circle(azimuth = azimuth))

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set background image
    ax.imshow(img, extent=[-1, 1, -1, 1])

    # Draw a circle of radius 1
    circle = plt.Circle((0, 0), 1, fill=False)
    ax.add_artist(circle)

    # Calculate the coordinates of the endpoint of the vector
    x = np.cos(radians)
    y = np.sin(radians)

    # Draw a vector from the edge to the origin
    arrow_length = 0.1
    ax.arrow(x, y, -(x-(np.cos(radians)*arrow_length)), -(y-(np.sin(radians)*arrow_length)), head_width=0.05, head_length=arrow_length, fc='k', ec='k')

    # Set the limits of the plot
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    # Remove the axis
    ax.axis('off')

    # set the DPI of the figure
    fig.set_dpi(300)

    return fig, ax

def elevation_diagram(elevation):
    # load image
    img = Image.open('./data/images/profile_head_01.png')

    # Angle in radians
    radians = degrees_to_radians(degrees = elevation)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set background image
    ax.imshow(img, extent=[-1, 1, -1, 1])

    # Draw a circle of radius 1
    circle = plt.Circle((0, 0), 1, fill=False)
    ax.add_artist(circle)

    # Calculate the coordinates of the endpoint of the vector
    x = np.cos(radians)
    y = np.sin(radians)

    # Draw a vector from the edge to the origin
    arrow_length = 0.1
    ax.arrow(x, y, -(x-(np.cos(radians)*arrow_length)), -(y-(np.sin(radians)*arrow_length)), head_width=0.05, head_length=arrow_length, fc='k', ec='k')

    # Set the limits of the plot
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    # Remove the axis
    ax.axis('off')

    # set the DPI of the figure
    fig.set_dpi(300)

    return fig, ax


# ********************
# Streamlit home page
# ********************
def main():
    st.sidebar.success("Flick between Sections here!")

    st.title("A Better Method Scientist's Invented")
    st.header("Head-Related Transfer Functions (HRTF)")
    st.markdown("Although 'Head-Related Transfer Functions' is a complicated name, and they're complicated to understand, the idea behind them is quite simple.<br><br> You would have noticed when previously changing the delay, volume, and frequency that no matter how much you played around it was difficult to make a sound appear to come from a specific direction. That's because although those three factors significantly influence our ability to detect sound, the real world is complicated and these are not the only factors at play. The shape of your ear, how sound bounces off your body, and even the elevation the sound comes from can change our perception of a sound's origin.<br>Scientists invented a better way that trying to fiddle with the delay, volume, and pitch until sound appeared to come from the desired location. Instead they just measured the sound from every angle around a person by sticking a microphone in both of their ears. Then they used some math to calculate how the sound changed depending on the angle and elevation, and came up with HRTFs.", unsafe_allow_html=True)
    cola,colb=st.columns(2)
    with cola:
        st.image("data/images/page_3_image_left.png", use_column_width=True)
        st.markdown("<center><em>The equipment scientists used to collect audio data. Speakers play the same sound in lots of different positions and the sound in each ear is recorded</em></center>",unsafe_allow_html=True)

    with colb:
        st.image("data/images/page_3_image_right.png", use_column_width=True)
        st.markdown("<center><em>The chair spins the person on the spot so the scientists can record sound from every angle. The image shows they know the location of both the ears and every speaker.</em></center>",unsafe_allow_html=True)


    st.markdown("<br><b>Have a play with what they came up with! Just Change the angle and elevation",unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        audio_selection = st.radio(label = 'Select Sound',
                                    options = audio_file_options,
                                    horizontal = True)


    hrir_selection = 'Subject 1'
    

    # Add a slider for azimuth angle
    st.markdown("Move the sliders around and the two cartoon heads will show where the sound will appear to come from.")
    col1, col2 = st.columns(2)
    with col1:
        azimuth = st.select_slider(label = "Azimuth angle (degrees)",
                                    options = azimuth_options,
                                    value = 0)
        azimuth_fig, azimuth_ax = azimuth_diagram(azimuth = azimuth)
        st.pyplot(azimuth_fig)

    with col2:
        elevation = st.select_slider(label = "Elevation angle (degrees)",
                                    options = elevation_options,
                                    value = 0)
        elevation_fig, elevation_ax = elevation_diagram(elevation = elevation)
        st.pyplot(elevation_fig)
    
    audio_data = hrtf.hrtf_application(azimuth=azimuth,
                                        elevation=elevation,
                                        audio_selection=audio_selection,
                                        hrir_selection=hrir_selection)


    st.header("Play Audio")
    # Save the modified audio as a wave file in memory
    with io.BytesIO() as buffer:
        with wave.open(buffer, "wb") as wave_file:
            wave_file.setframerate(96000)
            wave_file.setnchannels(2)
            wave_file.setsampwidth(2)
            wave_file.writeframes(audio_data)

        # Get the wave file data as a byte string
        buffer.seek(0)
        wave_data = buffer.read()

    st.audio(wave_data, format='audio/wav')

    # Add button to refer to the next page
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('Return to Home', key="start_button", help="Click to return to the home page",use_container_width=True):
        # Open the other Streamlit page
            switch_page("home page")
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# ********************
# run main()
# ********************
if __name__ == '__main__':
    main()


