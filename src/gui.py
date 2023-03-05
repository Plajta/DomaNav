import cv2
import numpy as np
from localization.finder import finder

f = finder()
index, len = f.find()

img = np.zeros((400,500))
x = index//5
y = index%5
x *= 100
y *= 100
print("X: "+str(x)+" Y: "+str(y))
img[x:x+100,y:y+100]=1

cv2.imshow('L',img)
cv2.waitKey(0)