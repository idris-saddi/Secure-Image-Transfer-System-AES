#!/usr/bin/env python
from logic import encrypt, decrypt

from tkinter import *
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import hashlib
import os

# message box alerts
def pass_alert():
   tkMessageBox.showinfo("Password Alert","Please enter a password.")

def enc_success(imagename):
   tkMessageBox.showinfo("Success","Encrypted Image: " + imagename)

def dec_success(outputfilename):
    tkMessageBox.showinfo("Success","Decrypted Image: " + outputfilename)

# image encrypt button event
def image_open():
    global file_path_e

    enc_pass = passg.get()
    if enc_pass == "":
        pass_alert()
    else:
        password = hashlib.sha256(enc_pass.encode()).digest()
        filename = tkFileDialog.askopenfilename()
        file_path_e = os.path.dirname(filename)
        encrypt(filename,password)
        enc_success(filename)

# image decrypt button event
def cipher_open():
    global file_path_d

    dec_pass = passg.get()
    if dec_pass == "":
        pass_alert()
    else:
        password = hashlib.sha256(dec_pass.encode()).digest()
        filename = tkFileDialog.askopenfilename()
        file_path_d = os.path.dirname(filename)
        outputfilename = decrypt(filename,password)
        dec_success(outputfilename)

class App:
  def __init__(self, master):
    global passg
    title = "Image Encryption"
    author = "Made by Idris SADDI"
    msgtitle = Message(master, text =title)
    msgtitle.config(font=('helvetica', 17, 'bold'), width=200)
    msgauthor = Message(master, text=author)
    msgauthor.config(font=('helvetica',10), width=200)

    canvas_width = 200
    canvas_height = 50
    w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
    msgtitle.pack()
    msgauthor.pack()
    w.pack()

    passlabel = Label(master, text="Enter Encrypt/Decrypt Password:")
    passlabel.pack()
    passg = Entry(master, show="*", width=20)
    passg.pack()

    self.encrypt = Button(master,
                         text="Encrypt", fg="black",
                         command=image_open, width=25,height=5)
    self.encrypt.pack(side=LEFT)
    self.decrypt = Button(master,
                         text="Decrypt", fg="black",
                         command=cipher_open, width=25,height=5)
    self.decrypt.pack(side=RIGHT)


# ------------------ MAIN -------------#
root = Tk()
root.wm_title("Image Encryption")
app = App(root)
root.mainloop()