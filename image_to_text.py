# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:02:59 2019

@author: Nigel Tee
"""
from PIL import Image
import pytesseract


class ImageToText:
    def __init__(self, name):
        self.name = name

    def print_filename(self):
        image = Image.open(self.name)
        text = pytesseract.image_to_string(image, lang="eng")
        print(text)
