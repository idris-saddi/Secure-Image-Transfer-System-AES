# Secure Image Transfer System

## Introduction
The **Secure Image Transfer System** is designed to provide a robust solution for the secure transmission of images over networks. By leveraging the AES encryption algorithm, this system ensures that sensitive image data remains confidential and protected from unauthorized access during transfer.

## Project Intention and Scope

### Main Objective
The project aims to implement a secure image transfer system using the AES algorithm, thereby protecting sensitive data during transmission over networks.

### Specific Objectives
- **Encrypt images before transmission**: Use the AES algorithm to ensure data confidentiality during transmission.
- **Ensure image confidentiality during transfer**: Prevent interception or unauthorized access to images during their transfer.
- **Allow the recovery of original images upon receipt**: Ensure that the recipient can decrypt the images and restore them to their original state.

## Business Context

### Current Situation
With the proliferation of electronic devices in Tunisia, data security becomes crucial. This project emerges in the context of enhancing the confidentiality of exchanged images, thus addressing current security concerns.

## Stakeholders

### Internal
- **Development team**: Responsible for the design, development, and implementation of the system.
- **IT managers**: Guardians of the security and integration of the system within the existing infrastructure.

### External
- **End users**: People using the system for secure image transfer.
- **Regulatory authorities**: Entities responsible for approval and compliance with current regulations.

## Solution Concept

### Security Method
The AES (Advanced Encryption Standard) algorithm will be used to encrypt the images, ensuring a high level of security.

### Benefits
- **Secure transfer of confidential images**: Reduction of unauthorized disclosure risks.
- **Potential application in medical and military fields**: Possibility of using the system in sensitive sectors requiring enhanced security.

## Features
- **AES Encryption**: Implements the Advanced Encryption Standard to encrypt images before they are transmitted.
- **Confidentiality**: Maintains the confidentiality of images during the transfer process to prevent unauthorized interception.
- **Decryption**: Allows recipients to decrypt and restore images to their original state upon receipt.

## Use Cases
This system is particularly beneficial for:
- **Medical field**: Securely transmitting patient images and medical records.
- **Military field**: Ensuring confidential transmission of strategic and sensitive images.

## Installation

### Prerequisites
- Python
- FastAPI
- Uvicorn
- Pillow
- PyCryptodome

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/secure-image-transfer-system.git
    cd secure-image-transfer-system
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation at:
    ```
    http://127.0.0.1:8000/docs
    ```

## Usage

### Encrypt an Image
1. Send a POST request to `/encrypt` with a form containing the image file and password.
2. The encrypted image will be returned as a response.

### Decrypt an Image
1. Send a POST request to `/decrypt` with a form containing the encrypted image file and password.
2. The decrypted image will be returned as a binary response.

## Graphical Interface
The system includes a graphical interface built with Tkinter for easy interaction.

### Running the GUI
1. Run the GUI application:
    ```bash
    python gui.py
    ```

2. Use the GUI to encrypt and decrypt images by providing a password and selecting the image files.

## Conclusion
The **Secure Image Transfer System** is a critical tool for ensuring the secure transmission of images, protecting sensitive information, and maintaining confidentiality. Through the use of AES encryption, this system offers a reliable solution for various sectors requiring enhanced data security.
