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
filename = 'model.pth'


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/disease_detection", methods=['GET','POST'])
def project():
    if 'image' not in request.files:
        print("No file uploaded")
        return render_template('disease_detection.html')


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def get_chatbot_response(prompt,context):
    context.append({'role': 'user', 'content': prompt})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': response})
    return response,context


@app.route("/gptresponse", methods=['GET','POST'])
def gptresponse(fname):
   
    #class_name = "Tomato__Target_Spot"
    context = [{'role': 'system', 'content': f"""
        act as a Plant Pathologist and tell me more about {fname}
        ***********************************************
        output: the output should take into consideration the following
        - make the output 100 words at most
        - use easy words to understand
    """}]
    gptresponse = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': gptresponse})
    response={

        "gptresponse": gptresponse,
        "context":context
    }
    return  jsonify(response)


@app.route("/userqa", methods=['GET','POST'])
def userqa(prompt,context):

    if request.method == "POST":
        prompt = request.json['prompt']
        context = request.json['context']
        gpt_response,context = get_chatbot_response(prompt,context)
        response={

            "gpt_response": gpt_response,
            "context":context
        }
    
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

    response={
        "name":  outputs['name'],
        "plant": outputs['plant'],
        "healthy": outputs['healthy'],
        "disease": outputs['disease'],
        "plant_probability": outputs['plant_probability']
    }
    
    return  jsonify(response)