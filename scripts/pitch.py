# ********************
# pitch
# ********************
def pitch(ear,file,change):
    import librosa
    import numpy as np
    import soundfile as sf

    y, sr = librosa.load('./data/audio/'+ file,mono=False)

    # Extract the left and right channels
    left = y[0]
    right = y[1]
    left_np = np.array(left)
    right_np = np.array(left)

    if ear == "left":
        # Shift the pitch of the left channel up by 2 semitones
        left_shifted = librosa.effects.pitch_shift(left_np, sr=sr, n_steps=change, bins_per_octave=12)
        # Combine the shifted left channel and the right channel to create the final stereo signal
        y_shifted = np.vstack((left_shifted, right)).T
        sf.write('./data/audio/pitch_overwrite.wav', y_shifted, sr, format='WAV')
    elif ear=="right":
        right_shifted = librosa.effects.pitch_shift(right_np, sr=sr, n_steps=change, bins_per_octave=12)
        # Combine the shifted left channel and the right channel to create the final stereo signal
        y_shifted = np.vstack((left, right_shifted)).T
        sf.write('./data/audio/pitch_overwrite.wav', y_shifted, sr, format='WAV')
    #else:
    #    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=change, bins_per_octave=12)
    #    sf.write('./data/audio/pitch_overwrite.wav', y_shifted, sr, format='WAV')
    return(y_shifted)

# ********************
# lowpass filter
# ********************
def wave_to_float_array(wave_file):
    """
    Reads a WAV file and converts it to a numpy float array.
    
    Args:
        wave_file: The path to the WAV file.
        
    Returns:
        A numpy float array representing the audio data.
    """
    # import libraries
    import wave
    import numpy as np

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
    # import libraries
    import wave
    import numpy as np

    # Scale the float array to the range [-1, 1]
    array = np.clip(array, -1, 1)
    max_val = np.iinfo(np.int16).max
    array = (array * max_val).astype(np.int16)
    
    # Reshape the array to have nchannels columns
    array = array.reshape(-1, nchannels)
    
    return array.tobytes()

def apply_lowpass_filter(ear, wave_file, cutoff_freq, order):
    """
    Applies a lowpass filter to a WAV file.
    
    Args:
        wave_file: The WAV file to filter.
        cutoff_freq: The cutoff frequency for the lowpass filter.
        order: The order of the Butterworth filter used to apply the lowpass filtering (i.e., the steepness)
    """
    
    # import libraries
    import wave
    import numpy as np
    import scipy.signal as signal

    # get audio file data
    with wave.open('./data/audio/' + wave_file, 'rb') as w:
        # Get the sample rate and data of the original audio
        sample_rate = w.getframerate()
    
    # convert to numpy array
    audio_array = wave_to_float_array(wave_file = './data/audio/' + wave_file)
    
    # Define filter parameters
    nyquist_freq = 0.5 * sample_rate
    normalized_cutoff_freq = cutoff_freq / nyquist_freq
    b, a = signal.butter(order, normalized_cutoff_freq, 'low')
    
    # map left/right ear to left/right channel
    if ear == 'left':
        filtered_channel = 0
        unfiltered_channel = 1
    else:
        filtered_channel = 1
        unfiltered_channel = 0

    # Apply filter to selected channel
    filtered_audio = np.zeros_like(audio_array)
    filtered_audio[:, filtered_channel] = signal.lfilter(b, a, audio_array[:, filtered_channel])
    # filtered_audio[:, unfiltered_channel] = signal.lfilter(b, a, audio_array[:, unfiltered_channel])
    filtered_audio[:, unfiltered_channel] = audio_array[:, unfiltered_channel]
    
    filtered_wave = float_array_to_wave(array=filtered_audio, sample_rate=96000, nchannels=2, sample_width=2)

    # write filtered audio to file
    with wave.open('./data/audio/pitch_overwrite.wav', "wb") as w:
        w.setframerate(96000)
        w.setnchannels(2)
        w.setsampwidth(2)
        w.writeframes(filtered_wave)
    
    return filtered_audio