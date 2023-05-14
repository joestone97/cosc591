def delay(ear, file, delay_time):
    """
    Function provides back-end functionality for the delay section of the web app

    The function has three steps:
        1.Reads an audio file from the ./data/audio/ folder
        2.Augments audio file based on input arguments
        3.Writes output to the temporary file in the ./data/audio/ folder

    note: the data in the returned "y_delayed" variable is redundant and simply triggers the reloading of a widget on the front end
    """
    import soundfile as sf
    import numpy as np
    #read selected audio file
    y, sr = sf.read('./data/audio/'+ file)

    #quick catch for the bug caused by no delay input or a delay being too small given sample frequency
    if delay_time == 0.0 or delay_time == 1e-05:
        return(y)
    sf.write('./data/audio/delay_overwrite.wav', y, sr, format='WAV')
    # Convert the delay time from seconds to samples
    delay_samples = int(delay_time * sr)

    # Create an empty array to hold the delayed signal
    left = y[:, 0]
    right = y[:, 1]

    # Apply the delay line algorithm to the left channel
    blank_section = np.zeros(delay_samples)
    if ear == "left":
        after_1_second = left[:-delay_samples]
        concatenated_array = np.concatenate((blank_section, after_1_second), axis=0)
        # Combine the delayed left channel and the right channel
        y_delayed = np.vstack((concatenated_array, right)).T
        sf.write('./data/audio/delay_overwrite.wav', y_delayed, sr, format='WAV')
    else:
        after_1_second = right[:-delay_samples]
        concatenated_array = np.concatenate((blank_section, after_1_second), axis=0)
        # Combine the delayed left channel and the right channel
        y_delayed = np.vstack((left,concatenated_array)).T
        sf.write('./data/audio/delay_overwrite.wav', y_delayed, sr, format='WAV')

    return(y_delayed)

