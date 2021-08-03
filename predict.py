# Arda Mavi
import cv2
import numpy as np
import skimage.transform as st
def predict(model, X):
    X = cv2.resize(X, (150, 150))
    Y = model.predict(X.reshape(1,150,150,3))
    return Y
