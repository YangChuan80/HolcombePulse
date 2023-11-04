#!/usr/bin/env python
# coding: utf-8

# # Holcombe Pulse

# ## Modules

# In[85]:


import max30102
import tkinter as tk
import time
import threading


# ### Sensor Connection

# In[ ]:


m = max30102.MAX30102() # sensor initialization


# ### Helper Functions

# In[86]:


str_rpm = '0'
str_speed = '0'

str_coolant_temp = '0'
str_fuel_level = '0'

str_intake_temp = '0'
str_throttle_pos = '0'
str_intake_pressure = '0'

indicator = 0


# In[87]:


def parsePulse():
    global red, ir, indicator
    
    while(1):
        
        # Determine Whether Meet the Requirements
        if indicator == 1:
            break
            
        # Parameter Adoptions
        red, ir = m.read_sequential() # get LEDs readings
        d = hrcalc.calc_hr_and_spo2(ir[:100], red[:100]) # give 100 values
        print('心率', d[0], '     血氧', d[2], '%')
        
        response_hr = d[0]
        response_spo2 = d[2]
        
        # Change Obj to String
        str_hr = str(response_hr)
        str_spo2 = str(response_spo2)
        
        # Delay Parsing Time
        time.sleep(0.01) 


# In[88]:


def stopParsing():
    global indicator
    indicator = 1


# In[89]:


def about():
    about_root=tk.Tk()
    
    w = 780 # width for the Tk root
    h = 480 # height for the Tk root

    # get screen width and height
    ws = about_root.winfo_screenwidth() # width of the screen
    hs = about_root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    about_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    about_root.title('About Holcombe Pulse')

    label_author=tk.Label(about_root,text='Holcombe Pulse Version 1.0', font=('tahoma', 24))
    label_author.place(x=200,y=60)

    label_author=tk.Label(about_root,text='Copyright (C) 2023', font=('tahoma', 24))
    label_author.place(x=225,y=120)
    
    label_author=tk.Label(about_root,text='Author: Chuan Yang', font=('tahoma', 24))
    label_author.place(x=225,y=180)
    
    label_author=tk.Label(about_root,text='Shengjing Hospital of China Medical University', font=('tahoma', 22))
    label_author.place(x=100,y=240)   

    button_refresh=tk.Button(about_root, width=15, text='OK', font=('tahoma', 24), command=about_root.destroy)
    button_refresh.place(x=230, y=330)

    about_root.mainloop()


# ### Thread Management

# In[90]:


def start_thread(event):
    global thread, indicator
    
    indicator = 0
    
    thread = threading.Thread(target=parsePulse)
    thread.daemon = True
    
    text_hr.delete('1.0', tk.END)
    text_hr.insert('1.0', str_hr)
    
    text_spo2.delete('1.0', tk.END)
    text_spo2.insert('1.0', str_spo2)
    
 
    thread.start()
    root.after(20, check_thread)

def check_thread():
    
    if thread.is_alive():
        
        text_hr.delete('1.0', tk.END)
        text_hr.insert('1.0', str_hr)
    
        text_spo2.delete('1.0', tk.END)
        text_spo2.insert('1.0', str_spo2)
    
        root.after(20, check_thread)    


# ### TKinter Mainflow

# In[91]:


root = tk.Tk()

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('Holcombe Pulse -- Pulse Diagnostics Parser')
#root.iconbitmap('dna.ico')

y0 = 150
y1 = 400
y2 = 580
y3 = 690

# Label & Edit Box

text_hr = tk.Text(root, width=5, height=1, font=('tahoma', 80), bd=2, wrap='none')
text_hr.place(x=280, y=y0)

label_hr = tk.Label(root, text='HR', font=('tahoma', 60))
label_hr.place(x=50,y=y0)

label_bpm = tk.Label(root, text='bpm', font=('tahoma', 60))
label_bpm.place(x=600,y=y0)


text_spo2 = tk.Text(root, width=5, height=1, font=('tahoma', 80), bd=2, wrap='none')
text_spo2.place(x=280, y=y1)

label_spo2 = tk.Label(root, text='SpO2', font=('tahoma', 60))
label_spo2.place(x=50,y=y1)

label_percentage = tk.Label(root, text='%', font=('tahoma', 60))
label_percentage.place(x=600,y=y1)

# Buttons

button_start = tk.Button(root, text="Start", width=12, font=('tahoma', 30), command=lambda:start_thread(None))
button_start.place(x=50, y=y3)

button_about = tk.Button(root, text="About...", width=12, font=('tahoma', 30), command=about)
button_about.place(x=400, y=y3)

button_exit = tk.Button(root, text="Exit", width=10, font=('tahoma', 30), command=root.destroy)
button_exit.place(x=745, y=y3)

root.bind('<Return>', start_thread)

root.mainloop()

