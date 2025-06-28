import speech_recognition as sr
from flask import Flask, render_template, request, jsonify
import torch
from diffusers import StableDiffusionPipeline

app = Flask(__name__)

# Load the Stable Diffusion model
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", low_cpu_mem_usage=True).to(device)

def recognize_speech():
    """Converts speech to text using Google Speech Recognition"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_prompt = recognize_speech()
        print("Recognized Speech:", text_prompt)

        # Generate image from text
        image = pipe(text_prompt).images[0]
        image_path = "static/generated_image.png"
        image.save(image_path)

        return jsonify({"text": text_prompt, "image_path": image_path})
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
