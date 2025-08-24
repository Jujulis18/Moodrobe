import gspread
from google.oauth2.service_account import Credentials
import datetime
import streamlit as st
import pandas as pd
import traceback


class SheetApi:

    def __init__(self):
        self.sheet, self.IS_PUBLIC = self._connexion()

    @staticmethod
    def _connexion():
        try:            
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            
            if "gcp_service_account" in st.secrets: 
                creds_dict = st.secrets["gcp_service_account"]
                creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
                #st.info("Mode CLOUD détecté (Streamlit secrets)")
            #else:  
            #    st.info("Get secret")
            #    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            #    st.info("Mode LOCAL détecté (credentials.json)")
                
                client = gspread.authorize(creds)
                sheet = client.open("moodrobe_sheet").sheet1
                IS_PUBLIC = False
                #st.info("Mode PRIVÉ : accès Google Sheets activé")

            return sheet, IS_PUBLIC

        except Exception as e:
            IS_PUBLIC = True
            #st.error(f"Erreur lors de la connexion : {e}")
            p#rint("Stacktrace complète :", e, flush=True)
            #st.text(traceback.format_exc())
            st.info("Mode PUBLIC : pas d'accès à Google Sheets")
            return None, IS_PUBLIC
    
    def get_all_data(self):
        all_rows = self.sheet.get_all_values()  
        df = pd.DataFrame(all_rows[1:], columns=all_rows[0])  
        return df


    def save_data(self, data):
        self.sheet.append_row(data)

