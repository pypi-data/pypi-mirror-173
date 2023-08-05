#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:51:19 2021

@author: gurpreet
"""
import tkinter as tk
import numpy as np

window = tk.Tk()
window.title("parallax to luminosity converter")
window.geometry("700x600")
# distance=1000/parallax                        # in pc
# distanceerr=distance*parallaxerr/parallax       #in pc
# distance=distance*3.086e18                         #in cm
# distanceerr=distanceerr*3.086e18                   #in cm
def lummaker(Parallax,Parralaxerrerr,Flux,Fluxerr):
    distance=1000/Parallax
    distanceerr=distance*Parralaxerrerr/Parallax
    distance=distance*3.086e18                         #in cm
    distanceerr=distanceerr*3.086e18
    luminosity=4*np.pi*distance**2*Flux
    luminosityerr=luminosity*(np.sqrt((Fluxerr/Flux)**2 + (2*distanceerr/distance)**2))
    return luminosity,luminosityerr
# print(lummaker(distance, distanceerr, flux, fluxerr))


def infos():
    p=float(para.get())
    pe=float(paraerr.get())
    f=float(flux.get())
    fe=float(fluxerr.get())
    L,Le=lummaker(p,pe,f, fe)
    ax=tk.Label(window,text=("Luminosity:",L),font=("Arial",20))
    ax.place(x="50",y="400")
    # print(L,Le)
    ax1=tk.Label(window,text=("Error:",Le),font=("Arial",20))
    ax1.place(x="50",y="450")    
    
plabel=tk.Label(window,text="Parallax:",font=("Arial",18)) 
plabel.place(x="10",y="10")
    
pelabel=tk.Label(window,text="Parallax Error:",font=("Arial",18)) 
pelabel.place(x="10",y="50")

flabel=tk.Label(window,text="Flux:",font=("Arial",18)) 
flabel.place(x="10",y="100")

felabel=tk.Label(window,text="Flux Error:",font=("Arial",18)) 
felabel.place(x="10",y="150")

para=tk.StringVar()
pentry=tk.Entry(window,text=para,font=("Arial",18))
pentry.place(x="200",y="10")

paraerr=tk.StringVar()
perrentry=tk.Entry(window,text=paraerr,font=("Arial",18))
perrentry.place(x="200",y="50")

flux=tk.StringVar()
fentry=tk.Entry(window,text=flux,font=("Arial",18))
fentry.place(x="200",y="100")

fluxerr=tk.StringVar()
ferrentry=tk.Entry(window,text=fluxerr,font=("Arial",18))
ferrentry.place(x="200",y="150")


inform=tk.Label(window,text="* Enter Parallax in 'mas' and Flux in 'cgs' units",font=("Arial",18))
inform.place(x="10",y="220")
clicked=tk.Button(window,text="Calculate",font=("Arial",18),command=infos)
clicked.place(x="100",y="300")
window.mainloop()
