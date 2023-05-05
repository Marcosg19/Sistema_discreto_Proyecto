import scipy.signal as signal
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import proyecto2

# Cargar señales de audio
x1, fs1 = sf.read('original.wav')
x2, fs2 = sf.read('filtromecanico.wav')

# Convertir señales de audio a tiempo discreto
fs = 44100 # Frecuencia de muestreo común
x1d = signal.resample(x1, int(len(x1)*fs/fs1))
x2d = signal.resample(x2, int(len(x2)*fs/fs2))

# Asegurarse de que los audios tengan la misma longitud
min_len = min(len(x1d), len(x2d))
audio1 = x1d[:min_len]
audio2 = x2d[:min_len]

# Definir los coeficientes del numerador y denominador de la función de transferencia
b = np.array(proyecto2.zeros1)
a = np.array(proyecto2.poles1)


factor=1.5
b1=b*factor
a1=a

# Aplicar el filtro
y = signal.lfilter(b1, a1, audio1)

# Crear un filtro de paso bajo
fc = 2000 # Frecuencia de corte del filtro
order = 1 # Orden del filtro
w, z = signal.butter(order, fc/(fs1/1.5))

y3 = signal.lfilter(w, z, y)

# Guardar la señal de salida filtrada en un archivo de audio
y2 = signal.resample(y3, int(len(y3)*fs/fs1))
sf.write('audio_filtrodigital.wav', y3, fs)

# Graficar la señal de entrada y la señal de salida
plt.plot(x2d, label='Filtro mecánico')
plt.plot(y2, label='Filtro digital')
plt.legend()
plt.show()
