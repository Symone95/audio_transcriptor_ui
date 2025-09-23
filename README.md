# 🎙️ Trascrittore Audio con Whisper + Kivy

Un'applicazione desktop scritta in **Python** che permette di selezionare un file audio, trascriverlo in testo tramite il modello [OpenAI Whisper](https://github.com/openai/whisper) e visualizzare i progressi in tempo reale con una **GUI sviluppata in Kivy**.  
Supporta vari formati audio (`.mp3`, `.wav`, `.m4a`, `.mp4`, `.flac`).

---

## ✨ Funzionalità

- Interfaccia grafica semplice con **Kivy**  
- Scelta del file audio tramite `FileChooser`  
- Trascrizione progressiva con **barra di avanzamento**  
- Visualizzazione del testo trascritto in tempo reale  
- Salvataggio automatico in `trascrizione.txt`  
- Pulsante **Stop** per interrompere la trascrizione  
- Possibilità di selezionare e trascrivere più file senza riavviare l’app

---

## 🛠️ Requisiti

- **Python 3.8+**  
- Librerie necessarie:  

```bash
pip install kivy pydub openai-whisper
```

## 🛠️ Buildare il progetto
Per buildare da zero il progetto lanciare il seguente script Python, creerà le cartelle `/build` e `/dist` e il file `.spec` nella root
```bash
python build.py
```

## 🛠️ Compilare il progetto manualmente
Per ricompilare il progetto lanciare il comando seguente, aggiornerà l'eseguibile sotto la cartella `./dist`
```bash
pyinstaller Audio_Transcriptor.spec
```