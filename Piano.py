import tkinter as tk
import simpleaudio as sa
from pydub.generators import Sine

# Frequências das notas musicais
notas = {
    'A': 261.63,  # Dó
    'S': 293.66,  # Ré
    'D': 329.63,  # Mi
    'F': 349.23,  # Fá
    'G': 392.00,  # Sol
    'H': 440.00   # Lá
}

# Gerar e armazenar os sons das notas
def gerar_som(frequencia):
    return Sine(frequencia).to_audio_segment(duration=300).set_frame_rate(44100).raw_data

sons = {tecla: sa.WaveObject(gerar_som(freq), num_channels=1, bytes_per_sample=2, sample_rate=44100) for tecla, freq in notas.items()}

# Criar interface gráfica
root = tk.Tk()
root.title("Piano Simples")

# Criar teclas visuais
teclas = {}
for i, tecla in enumerate("ASDFGH"):
    btn = tk.Button(root, text=tecla, width=6, height=3, font=("Arial", 20), relief="raised", bg="white")
    btn.grid(row=0, column=i, padx=5, pady=10)
    teclas[tecla] = btn

# Função para tocar nota e mudar visual da tecla
def tocar_nota(event):
    tecla = event.char.upper()
    if tecla in notas:
        teclas[tecla].config(bg="lightblue")  # Mudar cor ao pressionar
        sons[tecla].play()

# Função para restaurar visual da tecla
def soltar_nota(event):
    tecla = event.char.upper()
    if tecla in notas:
        teclas[tecla].config(bg="white")  # Voltar à cor original

# Associar eventos às teclas
root.bind('<KeyPress>', tocar_nota)
root.bind('<KeyRelease>', soltar_nota)

# Rodar a interface
root.mainloop()
