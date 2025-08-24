import cv2
import numpy as np
import pandas as pd
from collections import Counter
from typing import List, Tuple, Optional
import io
import logging


class ColorDetector:
    """Détecteur de couleurs avec palette de référence prédéfinie."""
    
    def __init__(self):
        self.palette_hex = self._load_color_palette()
        self.palette_rgb = np.array([self._hex_to_rgb(color) for color in self.palette_hex])
        self.palette_map = {
            tuple(int(c) for c in rgb): hex_color
            for rgb, hex_color in zip(self.palette_rgb, self.palette_hex)
        }
    
    def _load_color_palette(self) -> List[str]:
        palette_data = '''FFDAB9,AFEEEE,AAF0D1,F8BBD0,F8F8FF,E6E6FA,F6D1C1,A7C7E7,98FF98,FFFFE0,
F5DEB3,FF7F50,C7EA46,D8BFD8,FFFFF0,40E0D0,FF6F61,87CEEB,FF69B4,8DB600,
FFD700,87CEFA,7FFFD4,00A36C,5DADEC,FFF44F,C8A2C8,C19A6B,FFA07A,66BB44,
FF6347,FF4500,00CED1,002FA7,046307,00E5EE,BFFF00,7CFC00,C0C0C0,FF1493,
FFFF00,9370DB,B0E0E6,D9D9D9,BFA5D9,AEC6CF,E68FAC,6CA0DC,A3C1AD,8B8589,
8D3F6D,6A5ACD,915F6D,1C2841,6A0DAD,C71585,E30B5C,BA55D3,B38B6D,BEBEBE,
0033CC,87AFC7,9DC183,C08081,9CAF88,D2B48C,708090,702963,191970,C3B091,
B7410E,A3C585,8A9A5B,836953,800020,D4AF37,A9A9A9,FFD966,FFA500,78866B,
556B2F,8B4513,A0522D,4E342E,2F2F2F,014421,355E3B,CC5500,8B0000,6F4E37,
4B5320,3D2B1F,8B2500,B8860B,3B5323,5C0120,2B1B17,004B49,4B0082,B22222,
1C1C2D,FFFFFF,000000,E10600,8000FF,C71585'''
        
        return [color.strip() for color in palette_data.replace('\n', '').split(',')]
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convertit une couleur hex en RGB.
        
        Args:
            hex_color: Couleur au format hex (avec ou sans #)
            
        Returns:
            Tuple RGB (r, g, b)
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)



    
    def find_closest_color(self, target_hex: str) -> Tuple[str, np.ndarray]:
        """Trouve la couleur la plus proche dans la palette.
        
        Args:
            target_hex: Couleur cible au format hex
            
        Returns:
            Tuple (hex_color, rgb_array) de la couleur la plus proche
        """
        target_rgb = np.array(self._hex_to_rgb(target_hex))
        distances = np.linalg.norm(self.palette_rgb - target_rgb, axis=1)
        closest_idx = np.argmin(distances)
        return self.palette_hex[closest_idx], self.palette_rgb[closest_idx]
    
    #img doit etre en cv2
    def extract_dominant_colors(self, image_crop, 
                              top_n: int = 3, 
                              center_size: int = 5) -> List[Tuple[int, int, int]]:
        """Extrait les couleurs dominantes d'une zone d'image.
        
        Args:
            image_crop: Zone d'image découpée (format BGR)
            top_n: Nombre de couleurs principales à extraire
            center_size: Taille de la zone centrale à analyser
            
        Returns:
            Liste des couleurs dominantes en format RGB
        """

        rgb_crop = cv2.cvtColor(image_crop, cv2.COLOR_BGR2RGB)
        

        h, w = rgb_crop.shape[:2]
        center_h, center_w = h // 2, w // 2

        y1 = max(0, center_h - center_size)
        y2 = min(h, center_h + center_size)
        x1 = max(0, center_w - center_size)
        x2 = min(w, center_w + center_size)
        
        center_crop = rgb_crop[y1:y2, x1:x2]
        

        pixels = center_crop.reshape(-1, 3)
        pixel_tuples = [tuple(pixel) for pixel in pixels]
        

        color_counter = Counter(pixel_tuples)
        most_common_colors = color_counter.most_common(top_n + 20)  
        
  
        return [color for color, _ in most_common_colors[:top_n]]
    
    def detect_colors_from_boxes(self, image, 
                                detection_results) -> List[List[Tuple[int, int, int]]]:
        """Détecte les couleurs pour chaque boîte de détection.
        
        Args:
            image: Image source
            detection_results: Résultats de détection avec boxes et classes
            
        Returns:
            Liste des couleurs pour chaque boîte détectée
        """
        
        colors_per_box = []
        
        for box, cls in zip(detection_results.boxes.xyxy, detection_results.boxes.cls):
            
            x1, y1, x2, y2 = map(int, box)
            class_name = detection_results.names[int(cls)]
            
            # Découper la zone détectée
            crop = image[y1:y2, x1:x2]
            
            # top_n = 3
            if crop.size > 0:
                colors = self.extract_dominant_colors(crop, top_n=4)
                colors_per_box.append(colors)
            else:
                colors_per_box.append([])

        # Récupérer les couleurs les plus fréquentes
        flat_colors = [c for sublist in colors_per_box for c in sublist]
        color_counter = Counter(flat_colors)
        most_common_colors = color_counter.most_common(3)

        
        most_common_colors_hex = []
        for rgb, count in most_common_colors:
            target_hex = self._rgb_to_hex(tuple(int(c) for c in rgb))
            hex_color, _ = self.find_closest_color(target_hex)
            most_common_colors_hex.append((hex_color, count))

        
        return most_common_colors_hex, color_counter

def detection_eval():
    top_contributors = {}
    errors = {}

    for mapped_color, original_colors in mapping.items():
   
        counts = Counter(original_colors)
        top_k = [c for c, _ in counts.most_common(top_k_contributors)]
        top_contributors[mapped_color] = top_k
        
        # Calculer l'erreur moyenne
        distances = [color_distance(mapped_color, c) for c in original_colors]
        errors[mapped_color] = np.mean(distances)


    print("Mapping couleur palette -> couleurs originales contributrices:")
    for k, v in top_contributors.items():
        print(f"{k}: {v}")

    print("\nErreur moyenne par couleur mappée:")
    for k, v in errors.items():
        print(f"{k}: {v:.2f}")

def detect_colors(image, detection_results) -> List[List[Tuple[int, int, int]]]:
    """Fonction principale pour détecter les couleurs dans une image.
    
    Args:
        image: Image au format numpy array
        detection_results: Résultats de détection d'objets
        
    Returns:
        Liste des couleurs dominantes pour chaque objet détecté
    """
    image_rgb = np.array(image)
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    detector = ColorDetector()
    return detector.detect_colors_from_boxes(image, detection_results)

def get_palette():
    detector = ColorDetector()
    return detector.palette_hex

