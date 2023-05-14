import streamlit as st
import numpy as np
import wave
import matplotlib.pyplot as plt
import pickle
import gzip
# from netCDF4 import Dataset # to read Spatially Oriented Format for Acoustics (SOFA) files
from PIL import Image, ImageOps

# def write_compressed_pickle(data, file_name):
#     with gzip.open(file_name, 'wb') as f:
#         pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def read_compressed_pickle(file_name):
    with gzip.open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data

def read_hrir(file_name):
    hrir = read_compressed_pickle(file_name)
    return hrir['left'], hrir['right'], hrir['azimuth'], hrir['elevation'], hrir['radius']

# def read_sofa(file_name):
#     sofa_data = Dataset(file_name, 'r', format='NETCDF4')

#     # I think HRIR data set have left and right the wrong way around, so I flipped the index
#     hrir_left = np.squeeze(sofa_data['Data.IR'][:, 1, :]) # [:, 0, :]
#     hrir_right = np.squeeze(sofa_data['Data.IR'][:, 0, :]) # [:, 1, :]
#     az, el, r = np.squeeze(np.hsplit(sofa_data['SourcePosition'][:], 3))
#     # fs = sofa_data['Data.SamplingRate'][:][0] 
#     return hrir_left, hrir_right, az, el, r

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

def hrtf_application(azimuth,elevation,audio_selection,hrir_selection):
    import streamlit as st
    import numpy as np
    import wave
    import io
    import matplotlib.pyplot as plt
    from netCDF4 import Dataset # to read Spatially Oriented Format for Acoustics (SOFA) files
    from PIL import Image, ImageOps

    #valid files (just turned the if statements to a dictionary for clarity)
    audio_file = {
        "Sine Wave":"sine_96k.wav",
        "Drums":"drums_96k.wav",
        "Bird":"bird_chirping_96k.wav",
        "Dog":"dog_barking_96k.wav",
        "Singer":"singer_96k.wav",
        "Thunder":"thunder_96k.wav"
    }
    sofa_file_name = {
        # "Subject 1":"Subject1_HRIRs.sofa",
        # "Subject 2":"Subject30_HRIRs.sofa",
        # "Subject 3":"Subject44_HRIRs.sofa"
        "Subject 1":"subject_01.pkl.gz",
        "Subject 2":"subject_30.pkl.gz",
        "Subject 3":"subject_44.pkl.gz"
    }


    #find audio file from inputted selection
    audio_file = audio_file[audio_selection]

    #find sofa file from selection
    sofa_file_name = sofa_file_name[hrir_selection]

    # read SOFA data
    # hrir_left, hrir_right, az, el, r = read_sofa(file_name = './data/hrir/' + sofa_file_name)
    hrir_left, hrir_right, az, el, r = read_hrir(file_name = './data/hrir/' + sofa_file_name)
    #calculate index from azimuth/elevation
    # Find the index of the measurement position that corresponds to the desired azimuth and elevation
    mp_indices = np.where((az == azimuth) & (el == elevation))[0]

    # get number of channels from wave file
    n_channels = count_channels(wave_file = './data/audio/' + audio_file)

    # read wave file and convert to float array
    audio_array = wave_to_float_array(wave_file = './data/audio/' + audio_file)

    if len(mp_indices) == 0:
        raise ValueError(f"No measurement position found for azimuth={azimuth} and elevation={elevation}")
    elif len(mp_indices) > 1:
        raise ValueError(f"Multiple measurement positions found for azimuth={azimuth} and elevation={elevation}")
    index = mp_indices[0]

    # convolve audio
    if n_channels == 1:
        audio_data = convolve_mono(audio_array = audio_array,
                    hrir_left = hrir_left[index,:],
                    hrir_right = hrir_right[index,:])  
    elif n_channels == 2:
        audio_data = convolve_stereo(audio_array = audio_array,
                        hrir_left = hrir_left[index,:],
                        hrir_right = hrir_right[index,:])
        
    return(audio_data)
