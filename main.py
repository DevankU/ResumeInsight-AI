
from asciimatics.effects import Print
from asciimatics.renderers import Rainbow, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import time

# all of the above imports just for please wait

import os
from pdfminer.high_level import extract_text
from docx import Document
from PIL import Image
import pytesseract

import requests


import json

global extracted_text
extracted_text = ""

def animation(screen):
    effects = [
        Print(screen,
              Rainbow(screen, FigletText("Please Wait....", font='big')),
              y=screen.height//2 - 3,
              speed=1)
    ]
    
    
    end_time = time.time() + 5
    
    
    while time.time() < end_time:


        for effect in effects:
            effect.update(0)  
        screen.refresh()
        time.sleep(0.1)  
    
    screen.clear()

    screen.refresh()

Screen.wrapper(animation)




#bbelow part to take pdf or doc and give text



folder_path = r"your own folder path where you saved pdf/image/word file of resume."

def extract_text_from_pdf(pdf_path):

    return extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)

    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)

    return '\n'.join(fullText)

def extract_text_from_image(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'tessearact .exe path'
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':

        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
        return extract_text_from_image(file_path)
    else:

        raise ValueError("Unsupported file type. Please provide a .pdf, .docx , or image  file.")


def process_files_in_folder():
    global extracted_text 
    for file_name in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            try:
                extracted_text = extract_text_from_file(file_path)
            except Exception as e:

                print(f"Error extracting text from {file_name}: {e}")

if __name__ == "__main__":

    process_files_in_folder()




url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3-8b-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are an AI that summarizes resumes for recruiters. , you give answers in points form and in consise form , also you give only nessasary facts , and give your opinion on this candidate at the end. resume summary given by you should be consice."
        },
        {
            "role": "user",
            "content": extracted_text
        }
    ],
    "max_tokens": 0,
    "temperature": 0.2,
    "top_p": 0.9,
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer pplx-177eb4ce169ac55d32805ef3f95384-####lol did you really thought that i will share that:) (paste your own api key here.(both open -ai and perpelity api key  can be used here)(slight modification of the abovecode needed for open ai api ))"
}

response = requests.post(url, json=payload, headers=headers)

output_text = response.text




data = json.loads(output_text)


content = data['choices'][0]['message']['content']


content = content.replace('\\n', '\n')

print(content)
