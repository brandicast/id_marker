from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
import sys
import os.path
from util import log

def putChineseText (im,text,pos,color,font='NotoSansCJK-Bold.ttc', size=25):
    img_PIL = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
    log (resource_path(font))
    font = ImageFont.truetype(resource_path(font),size)
    fillColor = color #(255,0,0)
    position = pos #(100,100)
    #if not isinstance(chinese,unicode):
    #    chinese = chinese.decode('utf-8')
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position,text,font=font,fill=fillColor)
 
    img = cv2.cvtColor(np.asarray(img_PIL),cv2.COLOR_RGB2BGR)
    return img

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)