# ********************
# import libraries
# ********************
import numpy as np
import wave

# ********************
# define functions
# ********************
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

def increase_sample_rate(file_path):
    # Open the audio file
    with wave.open(file_path, 'rb') as wav_file:
        # Get the sample rate and data of the original audio
        rate = wav_file.getframerate()
        data = wav_file.readframes(wav_file.getnframes())
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()

    # Convert the data to a numpy array of float32 values
    data = np.frombuffer(data, dtype=np.int16).astype(np.float32)

    # Set the new sample rate
    new_rate = 96000

    # Compute the ratio between the old and new sample rates
    rate_ratio = float(new_rate) / rate

    # Compute the new length of the audio
    new_length = int(len(data) * rate_ratio)

    # Resample the audio using linear interpolation
    time_indices = np.arange(len(data)) / rate
    new_time_indices = np.arange(new_length) / new_rate
    new_data = np.interp(new_time_indices, time_indices, data)

    # Convert the data back to int16 and save it to a new file
    new_data = new_data.astype(np.int16)
    with wave.open(file_path[:-4] + '_96k.wav', 'wb') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(new_rate)
        wav_file.writeframes(new_data)