import pyedflib
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import streamlit as st
import tempfile
import os

def preprocess_data(data, fs):
    # Apply signal processing and filtering operations here
    # Example: Apply a high-pass filter
    cutoff = 1  # High-pass filter cutoff frequency (modify as needed)
    b, a = signal.butter(4, cutoff / (fs / 2), 'highpass', analog=False)
    filtered_data = signal.filtfilt(b, a, data, axis=0)
    return filtered_data

def plot_signals(raw_data, filtered_data, channel_names, fs):
    num_channels = raw_data.shape[1]
    time = np.arange(raw_data.shape[0]) / fs

    fig, axs = plt.subplots(num_channels, 2, figsize=(12, 3 * num_channels))
    for channel in range(num_channels):
        axs[channel, 0].plot(time, raw_data[:, channel])
        axs[channel, 0].set_title(f'Raw Signal - Channel {channel+1}: {channel_names[channel]}')
        axs[channel, 0].set_xlabel('Time (s)')
        axs[channel, 0].set_ylabel('Amplitude')

        axs[channel, 1].plot(time, filtered_data[:, channel])
        axs[channel, 1].set_title(f'Filtered Signal - Channel {channel+1}: {channel_names[channel]}')
        axs[channel, 1].set_xlabel('Time (s)')
        axs[channel, 1].set_ylabel('Amplitude')

    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("EEG/EMG Signal Analysis App")
    st.write("-Rithvik Sabnekar")
    st.write("Please wait at least 1 minute for detailed analytical graphs")
    st.markdown(f'<a href="https://drive.google.com/file/d/1TjXY6Ip_W_jfpFTThWZ2DmOIJ1OF99ZH/view?usp=sharing" download>Example Input file (S001R03.edf), source: https://www.physionet.org/content/eegmmidb/1.0.0/</a>', unsafe_allow_html=True)

    
    # Step 2: Data Upload
    uploaded_file = st.file_uploader("Upload EEG/EMG data file (.edf type)\n\nThe main purpose of EEG/EMG (Electroencephalography/Electromyography) analysis is to study and understand the electrical activity of the brain (EEG) or muscle activity (EMG). These techniques are widely used in neuroscience and clinical settings to gain insights into brain function, monitor sleep patterns, diagnose neurological disorders, and assess the effectiveness of treatments.", type=["edf"])

    if uploaded_file is not None:
        # Step 3: Data Preprocessing
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_filename = tmp_file.name
            uploaded_file.seek(0)
            tmp_file.write(uploaded_file.read())

            edf_data = pyedflib.EdfReader(tmp_filename)
            num_channels = edf_data.signals_in_file
            channel_names = edf_data.getSignalLabels()
            raw_data = []
            for channel in range(num_channels):
                raw_data.append(edf_data.readSignal(channel))
            raw_data = np.array(raw_data).T  # Transpose to have channels in columns
            fs = edf_data.samplefrequency(0)  # Get the sampling frequency from the first channel
            filtered_data = preprocess_data(raw_data, fs)

        # Step 4: Visualizations
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(101):
            status_text.text(f"Processing... {i}%")
            progress_bar.progress(i)
            time.sleep(0.01)  # Simulate some processing time

        # Display the final result
        progress_bar.empty()
        status_text.empty()
        plot_signals(raw_data, filtered_data, channel_names, fs)

        # Close the EDF file
        edf_data.close()

        # Delete the temporary file
        os.remove(tmp_filename)

if __name__ == '__main__':
    main()
