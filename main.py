import threading
import math
import os
import sys
from pydub import AudioSegment
import whisper

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView

# Imposto dimensioni base finestra
Window.size = (800, 600)

if sys.platform == "darwin":
    Window.set_icon("icons/logo.icns")
elif sys.platform.startswith("win"):
    Window.set_icon("icons/logo.ico")
else:
    Window.set_icon("icons/logo.png")

# Carico modello Whisper una sola volta
model = whisper.load_model("small")  # puoi provare "base", "medium", "large"


class Trascrittore(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.file_path = None
        self.stop_flag = False  # variabile per fermare la trascrizione

        self.label = Label(text="Seleziona un file audio", size_hint=(1, 0.1))
        self.add_widget(self.label)

        # File chooser
        self.download_folder = os.path.join(os.path.expanduser("~"), "Desktop")
        self.file_chooser = FileChooserIconView(
            size_hint=(1, 0.6),
            path=self.download_folder,
            filters=["*.mp3", "*.mp4", "*.wav", "*.m4a", "*.flac"]
        )
        self.add_widget(self.file_chooser)

        # Contenitore per bottoni
        btn_box = BoxLayout(size_hint=(1, 0.1), spacing=10)

        # Bottone avvio
        self.btn_start = Button(text="Avvia Trascrizione")
        self.btn_start.bind(on_press=self.start_transcription)
        btn_box.add_widget(self.btn_start)

        # Bottone stop
        self.btn_stop = Button(text="Interrompi", disabled=True)
        self.btn_stop.bind(on_press=self.stop_transcription)
        btn_box.add_widget(self.btn_stop)

        self.add_widget(btn_box)

        # Progress bar (inizialmente nascosta)
        self.progress = ProgressBar(max=100, value=0, size_hint=(1, 0.05))
        self.progress.opacity = 0
        self.add_widget(self.progress)

        # Area testo (inizialmente nascosta)
        self.text_area = TextInput(readonly=True, size_hint=(1, 0.25))
        self.text_area.opacity = 0
        self.add_widget(self.text_area)

    def start_transcription(self, instance):
        selection = self.file_chooser.selection
        if not selection:
            self.label.text = "⚠️ Nessun file selezionato!"
            return

        self.file_path = selection[0]
        self.stop_flag = False  # reset

        # Nascondo il file chooser
        if self.file_chooser.parent:
            self.remove_widget(self.file_chooser)

        self.label.text = f"Trascrizione in corso di:\n{os.path.basename(self.file_path)}"
        self.text_area.text = ""
        self.progress.value = 0
        self.btn_start.disabled = True
        self.btn_stop.disabled = False

        # Rendo visibili progress bar e area testo
        self.progress.opacity = 1
        self.text_area.opacity = 1

        # Avvia trascrizione in thread separato
        threading.Thread(target=self.transcribe_file).start()

    def stop_transcription(self, instance):
        self.stop_flag = True
        self.label.text = "⏹ Interruzione richiesta..."

    def transcribe_file(self):
        audio = AudioSegment.from_file(self.file_path)

        # Suddivisione in chunk
        chunk_size_ms = 60 * 1000  # 60 secondi
        num_chunks = math.ceil(len(audio) / chunk_size_ms)

        output_path = "trascrizione.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for i in range(num_chunks):
                if self.stop_flag:  # fermo subito
                    break

                start = i * chunk_size_ms
                end = min((i + 1) * chunk_size_ms, len(audio))

                chunk = audio[start:end]
                chunk_path = f"chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")

                result = model.transcribe(chunk_path, language="it", fp16=False)
                testo = result["text"].strip() + " "

                # Aggiorna GUI in modo thread-safe
                Clock.schedule_once(lambda dt, t=testo: self.update_text(t))
                Clock.schedule_once(lambda dt, v=(i + 1) / num_chunks * 100: self.update_progress(v))

                f.write(testo)
                os.remove(chunk_path)

        Clock.schedule_once(lambda dt: self.finish_transcription())

    def update_text(self, testo):
        self.text_area.text += testo + " "
        self.text_area.cursor = (0, len(self.text_area.text))

    def update_progress(self, value):
        self.progress.value = value

    def finish_transcription(self):
        if self.stop_flag:
            self.label.text = "❌ Trascrizione interrotta."
        else:
            self.label.text = "✅ Trascrizione completata!"

        self.btn_start.disabled = False
        self.btn_stop.disabled = True
        self.btn_start.text = "Avvia Trascrizione"

        # Ripristino file chooser
        if not self.file_chooser.parent:
            self.add_widget(self.file_chooser, index=1)
            self.file_chooser.path = self.download_folder
            self.file_chooser.selection = []

        # Reset percorso file
        self.file_path = None


class TrascrittoreApp(App):
    def build(self):
        return Trascrittore()


if __name__ == "__main__":
    TrascrittoreApp().run()
