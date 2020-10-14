import cv2
import tkinter as tk
import tkinter.font as tf
from PIL import Image,ImageTk

def video_loop():
    success, img = capture.read()  
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    video_show.imgtk = ImageTk.PhotoImage( image=Image.fromarray(cv2image) )
    
    video_show.config(image=video_show.imgtk)
    
    win.after(1, video_loop)
    
win = tk.Tk()
win.title('Hxa')
win.geometry('1000x600')    

capture = cv2.VideoCapture(0)    #摄像头

video_show = tk.Label(win)  
video_show.place(height = 360,width = 480,x = 0,y = 0)

var=tk.StringVar()
var.set("aaa\naaaaa")
result_show = tk.Label(win,anchor="nw",
                           textvariable = var,
                           justify = "left",
                           relief="ridge",
                           font=tf.Font(size=12,family='Microsoft YaHei')
                       )  
result_show.place(height = 360,width = 100,x = 580,y = 0)

video_loop()
win.mainloop()

capture.release()
cv2.destroyAllWindows()