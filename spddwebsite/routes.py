import torch
from flask import render_template, flash, redirect, url_for, jsonify, request
from spddwebsite import app
import openai
from PIL import Image
from transformers import ResNetConfig, ResNetForImageClassification

from torchvision import transforms
from spddwebsite.spdd_model import classify_plant

# Set your OpenAI API key
openai.api_key = "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"


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/disease_detection", methods=['GET','POST'])
def project():
    return render_template('disease_detection.html')


@app.route("/user_query", methods=['GET','POST'])
def user_query():
    context = [{'role': 'system', 'content': f"""
        act as a Plant Pathologist and tell me more about {class_name}
        ***********************************************
        output: the output should take into consideration the following
        - make the output 100 words at most
        - use easy words to understand
    """}]
    if request.method == "GET":
        gptresponse = get_completion_from_messages(context)
        context.append({'role': 'assistant', 'content': gptresponse})
        response = {"response" : gptresponse}
        print(response)

    if request.method == "POST":
        if request.json['prompt']:
            prompt = request.json['prompt']
            context.append({'role': 'user', 'content': prompt})
            gptresponse = get_completion_from_messages(context)
            context.append({'role': 'assistant', 'content': gptresponse})
            response = { "response": gptresponse }
            print(response)
    
    return  jsonify(response)


@app.route("/team_member")
def about():
    return render_template('team_member.html')


@app.route("/resourses")
def resorce():
    return render_template('resourses.html')


@app.route("/datarespons", methods=['GET','POST'])
def response(): 
    image_file = request.files['image']
    outputs = classify_plant(image_file)
    class_name = outputs['name']
    response={
        "name":  outputs['name'],
        "plant": outputs['plant'],
        "healthy": outputs['healthy'],
        "disease": outputs['disease'],
        "plant_probability": outputs['plant_probability']
    }
    
    return  jsonify(response)