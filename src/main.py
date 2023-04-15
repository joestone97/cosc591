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
from netCDF4 import Dataset # to read Spatially Oriented Format for Acoustics (SOFA) files
from PIL import Image, ImageOps

# ********************
# define functions
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
    img = Image.open('images/top_down_head_01.png')

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
    img = Image.open('images/profile_head_01.png')

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

def read_sofa(file_name):
    sofa_data = Dataset(file_name, 'r', format='NETCDF4')

    # I think HRIR data set have left and right the wrong way around, so I flipped the index
    hrir_left = np.squeeze(sofa_data['Data.IR'][:, 1, :]) # [:, 0, :]
    hrir_right = np.squeeze(sofa_data['Data.IR'][:, 0, :]) # [:, 1, :]
    az, el, r = np.squeeze(np.hsplit(sofa_data['SourcePosition'][:], 3))
    # fs = sofa_data['Data.SamplingRate'][:][0] 
    return hrir_left, hrir_right, az, el, r

def count_channels(wave_file):
    # Open the WAV file
    with wave.open(wave_file, 'rb') as wf:
        # Get the number of channels
        nchannels = wf.getnchannels()
    return nchannels

def wave_to_float_array(wave_file):
    """
    Reads a WAV file and converts it to a numpy float array.
    
    Args:
        wave_file: The path to the WAV file.
        
    Returns:
        A numpy float array representing the audio data.
    """
    # Open the WAV file
    with wave.open(wave_file, 'rb') as wf:
        # Get the number of channels and sample width
        nchannels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        
        # Read all the audio data as a byte string
        data = wf.readframes(wf.getnframes())
        
    # Convert the byte string to a numpy array
    dtype_map = {1: np.int8, 2: np.int16, 4: np.int32}
    data_type = dtype_map[sample_width]
    array = np.frombuffer(data, dtype=data_type)
    
    # Convert the array to a float array
    max_val = np.iinfo(data_type).max
    array = array.astype(np.float32) / max_val
    
    # Reshape the array to have nchannels columns
    array = array.reshape(-1, nchannels)
    
    return array

def float_array_to_wave(array, sample_rate=44100, nchannels=1, sample_width=2):
    """
    Writes a numpy float array to a WAV file.
    
    Args:
        array: The numpy float array to write.
        sample_rate: The sample rate of the audio data (default 44100 Hz).
        nchannels: The number of channels (default 1).
        sample_width: The sample width in bytes (default 2).
    """
    # Scale the float array to the range [-1, 1]
    array = np.clip(array, -1, 1)
    max_val = np.iinfo(np.int16).max
    array = (array * max_val).astype(np.int16)
    
    # Reshape the array to have nchannels columns
    array = array.reshape(-1, nchannels)
    
    return array.tobytes()

def convolve_mono(audio_array, hrir_left, hrir_right):
    # left
    audio_left = audio_array[:,0]
    left = np.convolve(audio_left, hrir_left, mode='same')

    # right
    audio_right = audio_array[:,0]
    right = np.convolve(audio_right, hrir_right, mode='same')

    # convert to wave
    float_array = np.column_stack((left, right))
    stereo_audio = float_array_to_wave(array = float_array,
                                       sample_rate = 96000,
                                       nchannels = 2,
                                       sample_width = 2)
    
    return stereo_audio

def convolve_stereo(audio_array, hrir_left, hrir_right):
    # left
    audio_left = audio_array[:,0]
    left = np.convolve(audio_left, hrir_left, mode='same')

    # right
    audio_right = audio_array[:,1]
    right = np.convolve(audio_right, hrir_right, mode='same')

    # convert to wave
    float_array = np.column_stack((left, right))
    stereo_audio = float_array_to_wave(array = float_array,
                                       sample_rate = 96000,
                                       nchannels = 2,
                                       sample_width = 2)
    
    return stereo_audio
        
# ********************
# main() - streamlit dashboard
# ********************
def main():
    tab1, tab2 = st.tabs(["Introduction", "Experiment"])

    with tab1:
       st.title("Directional Hearing")
       st.header("TODO")

    with tab2:
       st.title("Directional Hearing")
       st.header("Head-Related Transfer Functions (HRTF)")

       st.header("Audio Input")

       col1, col2 = st.columns(2)

       with col1:
          audio_selection = st.radio(label = 'Select Input Audio',
                                     options = ['Sine Wave', 'Drums', 'Bird', 'Dog', 'Singer', 'Thunder'],
                                     horizontal = True)

       # define wave file name based on user selection
       if audio_selection == 'Sine Wave':
           audio_file = 'sine_96k.wav'
       elif audio_selection == 'Drums':
           audio_file = 'drums_96k.wav'
       elif audio_selection == 'Bird':
           audio_file = 'bird_chirping_96k.wav'
       elif audio_selection == 'Dog':
           audio_file = 'dog_barking_96k.wav'
       elif audio_selection == 'Singer':
           audio_file = 'singer_96k.wav'
       elif audio_selection == 'Thunder':
           audio_file = 'thunder_96k.wav'
       else:
           audio_file = 'sine_96k.wav'


       with col2:
          hrir_selection = st.radio(label = 'Select Head Related Impulse Response (HRIR)',
                                     options = ['Subject 1', 'Subject 2', 'Subject 3'],
                                     horizontal = True)
       
       # read HRIR from .sofa file
       if hrir_selection == 'Subject 1':
           sofa_file_name = 'Subject1_HRIRs.sofa'
       elif hrir_selection == 'Subject 2':
           sofa_file_name = 'Subject30_HRIRs.sofa'
       elif hrir_selection == 'Subject 3':
           sofa_file_name = 'Subject44_HRIRs.sofa'
       else:
           sofa_file_name = 'Subject1_HRIRs.sofa'
       
       # read SOFA data
       hrir_left, hrir_right, az, el, r = read_sofa(file_name = 'hrir/' + sofa_file_name)   
        
       # Add a slider for azimuth angle
       st.header("Parameters")
       col1, col2 = st.columns(2)

       with col1:
          azimuth = st.select_slider(label = "Azimuth angle (degrees)",
                                     options = [*range(0,360,5)],
                                     value = 0)

          azimuth_fig, azimuth_ax = azimuth_diagram(azimuth = azimuth)
          st.pyplot(azimuth_fig)

       with col2:
          elevation = st.select_slider(label = "Elevation angle (degrees)",
                                       options = [-57, -30, -15, 0, 15, 30, 45, 60, 75],
                                       value = 0)

          elevation_fig, elevation_ax = elevation_diagram(elevation = elevation)
          st.pyplot(elevation_fig)

       # with col1:
       #    azimuth_fig, azimuth_ax = azimuth_diagram(azimuth = azimuth)
       #    st.pyplot(azimuth_fig)

       # with col2:
       #    elevation_fig, elevation_ax = elevation_diagram(elevation = elevation)
       #    st.pyplot(elevation_fig)


       # Find the index of the measurement position that corresponds to the desired azimuth and elevation
       mp_indices = np.where((az == azimuth) & (el == elevation))[0]

       if len(mp_indices) == 0:
           raise ValueError(f"No measurement position found for azimuth={azimuth} and elevation={elevation}")
       elif len(mp_indices) > 1:
           raise ValueError(f"Multiple measurement positions found for azimuth={azimuth} and elevation={elevation}")
       index = mp_indices[0]
       # print(index)

       # get number of channels from wave file
       n_channels = count_channels(wave_file = 'audio/' + audio_file)

       # read wave file and convert to float array
       audio_array = wave_to_float_array(wave_file = 'audio/' + audio_file)
       
       # convolve audio
       if n_channels == 1:
          audio_data = convolve_mono(audio_array = audio_array,
                        hrir_left = hrir_left[index,:],
                        hrir_right = hrir_right[index,:])  
       elif n_channels == 2:
          audio_data = convolve_stereo(audio_array = audio_array,
                          hrir_left = hrir_left[index,:],
                          hrir_right = hrir_right[index,:])  

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

# ********************
# run main()
# ********************
if __name__ == '__main__':
    main()


