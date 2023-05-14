def volume(ear, file, scaling_factor):
    """
    Function provides back-end functionality for the volume section of the web app

    The function has three steps:
        1.Reads an audio file from the ./data/audio/ folder
        2.Augments audio file based on input arguments
        3.Writes output to the temporary file in the ./data/audio/ folder

    note: the data in the returned "y_scaled" variable is redundant and simply triggers the reloading of a widget on the front end
    """
    import soundfile as sf
    import numpy as np
    y, sr = sf.read('./data/audio/'+ file)

    if ear=="left":
        # Apply the scaling factor to the left channel
        left_scaled = y[:, 0] * scaling_factor

        # Combine the scaled left channel and the right channel
        y_scaled = np.vstack((left_scaled, y[:, 1])).T
        sf.write('./data/audio/volume_overwrite.wav', y_scaled, sr, format='WAV')

    else:
        right_scaled = y[:, 1] * scaling_factor
        y_scaled = np.vstack((y[:,0], right_scaled)).T
        sf.write('./data/audio/volume_overwrite.wav', y_scaled, sr, format='WAV')

    return(y_scaled)

