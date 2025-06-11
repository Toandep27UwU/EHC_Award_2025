from PIL import Image
import numpy as np
import wave

img = Image.open("albumcover.png").convert('L')
arr = np.array(img)

arr = (arr / 255.0) * 65535 - 32767
arr = arr.astype(np.int16)

with wave.open("flag.wav", 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(arr.tobytes())
