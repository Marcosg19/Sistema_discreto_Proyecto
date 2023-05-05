import soundfile as sf
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

# Cargar señales de audio
x1, fs1 = sf.read('original.wav')
x2, fs2 = sf.read('filtromecanico.wav')

# Convertir señales de audio a tiempo discreto
fs = 44100 # Frecuencia de muestreo común
x1d = signal.resample(x1, int(len(x1)*fs/fs1))
x2d = signal.resample(x2, int(len(x2)*fs/fs2))

# Crear figura y subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8), sharex=True)

# Graficar señal de audio 1
ax1.plot(x1d)
ax1.set_xlabel('Muestras')
ax1.set_ylabel('Amplitud')
ax1.set_title('Audio Original')

# Graficar señal de audio 2
ax2.plot(x2d)
ax2.set_xlabel('Muestras')
ax2.set_ylabel('Amplitud')
ax2.set_title('Audio Filtro mecánico')

# Mostrar gráficos
plt.show()

# Asegurarse de que los audios tengan la misma longitud
min_len = min(len(x1d), len(x2d))
audio1 = x1d[:min_len]
audio2 = x2d[:min_len]

# Obtener la respuesta en frecuencia de los audios
freq1, response1 = signal.freqz(audio1, worN=2048)
freq2, response2 = signal.freqz(audio2, worN=2048)

# Calcular la función de transferencia
norm_response1 = response1 / np.max(np.abs(response1))
norm_response2 = response2 / np.max(np.abs(response2))
H = norm_response2[:len(norm_response1)] / norm_response1

# Obtener los coeficientes de la función de transferencia
zeros, poles, _ = signal.tf2zpk(np.real(H), np.imag(H))

# Crear un archivo txt y se guardan los coeficientes en el archivo
filename="CoeficientesH.txt"
with open(filename, 'w') as f:
    # Escribir una línea de encabezado
    f.write('Coeficientes Numerador: ')
    # Guardar los coeficientes en el archivo
    np.savetxt(f, abs(zeros),"%1.20e", newline=", ")

    # Escribir una línea de encabezado
    f.write('\n\nCoeficientes Denominador: ')
    # Guardar los coeficientes en el archivo
    np.savetxt(f, abs(poles),"%1.20e", newline=", ")

print('Coeficientes Numerador:', abs(zeros))
print('Coeficientes Denominador:', abs(poles))

zeros1 = abs(zeros)
poles1 = abs(poles)