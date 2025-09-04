# app.py

import os
from click import echo
import streamlit as st
import pandas as pd
import numpy as np #noqa
import time
import sqlite3
from datetime import datetime, timedelta #noqa
from model import flag_pos_anomalies, rolling_alert_recommendation

st.set_page_config(page_title="Incident Monitor", layout="wide", page_icon="🏠")
st.title("Home")

