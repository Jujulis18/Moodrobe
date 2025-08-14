import streamlit as st
from datetime import datetime
from PIL import Image
import time
from scripts.yolov8n_cloth import predict_clothes


if 'page' not in st.session_state:
    st.session_state.page = 'page1'

def display_dashboard():
	if st.session_state.page == 'page1':
		st.set_page_config(layout="wide")
		
		# --- Titre ---
		st.title("Analyse de mes vêtements")

		# --- Upload de l'image ---
		uploaded_file = st.file_uploader("Upload une photo de ton vêtement", type=["jpg", "png", "jpeg"])

		if uploaded_file:
		    # Affichage immédiat de l'image
		    image = Image.open(uploaded_file)
		    st.image(image, caption="Image uploadée", width=200 )
		    
		    # --- Section d'analyse ---
		    with st.spinner("Analyse en cours... ⏳"):
		        #time.sleep(2)  
		        detected_items, img_predict = predict_clothes(image)

		        detected_color = "Bleu"  
		        season = "Été"  
		        
		    st.success("Analyse terminée ✅")
		    
		    # --- Résumé de ce qui a été trouvé ---
		    st.subheader("Résumé de l'analyse")
		    st.write(f"**Date :** {datetime.today().strftime('%Y-%m-%d')}")
		    st.write(f"**Vêtements :** {detected_items}")
		    st.write(f"**Couleur :** {detected_color}")
		    st.write(f"**Saison :** {season}")
		    st.image(img_predict, caption="Résultat YOLO", width=200)
		    # tu peux ajouter d'autres infos ici
		    
		    # --- Bouton Mood ---
		    if st.button("Afficher le mood associé 🎨"):
		        # TODO : ici tu branches ton algo mood
		        # Par exemple : afficher plusieurs images liées à la couleur détectée
		        st.subheader("Mood du jour")
		        st.write(f"Basé sur la couleur **{detected_color}**")
		        # Exemple : afficher plusieurs images
		        st.image(["exemple1.jpg", "exemple2.jpg"], width=150)  # à remplacer par tes images
