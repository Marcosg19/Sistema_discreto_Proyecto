import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
import time
import filtrodigital2

# Cargar señales de audio
audio1, fs1 = sf.read('audio_filtrodigital.wav')
audio2, fs2 = sf.read('filtromecanico.wav')
audio3, fs3 = sf.read('original.wav')

# Asegurarse de que las señales tengan la misma duración
min_len = min(len(audio1), len(audio2))
audio1 = audio1[:min_len]
audio2 = audio2[:min_len]

# Normalizar las señales
audio1 = audio1 / np.max(np.abs(audio1))
audio2 = audio2 / np.max(np.abs(audio2))

# Calcular la correlación cruzada
corr = np.correlate(audio1, audio2, mode='same')

# Normalizar la correlación cruzada
corr = corr / np.max(np.abs(corr))

# Crear figura y subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8), sharex=True)

# Graficar señal de audio 1
ax1.plot(audio1)
ax1.set_xlabel('Muestras')
ax1.set_ylabel('Amplitud')
ax1.set_title('Filtro digital')

# Graficar señal de audio 2
ax2.plot(audio2)
ax2.set_xlabel('Muestras')
ax2.set_ylabel('Amplitud')
ax2.set_title('Filtro mecánico')

# Mostrar gráficos
plt.show()

# Crear figura y subplot
fig, ax = plt.subplots(1, 1, figsize=(10,5))

# Graficar la correlación cruzada
ax.plot(corr)
ax.set_xlabel('Retraso (muestras)')
ax.set_ylabel('Correlación cruzada')
ax.set_title('Correlación cruzada entre filtro digital y filtro mecánico')

# Mostrar gráfico
plt.show()

# Normalizar la correlación cruzada
#norm_corr = corr / (np.linalg.norm(audio1) * np.linalg.norm(audio2))

# Obtener el valor máximo y promedio de la correlación cruzada normalizada
max_corr = np.amax(corr)
avg_corr = np.mean(corr)

# Calcular el valor de similitud
similarity = np.dot(audio1, audio2) / (np.linalg.norm(audio1) * np.linalg.norm(audio2))

print("Valor máximo de la correlación cruzada normalizada:", max_corr)
print("Valor de similitud entre las dos señales:", similarity)

diff = np.sqrt(np.mean((audio1 - audio2)**2))
print('Diferencia RMS:', diff)
time.sleep(2)

# Reproducción de audio original
sd.play(audio3, fs3)
sd.wait()
time.sleep(2)

# Reproducción de filtro mecanico
sd.play(audio2, fs1)
sd.wait()
time.sleep(2)


# Reproducción de filtro digital
sd.play(audio1, fs2)
sd.wait()