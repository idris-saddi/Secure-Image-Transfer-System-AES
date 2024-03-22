from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from logic import encrypt, decrypt

app = FastAPI()

@app.post("/encrypt/")
async def encrypt_image(password: str, file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    with open("temp_image.jpg", "wb") as temp_image:
        temp_image.write(file.file.read())
    
    # Encrypt the image
    encrypt("temp_image.jpg", password)

    # Return the encrypted image
    return FileResponse("2-share_encrypt.jpeg")

@app.post("/decrypt/")
async def decrypt_image(password: str, file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    with open("temp_encrypted_image.crypt", "wb") as temp_encrypted_image:
        temp_encrypted_image.write(file.file.read())
    
    # Decrypt the image
    decrypt("temp_encrypted_image.crypt", password)

    # Return the decrypted image
    return FileResponse("visual_decrypt.jpeg")
