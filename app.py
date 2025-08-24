## App.py
import streamlit as st
import pandas as pd
#from pages.page1 import display_dashboard
from modules import page1, page2
from pathlib import Path
from scripts.sheet_api import SheetApi

# 
@st.cache_data

def load_data():
    data_path = Path(__file__).parent / "data" / "raw" / "df_combined.csv"
    data = pd.read_csv(data_path)
    return data


def get_access_api():
	connexion = SheetApi()
	if "sheet" not in st.session_state:
		st.session_state.sheet_api = connexion
	if "IS_PUBLIC" not in st.session_state:
		st.session_state.IS_PUBLIC = connexion.IS_PUBLIC

def main():

	#import sys
	#import os
	#print("Python executable:", sys.executable)
	#print("PYTHONPATH:", os.environ.get("PYTHONPATH"))
	get_access_api()
	tab1, tab2 = st.tabs(["Accueil", "Mood calendar"])
	with tab1:
		page1.show()

	with tab2:
		page2.show()


if __name__ == "__main__":
    main()
