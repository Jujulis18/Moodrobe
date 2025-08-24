from ultralytics import YOLO
from datetime import datetime
from PIL import Image
import time
import tempfile

def predict_clothes(image):
    # Lire l'image
    #image = Image.open(uploaded_file)
    #st.image(image, caption='Image chargée', use_column_width=True)

    model = YOLO("./models/best.pt")
    
    # Sauvegarder temporairement l'image pour YOLO
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        tmp_path = tmp.name
    
    # Faire la prédiction
    results = model.predict(tmp_path, save=True)  # save=True crée runs/detect/exp avec l'image annotée
    
    # Afficher le résultat annoté
    #annotated_img_path = results[0].plot()  # récupère l'image annotée en array
    #st.image(annotated_img_path, caption="Résultat YOLO", use_column_width=True)


    classes = results[0].boxes.cls  
    detected_item = [results[0].names[int(c)] for c in classes]     

    annotated_img = results[0].plot()

    return detected_item, annotated_img, results[0]

