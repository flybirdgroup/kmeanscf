from flask import Flask, request, jsonify, render_template
from Utilities.feature_engineering import feature_engineering_processing
from Utilities.utility import *
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
from Utilities.parameters import *
customer_id='HK000000580H'
import os,shutil

class Recommend(object):
	def __init__(self,customer_id,sales_data_path,plt_save_path,K_value,max_iter_eps):
		self.sales_data_path = sales_data_path
		self.plt_save_path = plt_save_path
		self.customer_id = customer_id
		self.K_value = K_value
		self.max_iter_eps = max_iter_eps
		self.customer_cluster_path = customer_cluster_path

	def feature_engineering_processing(self):
		customer_clusters = feature_engineering_processing(self.K_value,self.max_iter_eps)
		cluster_num = customer_clusters[customer_clusters['CUSTOMER'] == self.customer_id]['cluster'].values
		cluster_num = cluster_num[0]
		return cluster_num

	def return_cluster_num(self):
		customer_cluster = pd.read_csv(self.customer_cluster_path)
		cluster_num = customer_cluster[customer_cluster['CUSTOMER'] == self.customer_id]['cluster'].values
		cluster_num = cluster_num[0]
		return cluster_num

	def run(self):
		file = open("./data/output/cluster_%s.csv"%(self.return_cluster_num()),'r', encoding='UTF-8')
		data = {}##存放每位用户
		for line in file.readlines()[1:]:
			#注意这里不是readline()
			line = line.strip().split(',')
			#如果字典中没有某位用户，则使用用户ID来创建这位用户
			if not line[0] in data.keys():
				data[line[0]] = {line[1]:line[2]}
			#否则直接添加以该用户ID为key字典中
			else:
				data[line[0]][line[1]] = line[2]

		RES = Customers(data,self.customer_id)
		print(RES.recommend())
		return RES.recommend()

if __name__ == '__main__':
	RES = Recommend(customer_id, sales_data_path, plt_save_path, K_value, max_iter_eps)
	RES.feature_engineering_processing()