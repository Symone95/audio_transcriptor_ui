import whisper
from tqdm import tqdm
from pydub import AudioSegment
import math
import os

# Carico modello
model = whisper.load_model("small")  # puoi provare "base", "medium", "large"

# Percorso file originale
file_path = "/Users/simone/Downloads/diritto 2.m4a"

# Percorso file di output
output_path = "trascrizione.txt"

# Carico l'audio con pydub
audio = AudioSegment.from_file(file_path, format="m4a")

# Parametri chunk
chunk_size_ms = 60 * 1000  # 60 secondi
num_chunks = math.ceil(len(audio) / chunk_size_ms)

# Se esiste un vecchio file, lo cancello
if os.path.exists(output_path):
    os.remove(output_path)

print(f"Trascrizione in corso... scrittura su '{output_path}'")

# Processa ogni chunk
for i in tqdm(range(num_chunks), desc="Trascrizione"):
    start = i * chunk_size_ms
    end = min((i + 1) * chunk_size_ms, len(audio))

    # Estraggo il pezzo
    chunk = audio[start:end]
    chunk_path = f"chunk_{i}.wav"
    chunk.export(chunk_path, format="wav")

    # Trascrivo
    result = model.transcribe(chunk_path, language="it")
    text = result["text"].strip()

    # Scrivo subito su file
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(text + " ")

    # Pulizia file temporaneo
    os.remove(chunk_path)

print("\n--- TRASCRIZIONE COMPLETA ---")
print(f"Testo salvato in '{output_path}'")
