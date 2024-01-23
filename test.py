import speech_recognition as sr
from pydub import AudioSegment


# Leer el texto
lines =[
  'I had a friend who always claimed to be a health guru.',
  'He preached about the benefits of clean eating and exercise.',
  'But he never followed his own advice.',
  'One day, he scoffed at me for choosing a salad over a burger.',
  'He said I was wasting my time.',
  'A few months later, he ended up in the hospital with heart problems.',
  "I couldn't help but say, 'I told you so.'",
  "It was the most satisfying 'I told you so' moment I've ever had."
]

recognizer = sr.Recognizer()


# Obtener los tiempos de inicio y fin de cada frase
for line in lines:
    print("IN THIS LINE: ", line)
    frase = line.strip()
    with sr.AudioFile('procesed.wav') as source:
        audio = recognizer.record(source)
        # Realizar la transcripción
        try:
            transcription = recognizer.recognize_google(audio, language='es-ES')
            
            print(transcription)
            
            start_time = transcription.index(frase)
            end_time = start_time + len(frase)
            print(f"Frase: {frase} - Tiempo inicio: {start_time} seg - Tiempo fin: {end_time} seg")
        except sr.UnknownValueError:
            print("No se pudo transcribir la frase")
        except ValueError:
            print(f"No se encontró la frase '{frase}' en la transcripción")