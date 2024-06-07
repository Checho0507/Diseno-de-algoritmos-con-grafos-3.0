import uuid
import pandas as pd
import streamlit as st
import re
import numpy as np
from scipy.stats import wasserstein_distance

def restablecer_matriz():
    original = [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
    ]
    global probabilities
    if probabilities != original:
        st.warning("Se perderán los cambios actuales")
        if st.button("Confirmar"):
            probabilities = original
    else:
        st.success("Se restableció la matriz original")


# Add other utility functions here, including those for probability calculations and EMD.
