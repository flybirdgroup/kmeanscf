from flask import Flask, request, jsonify, render_template
from Utilities.feature_engineering import feature_engineering_processing
from Utilities.utility import *
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
from Utilities.parameters import *
import re
#pamars

customer_id='HK000000580H'
from model_trainning import Recommend


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	my_prediction = dict()
	if request.method == 'POST':
		message = request.form['message']
		RES = Recommend(message,sales_data_path,plt_save_path,K_value,max_iter_eps)
		prediction,top_similarity = RES.run()
		my_prediction['items'] = prediction
		my_prediction['top_similarity'] = top_similarity
	return render_template('result.html',prediction = my_prediction)

@app.route('/training',methods=['POST'])
def training():
	my_prediction = dict()
	if request.method == 'POST':
		message = request.form['parameters']
		K_value, max_iter_eps = tuple(message.split(sep=','))
		K_value = int(re.findall(r"\d+\.?\d*", K_value)[0])
		max_iter_eps = int(re.findall(r"\d+\.?\d*", max_iter_eps)[0])
		print('K',K_value,'mi',max_iter_eps)
		RES = Recommend(customer_id,sales_data_path,plt_save_path,K_value,max_iter_eps)
		RES.feature_engineering_processing()
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True,port=5050)