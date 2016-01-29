import multiprocessing
import Tkinter as tk
import cv2
from PIL import Image, ImageTk

e = multiprocessing.Event()
p = None

# -------begin capturing and saving video
def startrecording(e):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc,  20.0, (640,480))

    while(cap.isOpened()):
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        if ret==True:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
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

def quit():
    stoprecording()
    root.quit()
    root.destroy()

if __name__ == "__main__":
    # -------configure window
    root = tk.Tk()
    root.geometry("%dx%d+0+0" % (100, 130))
    startbutton=tk.Button(root,width=10,height=1,text='Start',command=start_recording_proc)
    stopbutton=tk.Button(root,width=10,height=1,text='Stop', command=stoprecording)
    pausebutton=tk.Button(root,width=10,height=1,text='Pause', command=pauserecording)
    quitbutton=tk.Button(root,width=10,height=1,text='Quit', command=quit)
    startbutton.pack()
    stopbutton.pack()
    quitbutton.pack()
    pausebutton.pack()
    lmain = tk.Label(root)
    lmain.pack()
    # -------begin
    root.mainloop()