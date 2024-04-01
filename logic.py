#!/usr/bin/env python
# ----------------- Header Files ---------------------#

from __future__ import division, print_function, unicode_literals

from PIL import Image
from Crypto.Cipher import AES
import binascii
import numpy as np
from os.path import join as path_join
from os import makedirs
from os.path import exists

global password 

# ----------------- Create Folders ---------------------#

files_folder_path = "files/"
if not exists(files_folder_path):
    makedirs(files_folder_path)
cipher_folder_path = "cipher_files/"
if not exists(cipher_folder_path):
    makedirs(cipher_folder_path)

# ----------------- Utility Functions ---------------------#

def load_image(name):
    return Image.open(name)

# ----------------- Functions for encryption ---------------------#

def prepare_message_image(image, size):
    if size != image.size:
        image = image.resize(size, Image.ANTIALIAS)
    return image

def generate_secret(size, secret_image = None):
    width, height = size
    new_secret_image = Image.new(mode = "RGB", size = (width * 2, height * 2))

    for x in range(0, 2 * width, 2):
        for y in range(0, 2 * height, 2):
            color1 = np.random.randint(255)
            color2 = np.random.randint(255)
            color3 = np.random.randint(255)
            new_secret_image.putpixel((x,  y),   (color1,color2,color3))
            new_secret_image.putpixel((x+1,y),   (255-color1,255-color2,255-color3))
            new_secret_image.putpixel((x,  y+1), (255-color1,255-color2,255-color3))
            new_secret_image.putpixel((x+1,y+1), (color1,color2,color3))
                
    return new_secret_image

def generate_ciphered_image(secret_image, prepared_image):
    width, height = prepared_image.size
    ciphered_image = Image.new(mode = "RGB", size = (width * 2, height * 2))
    for x in range(0, width*2, 2):
        for y in range(0, height*2, 2):
            sec = secret_image.getpixel((x,y))
            msssg = prepared_image.getpixel((int(x/2),int(y/2)))
            color1 = (msssg[0]+sec[0])%256
            color2 = (msssg[1]+sec[1])%256
            color3 = (msssg[2]+sec[2])%256
            ciphered_image.putpixel((x,  y),   (color1,color2,color3))
            ciphered_image.putpixel((x+1,y),   (255-color1,255-color2,255-color3))
            ciphered_image.putpixel((x,  y+1), (255-color1,255-color2,255-color3))
            ciphered_image.putpixel((x+1,y+1), (color1,color2,color3))
                
    return ciphered_image

def generate_image_back(secret_image, ciphered_image):
    width, height = secret_image.size
    new_image = Image.new(mode = "RGB", size = (int(width / 2), int(height / 2)))
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            sec = secret_image.getpixel((x,y))
            cip = ciphered_image.getpixel((x,y))
            color1 = (cip[0]-sec[0])%256
            color2 = (cip[1]-sec[1])%256
            color3 = (cip[2]-sec[2])%256
            new_image.putpixel((int(x/2),  int(y/2)),   (color1,color2,color3))
               
    return new_image

#------------------------Encryption -------------------#

def level_one_encrypt(Imagename):
    message_image = load_image(Imagename)
    size = message_image.size

    secret_image = generate_secret(size)
    secret_image.save(path_join(files_folder_path, "secret.jpeg"))

    prepared_image = prepare_message_image(message_image, size)
    ciphered_image = generate_ciphered_image(secret_image, prepared_image)
    ciphered_image.save(path_join(files_folder_path, "2-share_encrypt.jpeg"))

# -------------------- Construct Encrypted Image  ----------------#

def construct_enc_image(ciphertext,relength,width,height):
    asciicipher = binascii.hexlify(ciphertext).decode()
    def replace_all(text, dic):
        res = text
        for i, j in dic.items():
            res = res.replace(i, j)
        return res

    # use replace function to replace ascii cipher characters with numbers
    reps = {'a':'1', 'b':'2', 'c':'3', 'd':'4', 'e':'5', 'f':'6', 'g':'7', 'h':'8', 'i':'9', 'j':'10', 'k':'11', 'l':'12', 'm':'13', 'n':'14', 'o':'15', 'p':'16', 'q':'17', 'r':'18', 's':'19', 't':'20', 'u':'21', 'v':'22', 'w':'23', 'x':'24', 'y':'25', 'z':'26'}
    asciiciphertxt = replace_all(asciicipher, reps)

    # construct encrypted image
    step = 3
    encimageone=[asciiciphertxt[i:i+step] for i in range(0, len(asciiciphertxt), step)]
    # if the last pixel RGB value is less than 3-digits, add a digit a 1
    if int(encimageone[len(encimageone)-1]) < 100:
        encimageone[len(encimageone)-1] += "1"
    # check to see if we can divide the string into partitions of 3 digits.  if not, fill in with some garbage RGB values
    if len(encimageone) % 3 != 0:
        while (len(encimageone) % 3 != 0):
            encimageone.append("101")

    encimagetwo=[(int(encimageone[int(i)]),int(encimageone[int(i+1)]),int(encimageone[int(i+2)])) for i in range(0, len(encimageone), step)]

    while (int(relength) != len(encimagetwo)):
        encimagetwo.pop()

    encim = Image.new("RGB", (int(width),int(height)))
    encim.putdata(encimagetwo)

    encim.save(path_join(files_folder_path, "visual_encrypt.jpeg"))

#------------------------- Visual-encryption -------------------------#

def encrypt(imagename,password):
    plaintext = list()
    plaintextstr = ""

    im = Image.open(imagename) 
    pix = im.load()

    width , height = im.size
    
    # break up the image into a list, each with pixel values and then append to a string
    for y in range(0,height):
        for x in range(0,width):
            plaintext.append(pix[x,y])

    # add 100 to each tuple value to make sure each are 3 digits long. 
    for i in range(0,len(plaintext)):
        for j in range(0,3):
            aa = int(plaintext[i][j])+100
            plaintextstr = plaintextstr + str(aa)

    # length save for encrypted image reconstruction
    relength = len(plaintext)

    # append dimensions of image for reconstruction after decryption
    plaintextstr += "h" + str(height) + "h" + "w" + str(width) + "w"

    # make sure that plantextstr length is a multiple of 16 for AES.  if not, append "n". 
    while (len(plaintextstr) % 16 != 0):
        plaintextstr = plaintextstr + "n"

    # encrypt plaintext
    obj = AES.new(bytes(password), AES.MODE_CBC, b'This is an IV456')
    ciphertext = obj.encrypt(plaintextstr.encode())

    # write ciphertext to file for analysis
    cipher_name = path_join(cipher_folder_path, imagename.split("/")[-1] + ".crypt")
    g = open(cipher_name, 'wb')
    g.write(ciphertext)
    construct_enc_image(ciphertext,relength,width,height)
    print("Visual Encryption done.......")
    level_one_encrypt(path_join(files_folder_path,"visual_encrypt.jpeg"))
    print("2-Share Encryption done.......")
    return cipher_name

# ---------------------- decryption ---------------------- #

def decrypt(ciphername,password):

    secret_image = Image.open(path_join(files_folder_path, "secret.jpeg"))
    ima = Image.open(path_join(files_folder_path, "2-share_encrypt.jpeg"))
    new_image = generate_image_back(secret_image, ima)
    new_image.save(path_join(files_folder_path, "2-share_decrypt.jpeg"))
    print("2-share Decryption done....")
    cipher = open(ciphername,'rb')
    ciphertext = cipher.read()

    # decrypt ciphertext with password
    obj2 = AES.new(bytes(password), AES.MODE_CBC, b'This is an IV456')
    try:
        decrypted_bytes = obj2.decrypt(ciphertext)
    except Exception as e:
        print("Decryption failed:", e)

    # remove padding
    decrypted_bytes = decrypted_bytes.rstrip(b'n')

    # convert bytes to string
    decrypted = decrypted_bytes.decode()

    # parse the decrypted text back into integer string
    decrypted = decrypted.replace("n","")

    # extract dimensions of images
    newwidth = decrypted.split("w")[1]
    newheight = decrypted.split("h")[1]

    # replace height and width with emptyspace in decrypted plaintext
    heightr = "h" + str(newheight) + "h"
    widthr = "w" + str(newwidth) + "w"
    decrypted = decrypted.replace(heightr,"")
    decrypted = decrypted.replace(widthr,"")

    # reconstruct the list of RGB tuples from the decrypted plaintext
    step = 3
    finaltextone=[decrypted[i:i+step] for i in range(0, len(decrypted), step)]
    finaltexttwo=[(int(finaltextone[int(i)])-100,int(finaltextone[int(i+1)])-100,int(finaltextone[int(i+2)])-100) for i in range(0, len(finaltextone), step)]

    # reconstruct image from list of pixel RGB tuples
    newim = Image.new("RGB", (int(newwidth), int(newheight)))
    newim.putdata(finaltexttwo)
    outputfilename = path_join(files_folder_path, "visual_decrypt.jpeg")
    newim.save(outputfilename)
    print("Visual Decryption done......")
    return outputfilename
