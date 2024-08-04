import pdfplumber
from pathlib import Path
import openai
import re
import os
from pydub import AudioSegment
from moviepy.editor import concatenate_audioclips, AudioFileClip
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY")

"""First extract all texts from PDF"""
def extract_text_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pdf_content = ""
        for page in pdf.pages:
            texts = page.extract_text()
            if texts:
                markdown_page = texts.replace('\n', '\n\n')
                pdf_content += markdown_page + '\n\n---\n\n'
        return pdf_content
    
pdf_path = 'Gulliver’s_Travel.pdf' 
total_words = extract_text_pdf(pdf_path)
print(total_words)
print("Whole texts extract complete")


# Now we convert the resultant words to plain text
def convert_to_plain_text(total_words):
    # Remove Markdown URL syntax ([text](link)) and keep only the text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', total_words)

    # Remove Markdown formatting for bold and italic text
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold with **
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic with *
    text = re.sub(r'\_\_([^_]+)\_\_', r'\1', text)  # Bold with __
    text = re.sub(r'\_([^_]+)\_', r'\1', text)      # Italic with _

    # Remove Markdown headers, list items, and blockquote symbols
    text = re.sub(r'#+\s?', '', text)  # Headers
    text = re.sub(r'-\s?', '', text)   # List items
    text = re.sub(r'>\s?', '', text)   # Blockquotes

    return text

plain_text = convert_to_plain_text(total_words)
# print(plain_text)  # Printing the converted plain text

# Needed further cleaning the data (todo: method to extract all unwanted data and pass them below)
plain_text = plain_text.replace("① magician：魔术师", "")
# Printing the cleaned text to verify the changes
print(plain_text)

# Following method converts the resultant texts to chunks of data
def split_text_to_chunks(text, max_chunk_size = 999):
    chunks = []
    current_chunk =""
    # Split the text into sentences and iterate through them
    for sentence in text.split('.'):
        sentence = sentence.strip()  # Remove leading/trailing whitespaces
        if not sentence:
            continue  # Skip empty sentences

        # Check if adding the sentence would exceed the max chunk size
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += sentence + "."  # Add sentence to current chunk
        else:
            chunks.append(current_chunk)  # Add the current chunk to the list
            current_chunk = sentence + "."  # Start a new chunk

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
# Function Usage
chunks = split_text_to_chunks(plain_text)

# Printing each chunk with its number
for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}:\n{chunk}\n---\n")

# Text-to-Speech Conversion
def text_to_speech(input_text, output_file, model = "tts-1", voice = "nova"):
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text
    )
    audio_file_path = Path(output_file)
    response.stream_to_file(audio_file_path)
    print(f"Audio is saved to {audio_file_path}")

# convert text chunks to audio files and save them
def text_chunks_to_audio(chunks, output_folder):
    audio_files = []  # store paths of generated audio

    for i,chunk in enumerate(chunks):
        output_audio_file = os.path.join(output_folder, f"chunk_{i+1}.mp3")
        text_to_speech(chunk, output_audio_file)
        audio_files.append(output_audio_file)

    return audio_files
output_folder = "audio_chunks"  
audio_files = text_chunks_to_audio(chunks, output_folder)  
print(audio_files) 

# # Next combine multiple audio files to a single file
# def convert_audio_chunks_single_file():
#     audio_clips = []
#     # Iterate through each file in the given folder
#     for file_name in sorted(os.listdir(folder_path)):
#         if file_name.endswith('.mp3'):
#             file_path = os.path.join(folder_path, file_name)
#             print(f"Processing file: {file_path}")

#             try:
#                 # Create an AudioFileClip object for each audio file
#                 clip = AudioFileClip(file_path)
#                 audio_clips.append(clip)  # Add the clip to the list
#             except Exception as e:
#                 # Print any errors encountered while processing the file
#                 print(f"Error processing file {file_path}: {e}")

#     if audio_clips:
#         final_clip = concatenate_audioclips(audio_clips)
#         final_clip.write_audiofile(output_file)
#         print(f"Combined audio saved to {output_file}")
#     else:
#         print("No audio clips to combine.")

# convert_audio_chunks_single_file('chunks', 'combined_audio.mp3')  # Combine audio files in 'chunks' folder
