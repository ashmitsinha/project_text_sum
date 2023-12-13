import requests
from django.shortcuts import render
from django.http import HttpResponse
import pyttsx3
from googletrans import Translator

# class IndexView(View):
#     template_name = "index.html"

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
#         api_token = "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"
#         headers = {"Authorization": f"Bearer {api_token}"}

#         data = request.POST.get("data")
#         max_length = int(request.POST.get("maxL"))
#         min_length = max_length // 4

#         def query(payload):
#             response = requests.post(api_url, headers=headers, json=payload)
#             return response.json()

#         output = query({
#             "inputs": data,
#             "parameters": {"min_length": min_length, "max_length": max_length},
#         })[0]

#         return render(request, self.template_name, {"result": output["summary_text"]})


def index(request):
    return render(request,'index.html')


text = ''

def output(request):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    api_token = "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"
    headers = {"Authorization": f"Bearer {api_token}"}

    data = request.POST.get("data")
    max_length = int(request.POST.get("maxL"))
    min_length = max_length // 4

    def query(payload):
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": data,
        "parameters": {"min_length": min_length, "max_length": max_length},
        })[0]
    print(len(output["summary_text"]))
    #return HttpResponse(f'<h1>{output["summary_text"]}</h1>')
    text = output["summary_text"]
    request.session['text_for_speech'] = text
  
    return render(request, 'output.html', {"result": output["summary_text"]})

def texttospeech(request):
    rate=500
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    text = request.session.get('text_for_speech', '')
        # Use the engine to speak the given text                                         audio
    engine.say(text)
        # Wait for the speech to finish
    engine.runAndWait()
    return render(request, 'output.html', {"result": text})


def texttotranslate(request):
    # Ensure 'text_for_translate' is present in the session
    text = request.session.get('text_for_translate','')
    print(text)
    if text is  None:
        # If text is not None, proceed with translation
        translator = Translator()
        translation = translator.translate(text, dest='hi')

        # Set the translated text to a new session key
        request.session['translated_text'] = translation

        return render(request, 'output.html', {"result": translation.text})
    else:
        # If 'text_for_translate' is not present, handle accordingly
        return render(request, 'output.html', {"result": "Text for translation not found in session"})