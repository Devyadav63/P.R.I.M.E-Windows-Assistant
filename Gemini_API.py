
def Answer(x):
    import google.generativeai as genai

    genai.configure(api_key="AIzaSyD6Zxf_u7LrLnJYynnhUT6-ZlId8ysfV0Y")

    # Set up the model
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["how r u"]
    },
    {
        "role": "model",
        "parts": ["I am an AI language model, so I don't have feelings or experiences like humans do. However, I'm functioning well and ready to assist you. How can I help you today?"]
    },
    ])

    convo.send_message(x)
    return convo.last.text
