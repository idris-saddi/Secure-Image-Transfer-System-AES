#!/usr/bin/env python
import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from logic import encrypt, decrypt
from io import BytesIO

app = FastAPI()

@app.post("/encrypt")
async def encrypt_image(request: Request):
    data = await request.form()
    password = (data.get('password', '') + '\0' * 16)[:16].encode('utf-8')
    
    # Get the uploaded file name
    filename = data['file'].filename

    try:
        # Encrypt the file
        encrypted_data = encrypt(filename, password)

        # Return the encrypted file
        return {"cipher_file": encrypted_data}
    except Exception as e:
        return {"error": str(e)}  # Handle any exceptions and return an error message


@app.post("/decrypt")
async def decrypt_image(request: Request):
    data = await request.form()
    password = (data.get('password', '') + '\0' * 16)[:16].encode('utf-8')

    # Get the uploaded file name
    filename = data.get('file', '')
    if not filename:
        return {"error": "No file uploaded"}

    # Construct the full path to the file
    cipherfilename = os.path.join('cipher_files', filename)

    # Decrypt the file
    try:
        decrypted_data = decrypt(cipherfilename, password)
    except Exception as e:
        return {"error": str(e)}

    # Open the decrypted image file
    with open(decrypted_data, 'rb') as image_file:
        image_data = image_file.read()

    # Return the decrypted image as a binary response
    return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")