import wave
import struct
import math
import os

def generar_sonido(filename, frecuencia, duracion, tipo="seno"):
    sample_rate = 44100
    num_samples = int(sample_rate * duracion)

    with wave.open(filename, 'w') as obj:
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate
            if tipo == "seno":
                value = int(32767 * math.sin(2 * math.pi * frecuencia * t))
            elif tipo == "cuadrado":
                value = 32767 if math.sin(2 * math.pi * frecuencia * t) > 0 else -32767
            elif tipo == "beep":
                valor_base = math.sin(2 * math.pi * frecuencia * t)
                valor_env = max(0, 1 - (t / duracion))
                value = int(32767 * valor_base * valor_env)
            data = struct.pack('<h', value)
            obj.writeframesraw(data)

os.makedirs("sonidos", exist_ok=True)

print("Generando sonidos...")
generar_sonido("sonidos/descarga.wav", 440, 0.5, "beep")
generar_sonido("sonidos/terminado.wav", 880, 0.3, "beep")
print("Listo!")