from Utilities.feature_engineering import feature_engineering_processing
from Utilities.utility import *
import warnings
warnings.filterwarnings("ignore")


#pamars
sales_data_path = '../data/2019.xlsx'
plt_save_path = './data/pic'
csv_file = "../data/cluster_0.csv"
customer_id='HK000000580H'
K_value = 3
max_iter_eps = 500
customer_cluster = feature_engineering_processing()
# print(customer_cluster.head())
cluster_num = customer_cluster[customer_cluster['CUSTOMER']==customer_id]['cluster'].values
cluster_num = cluster_num[0]
print(cluster_num)


def run():
    file = open("./data/cluster_%s.csv"%cluster_num,'r', encoding='UTF-8')#记得读取文件时加‘r’， encoding='UTF-8'
    ##读取data.csv中每行中除了名字的数据
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

    RES = Customers(data,customer_id)
    re_items, top_similar = RES.recommend()
    # print('recommend items', re_items)
    # print('top similarity', top_similar)

if __name__ == '__main__':
    run()