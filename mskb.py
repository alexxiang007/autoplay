import pyautogui
from time import sleep
import cv2
import numpy as np
import pyscreeze
from PIL import Image
# from matplotlib import pyplot as plt

# functions
def compare_pix(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)/300
def myregion(ux,uy,dx,dy):
    return (ux,uy,dx-ux+1,dy-uy+1)

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
    region = myregion(ux,uy,dx,dy)    
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

    return None

# find color
def sort(xy,score,limit=1000):
    length = len(xy)
    if length == 0:        
        return None,None
        
    index = sorted(range(length),key=lambda k:score[k])
    xy_return = []
    score_return = []
    for i in range(0,length,1):
        xy_return.append(xy[index[i]])
        score_return.append(score[index[i]])
        if i>= limit:
            break
    return xy_return,score_return

def hex_to_bgr(hex):
    hex = hex.lstrip('#')
    rgb = (tuple(int(hex[i:i+len(hex) // 3], 16) for i in range(0,len(hex),len(hex) // 3)))
    return(rgb[2],rgb[1],rgb[0])

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def find_pix(ux,uy,dx,dy,color,quality=0.8,repeat=1,interval=0.05,limit=1000, **kwargs):
    
    if isinstance(color, str):
        bgr = hex_to_bgr(color)
    elif isinstance(color, tuple):        
        bgr = color
    else:
        return None,None

    b = bgr[0]
    g = bgr[1]
    r = bgr[2]

    region = myregion(ux,uy,dx,dy)
    img1_data = Image.new('RGB',(1,1))
    img1_data.putdata([(b,g,r)])
    img1 = np.asarray(img1_data)

    for i in range(0,repeat,1):        
        img2 = np.array(pyscreeze.screenshot(region=region))
        w1,h1,cn1 = img1.shape
        w2,h2,cn2 = img2.shape        
        result = cv2.matchTemplate(img1,img2,cv2.TM_SQDIFF)/300         
        loc = np.where(result<=quality)
        xy = []
        score = []
        for pt in zip(*loc[::-1]):            
            xy.append((ux+pt[0],uy+pt[1]))
            score.append(result[pt[1],pt[0]])
        if len(xy)>=1:
            xy,score = sort(xy,score)
            return xy,score
        sleep(interval)

    return None,None

def find_multi_pix(ux,uy,dx,dy,colors,quality=0.5,repeat=1,interval=0.05,limit=5, **kwargs):
    if isinstance(colors, str):
        points = colors.split(",")
        length = len(points)
        rel_xy = []
        colors = []
        for i in range(0,length,1):
            if i == 0:
                colors.append(points[i].lstrip('"').rstrip('"'))
                rel_xy.append((0,0))
            else:               
                x,y,color = points[i].split("|")
                colors.append(color.lstrip('"').rstrip('"'))
                rel_xy.append((int(x.lstrip('"')),int(y.rstrip('"'))))
    else:
        return None

    xy,score = find_pix(ux,uy,dx,dy,colors[0],quality=0.2)
    num_starting_pts = len(score)    
    if num_starting_pts>limit:
        num_starting_pts = limit

    scores = []    
    for i in range(0,num_starting_pts,1):
        scores.append(score[i])
        for j in range(0,length,1):
            pix_tomatch = hex_to_bgr(colors[j])                        
            x_onscreen = 0
            y_onscreen = 0
            if int(xy[i][0]+rel_xy[j][0])<0 and int(xy[i][1]+rel_xy[j][1])>=0:
                x_onscreen = 0
                y_onscreen = int(xy[i][1]+rel_xy[j][1])
            elif int(xy[i][0]+rel_xy[j][0])>=0 and int(xy[i][1]+rel_xy[j][1])<0:
                x_onscreen = int(xy[i][0]+rel_xy[j][0])
                y_onscreen = 0
            elif int(xy[i][0]+rel_xy[j][0])<0 and int(xy[i][1]+rel_xy[j][1])<0:
                x_onscreen = 0
                y_onscreen = 0
            else:
                x_onscreen = int(xy[i][0]+rel_xy[j][0])
                y_onscreen = int(xy[i][1]+rel_xy[j][1])                
            pix_onscreen = pyautogui.pixel(x_onscreen,y_onscreen)            
            scores[i] = scores[i]+compare_pix(pix_tomatch,pix_onscreen)
        scores[i] = scores[i]/length
    xy,results = sort(xy[0:num_starting_pts],scores)
    if results[0]<1-quality:
        return xy[0],results[0]
    else:
        return None,None


_all__ = [
'moveto','left_down','left_up','right_down','right_up','left_click','right_click',
'scroll','key_press','key_press_alt','message','delay','find_pic','find_pix','find_multi_pix',
'hex_to_bgr','rgb_to_hex'
]