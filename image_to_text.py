# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:02:59 2019

@author: Nigel Tee
"""

from PIL import Image
import pytesseract
image = Image.open("Sample.png")
text = pytesseract.image_to_string(image, lang="eng")
print(text)