import sqlite3
import cv2
import numpy as np
import os
from math import sqrt, ceil, floor

class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def get_winners_img(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('''SELECT image FROM winners 
                           INNER JOIN prizes ON winners.prize_id = prizes.prize_id 
                           WHERE user_id = ?''', (user_id, ))
            return cur.fetchall()

def create_collage(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is not None:
            images.append(cv2.resize(img, (200, 200)))
    
    if not images: return None
    num_cols = max(1, floor(sqrt(len(images))))
    num_rows = ceil(len(images) / num_cols)
    h, w, _ = images[0].shape
    collage = np.zeros((num_rows * h, num_cols * w, 3), dtype=np.uint8)
    for i, img in enumerate(images):
        r, c = i // num_cols, i % num_cols
        collage[r*h:(r+1)*h, c*w:(c+1)*w, :] = img
    return collage
