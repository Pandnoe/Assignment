import streamlit as st
import time

def showProgressBar():
    progressBar = st.progress(0)
    for i in range(1, 101):
        progressBar.progress(i)
        time.sleep(0.03)
    time.sleep(0.2)