
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import streamlit as st

def extract_string(regex_t: str) -> str | None:
    """regex_t: the regex to match in the string"""
    search = re.search(regex_t, entry)
    if search is not None:
        groups = search.group()
        if isinstance(groups, str):
            print("Expected. Found one matching")
            return groups

        elif isinstance(groups, tuple):
            print("Unexpected. Found more than one matching")
            raise ValueError(f"Found the following matches: {groups}")
        else:
            raise ValueError("Unexpected. Did not find exactly one matching")
        
# GUI: File upload component
file = st.file_uploader("Log file",
                 type=['log', 'txt']
                 )
if file:
    entries: bytes = file.readlines()

    observations = []

    for interim_entry in entries:
        # Read the bytes in as an in memory file object
        stringio = StringIO(interim_entry.decode("utf-8"))
        # Read from the file object as string
        entry: str = stringio.read()

        timestamp = None
        status = None
        
        regex_t = r'\d+-\d+-\d+ \d+:\d+:\d+'
        
        
        search_a = re.search("The service quality of DNS on wan1 is low", entry)
        if search_a is not None:
            timestamp = extract_string(regex_t)
            status = 0
        
        search_a = re.search("The service quality of DNS on wan1 is recovered", entry)
        if search_a is not None:
            timestamp = extract_string(regex_t)
            status = 1
            
        observations.append((timestamp, status))


    df = pd.DataFrame(observations)

    df.dropna(inplace=True)
    df.index = pd.to_datetime(df.iloc[:,0])
    df.columns = ['timestamp', 'state']
    df.drop(columns='timestamp', inplace=True)


    fig, ax = plt.subplots(figsize=(20, 6))

    # Perform plotting operations on the axes object 'ax'
    ax.step(df.index, df.state, where='post')
    ax.set_title("Router Uptime vs Downtime")
    ax.set_xlabel("Time")
    ax.set_ylabel("State (0=Down, 1=Up)")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Downtime', 'Uptime']) # Optional: more descriptive labels
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, axis='y', linestyle=':')

    # Display the figure in Streamlit
    st.pyplot(fig)
