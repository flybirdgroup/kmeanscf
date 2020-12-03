import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn import metrics
import datetime
from Utilities.data_processing import data_cleanup
#pamars
from Utilities.parameters import *

def feature_engineering_processing(K_value,max_iter_eps):
    # read data
    df = pd.read_excel(sales_data_path)
    df = data_cleanup(df)

    # select fields
    df_new = df[['Invoice_date','CUSTOMER','PROVINCE','CUSTYP', 'TYPDES', 'ITEM', 'QTY', 'price','PERIOD']]

    # Feature Engineering
    # change date string into date Type
    df_new['paytime'] = pd.to_datetime(df_new['Invoice_date'].apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d')))

    # extract customer's closest purchase date --提取每个用户最近（最大）的购买日期
    data_r = df_new.groupby('CUSTOMER')['paytime'].max().reset_index()
    # we set the report date is 2020-01-01, so we calculate the how days between purchase date and report date
    # 当前日期相减，取得最近一次购买距当前的天数。
    data_r['recency'] = data_r['paytime'].apply(lambda x:(pd.to_datetime('2020-01-01')-x).days)
    # 两个日期相减，得到的数据类型是timedelta类型，要进行数值计算，需要提取出天数数字。
    data_r.drop('paytime',axis = 1,inplace = True)

    # Frequency--用户最近一段时间内累计消费频次，衡量用户的粘性
    # 分组聚合，得到每个用户发生于不同日期的购买次数
    data_f = df_new.groupby(['CUSTOMER','paytime'])['Invoice_date'].count().reset_index()
    data_f = data_f.groupby('CUSTOMER')['paytime'].count().reset_index()
    # 修改列名
    data_f.rename({'paytime':'frequence'},axis = 1,inplace = True)

    # M（Money)： 用户最近一段时间内累计消费金额，衡量用户的消费能力和忠诚度
    df_new['sales']=df_new["QTY"]*df_new["price"]
    data_m = df_new.groupby('CUSTOMER')['sales'].sum().reset_index()
    data_m['money'] = data_m['sales']/data_f['frequence']
    data_m.drop('sales',axis = 1,inplace = True)
    data_rf = pd.merge(data_r,data_f,on = 'CUSTOMER',how = 'inner')
    data_rfm = pd.merge(data_rf,data_m, on = 'CUSTOMER',how = 'inner')


    plt.figure(figsize = (6,4))
    sns.set(style = 'darkgrid')
    sns.countplot(data_rfm['frequence'])

    sns.distplot(data_rfm['recency'])
    plt.title('recency distribution',fontsize = 15)

    sns.distplot(data_rfm['money'],color = 'g')
    plt.title('money distritbution',fontsize = 15)


    # one hot
    df_one_hot = df_new[['CUSTOMER','PROVINCE','CUSTYP', 'TYPDES', 'ITEM','PERIOD']]
    df_one_hot = pd.get_dummies(df_one_hot,columns=['PROVINCE','CUSTYP', 'TYPDES', 'ITEM','PERIOD'])
    df_one_hot = df_one_hot.groupby("CUSTOMER").sum().reset_index()

    df_one_hot = df_one_hot.groupby("CUSTOMER").sum().reset_index()
    df_all_new_features = pd.merge(data_rfm,df_one_hot, on = 'CUSTOMER',how = 'inner')

    # 对连续性数值进行标准化比如Zscore
    data_rfm = df_all_new_features.copy()
    min_max_scaler = preprocessing.MinMaxScaler()
    data_rfm_s = min_max_scaler.fit_transform(df_all_new_features.iloc[:,1:])

    # 选择合适的cluster个数
    inertia = []
    ch_score = []
    ss_score = []
    for k in range(2,9):
        model = KMeans(n_clusters=k, init='k-means++',max_iter=max_iter_eps)
        model.fit(data_rfm_s)
        pre = model.predict(data_rfm_s)
        ch = metrics.calinski_harabasz_score(data_rfm_s,pre)
        ss = metrics.silhouette_score(data_rfm_s,pre)
        inertia.append(model.inertia_)
        ch_score.append(ch)
        ss_score.append(ss)
    print(ch_score,ss_score,inertia)

    score = pd.Series([ch_score,ss_score,inertia],index = ['ch_score','ss_score','inertia'])
    aa = score.index.tolist()
    plt.figure(figsize = (15,6))
    j = 1
    for i in aa:
        plt.subplot(1,3,j)
        plt.plot(list(range(2,9)),score[i])
        plt.xlabel('k numbers',fontsize = 13)
        plt.ylabel(f'{i}value',fontsize = 13)
        plt.title(f'{i}value chaning trend',fontsize = 15)
        j+=1
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(plt_save_path)

    model = KMeans(n_clusters=K_value, init='k-means++', max_iter=max_iter_eps)
    model.fit(data_rfm_s)
    ppre = model.predict(data_rfm_s)
    ppre = pd.DataFrame(ppre)
    data = pd.concat([df_all_new_features,ppre], axis=1)
    data.rename({0:u'cluster'},axis=1, inplace=True)

    customer = pd.merge(data[['CUSTOMER','cluster']],df_new, on = 'CUSTOMER',how = 'inner')
    customer.to_csv(cluster_all_path)
    # 基于聚类分类,使用协同过滤算法进行产品推荐给不同客户

    for i in range(int(K_value)):
        print(i)
        cluster = customer[customer["cluster"] == i][['CUSTOMER', 'ITEM', 'QTY']]
        path = './data/output/cluster_%s.csv'%(i)
        cluster.groupby(['CUSTOMER','ITEM']).sum().to_csv(path)
        print(path)
    data[['CUSTOMER', 'cluster']].to_csv(customer_cluster_path)
    return data[['CUSTOMER','cluster']]

if __name__ == '__main__':
    feature_engineering_processing(K_value,max_iter_eps)