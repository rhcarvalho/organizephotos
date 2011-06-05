#!/usr/bin/env python
from Tkinter import *
import Image, ImageTk
import os

SOURCE = os.path.expanduser("~")
SOURCE = os.path.expanduser(raw_input("Read photos from [%s]: " % SOURCE)) or SOURCE


class Photo(object):
    def __init__(self, path):
        self.path = path
        self.visited = False
        self.share = None

    def __str__(self):
        return self.path
    
    def visit(self, share):
        self.visited = True
        self.share = share


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=N+S+E+W)
        self.createWidgets()
        self._photoIndex = 0
        self._photos = [Photo(os.path.join(root, f))
                            for root, dirs, files in os.walk(SOURCE)
                                for f in files
                                    if f.lower().endswith('.jpg')]
        print 'loaded %d photos from "%s"' % (len(self._photos), SOURCE)
        self.nextImage()

    def createWidgets(self):
        self.yesButton = Button(self, text='(Y)es',
            command=self.yes, background='#dfd')
        self.noButton = Button(self, text='(N)o',
            command=self.no, background='#fdd')
        self.detailsLabel = Label(text="...", padx=10, pady=10)
        self.imageLabel = Label()
        
        self.yesButton.grid(row=0, column=0, sticky=NW)
        self.noButton.grid(row=0, column=1, sticky=NW)
        self.imageLabel.grid(row=1, columnspan=3, sticky=N+S)
        self.detailsLabel.grid(row=0, column=2, sticky=NW)
        
        top = self.winfo_toplevel()
        top.bind('y', self.yes)
        top.bind('n', self.no)
        top.bind('<Escape>', lambda _: self.quit())
        
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0)
        self.columnconfigure(1)
        self.columnconfigure(2, weight=1)
        
        
    def yes(self, event=None):
        #print 'yes', event
        self.currentPhoto.visit(True)
        self.nextImage()
        
    def no(self, event=None):
        #print 'no', event
        self.currentPhoto.visit(False)
        self.nextImage()
        
    def nextImage(self):
        self.currentPhoto = self._photos[self._photoIndex]
        #print 'source:', self.currentPhoto
        image = Image.open(self.currentPhoto.path)
        image.thumbnail((1000, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self._photoIndex = (self._photoIndex + 1) % len(self._photos)
        self.imageLabel.configure(image=self.image)
        self.detailsLabel.configure(text=self.currentPhoto.path)
        

app = Application()
app.master.title("Choose photos to share with mom")
try:
    app.mainloop()
finally:
    to_share = [photo.path for photo in app._photos if photo.share]
    if to_share:
        print 'Share these photos:'
        print '\n'.join(to_share)

