import google.generativeai as genai

genai.configure(api_key="AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc")

models = genai.list_models()
for model in models:
    print(model.name)

