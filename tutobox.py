#!/usr/bin/env python

from moviepy.editor import *
from moviepy.video.tools.credits import credits1
import multiprocessing
import Tkinter as tk
import cv2
from PIL import Image, ImageTk
from moviepy.editor import *
from moviepy.video.tools.credits import credits1


width, height = 640, 480
cap = cv2.VideoCapture(0)

root = tk.Tk()
lmain = tk.Label(root)
lmain.pack()
e = multiprocessing.Event()
p = None

# -------begin capturing and saving video
def startrecording(e):
    fourcc = cv2.cv.CV_FOURCC(*'MJPG')
    out = cv2.VideoWriter('tmp/output.avi',fourcc,  20.0, (640,480))
    while(cap.isOpened()):
        if e.is_set():
            cap.release()
            out.release()
           # cv2.destroyAllWindows()
           # e.clear()
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
        else:
            break

def pauserecording(e):
    e.set()
    p.join()

def start_recording_proc():
    global p
    p = multiprocessing.Process(target=startrecording, args=(e,))
    p.start()

# -------end video capture and stop tk
def stoprecording():
	e.set()
	p.join()
	clip = (VideoFileClip('tmp/output.avi', audio=False))
	

	credits = credits1('settings/credits.txt',3*clip.w/4,gap=10,fontsize=20,color="white")
	scrolling_credits = credits.set_pos(lambda t:('center',-10*t)).set_start(3).crossfadein(1)
	titre = TextClip(txt="Tuto XXX", color="white",bg_color="black",fontsize=20).set_pos((80,15))
	logo = ImageClip("settings/logo.png").set_pos((0,0)).resize(height=50)

	final = CompositeVideoClip([clip,logo,scrolling_credits,titre])
	
	final.subclip(0,clip.duration).write_videofile("output/demo.mp4",fps=20) 

def quit():
	e.set()
	p.join()
	root.quit()
	root.destroy()

def show_frame():
    _, frame = cap.read()
   # frame = cv2.flip(frame, )
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

root.geometry("%dx%d+0+0" % (640, 560))
startbutton=tk.Button(root,width=10,height=1,text='Start',command=start_recording_proc)
stopbutton=tk.Button(root,width=10,height=1,text='Stop', command=stoprecording)
pausebutton=tk.Button(root,width=10,height=1,text='Pause', command=pauserecording)
quitbutton=tk.Button(root,width=10,height=1,text='Quit', command=quit)
startbutton.pack()
stopbutton.pack()
quitbutton.pack()
pausebutton.pack()
show_frame()
root.mainloop()