import pyautogui
from time import sleep
import cv2
import numpy as np
from PIL import Image

# functions
def compare_pix(a,b):
    return (255-np.max([abs(a[0]-b[0]),abs(a[1]-b[1]),abs(a[2]-b[2])]))/255

# mouse control
def moveto(x,y,duration=0.05):
	pyautogui.moveTo(x,y,0,0,duration,pyautogui.easeOutElastic)

def left_down():
    pyautogui.mouseDown()

def left_up():
    pyautogui.mouseUp()

def right_down():
    pyautogui.mouseDown(button='right')

def right_up():
    pyautogui.mouseUp(button='right')

def left_click(x=None,y=None):
    if x==None or y==None:
    	pyautogui.click()    
    else:
    	pyautogui.click(x,y)    

def right_click(x=None,y=None):
    if x==None or y==None:
    	pyautogui.click(button='right')    
    else:
    	pyautogui.click(x,y,button='right')       

def scroll(dist):
    pyautogui.scroll(dist)

# keyboard control
def key_press(keys):
	pyautogui.press(keys)

def key_press_alt(key):
	pyautogui.hotkey('alt',key)

# other control
def message(text, title='Alert', button='OK'):
	pyautogui.alert(text=text,title=title,button=button)

def delay(t):
	sleep(t/1000)

# find picture
def find_pic(ux,uy,dx,dy,img,quality=0.8,repeat=1,interval=0.05, **kwargs):
    region = (ux,uy,dx,dy)    
    img1 = cv2.imread(img)

    for i in range(0,repeat,1):        
        img2 = np.array(pyscreeze.screenshot(region=region))
        w1,h1,cn1 = img1.shape
        w2,h2,cn2 = img2.shape
        img1_gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img1_gray,img2_gray,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result>=quality)    
        xy = []
        score = []
        for pt in zip(*loc[::-1]):
            if pt == (0,0):
                continue
            xy.append(pt)
            score.append(result[pt[1],pt[0]])
        if len(xy)>=1:
            max_score = np.max(score)
            max_xy = xy[np.argmax(score)]
            return max_xy
        sleep(interval)

    return (-1,-1)

# find color
def find_pix(ux,uy,dx,dy,r,g,b,quality=0.8,repeat=1,interval=0.05, **kwargs):
 
    
# find_pix(0,0,1920,1080,0,0,0)
# find word


