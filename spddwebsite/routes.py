import io
import torch
from flask import render_template, flash, redirect, url_for, jsonify, request
from spddwebsite import app, spdd_db
from spddwebsite.forms import RegistrationForm, LoginForm
from spddwebsite.models import User, Plant
from spddwebsite.models import UserSchema, PlantSchema
import openai
from PIL import Image
from transformers import ResNetConfig, ResNetForImageClassification
# import transformers
from torchvision import transforms

# Set your OpenAI API key
openai.api_key = "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"
filename = 'resnet_model.pth'

classes=['Tomato__Target_Spot',
 'Tomato_Late_blight',
 'Pepper__bell___healthy',
 'Potato___Late_blight',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato_Spider_mites_Two_spotted_spider_mite',
 'Pepper__bell___Bacterial_spot',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Leaf_Mold',
 'Potato___healthy',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_healthy',
 'Potato___Early_blight']

class_dict = {
    "0": {
        "name": "Tomato__Target_Spot",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Target Spot"
    },
    "1": {
        "name": "Tomato_Late_blight",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Late Blight"
    },
    "2": {
        "name": "Pepper__bell___healthy",
        "plant": "Pepper",
        "healthy": False,
        "disease": None
    },
    "3": {
        "name": "Potato___Late_blight",
        "plant": "Potato",
        "healthy": False,
        "disease": "Late Blight"
    },
    "4": {
        "name": "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Tomato Yellow Leaf Curl Virus"
    },
    "5": {
        "name": "Tomato_Spider_mites_Two_spotted_spider_mite",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Spider Mites (Two-Spotted Spider Mite)"
    },
    "6": {
        "name": "Pepper__bell___Bacterial_spot",
        "plant": "Pepper",
        "healthy": False,
        "disease": "Bacterial Spot"
    },
    "7": {
        "name": "Tomato_Septoria_leaf_spot",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Septoria Leaf Spot"
    },
    "8": {
        "name": "Tomato_Leaf_Mold",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Leaf Mold"
    },
    "9": {
        "name": "Potato___healthy",
        "plant": "Potato",
        "healthy": True,
        "disease": None
    },
    "10": {
        "name": "Tomato__Tomato_mosaic_virus",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Tomato Mosaic Virus"
    },
    "11": {
        "name": "Tomato_Bacterial_spot",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Bacterial Spot"
    },
    "12": {
        "name": "Tomato_Early_blight",
        "plant": "Tomato",
        "healthy": False,
        "disease": "Early Blight"
    },
    "13": {
        "name": "Tomato_healthy",
        "plant": "Tomato",
        "healthy": True,
        "disease": None
    },
    "14": {
        "name": "Potato___Early_blight",
        "plant": "Potato",
        "healthy": False,
        "disease": "Early Blight"
    }
}
@app.route("/create")
def create():
	spdd_db.create_all()  
	return "Tables created!"

@app.route("/")
@app.route("/index")
def home():
	return render_template('index.html')
	
# @app.route("/disease_detection", methods=['GET'])
# def show_disease_detection():
# 	return render_template('disease_detection.html')

@app.route("/disease_detection", methods=['GET','POST'])
def project():
	# Load the model state dict
	model_state_dict = torch.load("spddwebsite\model.pth",map_location=torch.device('cpu') )
	model = ResNetForImageClassification.from_pretrained('microsoft/resnet-152')
	# Load the state dict into the new model
	model.load_state_dict(model_state_dict)
	
	if 'image' not in request.files:
		print("No file uploaded")
		return render_template('disease_detection.html')

@app.route("/team_member")
def about():
	return render_template('team_member.html')

@app.route("/resourses")
def resorce():
	return render_template('resourses.html')


@app.route("/datarespons", methods=['GET','POST'])
def response():
	# Load the model state dict
	model_state_dict = torch.load("spddwebsite\model.pth",map_location=torch.device('cpu') )
	model = ResNetForImageClassification.from_pretrained('microsoft/resnet-152')
	# Load the state dict into the new model
	model.load_state_dict(model_state_dict)
	
	image_file = request.files['image']

	image =Image.open(io.BytesIO(image_file.read())).convert("RGB")

	# Define a transform to resize the image to 64x64
	predict_transform = transforms.Compose([
		transforms.Resize((64, 64)),
		transforms.ToTensor()
	])

	# Convert the image to a tensor
	img_tensor = predict_transform(image).unsqueeze(dim=0)
	outputs = model(img_tensor)

	_, predicted = torch.max(outputs.logits, 1)
	probabilities = torch.softmax(outputs.logits, dim=1)
	probability = probabilities[0][predicted]

	name =  class_dict[str(int(predicted))]['name']
	plant = class_dict[str(int(predicted))]['plant']
	healthy = class_dict[str(int(predicted))]['healthy']
	disease = class_dict[str(int(predicted))]['disease']
	plant_probability = probability[0].float().item()
	

	print("Class Name:", name)
	print("Plant Name:", plant)
	print("Is Healthy:", healthy)
	print("Disease Name:", disease)
	print("Probablity of the prediction:",plant_probability*100,"%")
	response={
        "name": name,
        "plant": plant,
        "healthy": healthy,
        "disease": disease,
        "plant_probability": round(plant_probability * 100, 3)
    }
	return  jsonify(response)
 
	 
    
    
    
 
    
    
 
 
 
   
	
	





# return render_template('disease_detection.html',name=name,plant=plant,healthy=healthy,disease=disease,plant_probability=plant_probability)
	# return render_template('disease_detection.html',name)
	# return render_template('disease_detection.html')
	# return name
# @app.route("/create_user")
# def create_user():
# 	user = User(username='Adam', email='add_203@gmail.com', password='passwor2', image_file=None)
# 	spdd_db.session.add(user)
# 	spdd_db.session.commit()
# 	return f'User {user.username} created!'

# @app.route("/users")
# def get_users():
# 	users = User.query.all()
# 	user_schema = UserSchema(many=True)
# 	output = user_schema.dump(users)
# 	return jsonify({'in': output})


# @app.route("/login", methods=['GET', 'POST'])
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		if form.email.data == 'admain@spdd.net' and form.password.data == 'password':
# 			flash('You have been logged in!', 'success')
# 			return redirect(url_for('home'))
# 		else:
# 			flash('Login Unsuccessful. Please check username and password', 'danger')
# 	return render_template('login.html', title='Login', form=form)

# @app.route("/register", methods=['GET', 'POST'])
# def register():
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 		flash(f'Account created for {form.username.data}!', 'success')
# 		return redirect(url_for('home'))
# 	return render_template('register.html', title='Register', form=form)
	
