from math import *


class Customers(object):
    def __init__(self, data_dict,userID):
        self.data = data_dict
        self.userID = userID

    def Euclidean(self,user1,user2):
        # 取出两位用户购买的产品
        user1_data = self.data[user1]
        user2_data = self.data[user2]
        distance = 0
        # 找到两位用户都购买的产品和数量，并计算欧式距离
        for key in user1_data.keys():
            if key in user2_data.keys():
                # 注意，distance越大表示两者越相似
                distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

        return 1 / (1 + sqrt(distance))  # 这里返回值越小，相似度越大

    # 计算某个用户与其他用户的相似度
    def top_simliar_customers(self):
        res = []
        for userid in self.data.keys():
            # 排除与自己计算相似度
            if not userid == self.userID:
                simliar = self.Euclidean(self.userID, userid)
                res.append((userid, simliar))
        res.sort(key=lambda val: val[1])
        return res[:5]

    def recommend(self):
        # 相似度最高的用户
        top_sim_user = self.top_simliar_customers()[0][0]
        print(top_sim_user)
        # 相似度最高的用户的产品记录
        items = self.data[top_sim_user]
        recommendations = []
        # 筛选出该用户未购买的产品并添加到列表中
        for item in items.keys():
            if item not in self.data[self.userID].keys():
                recommendations.append((item, items[item]))
        recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
        # 返回销量最高的10个产品
        print(recommendations[:10])
        return recommendations[:10],top_sim_user


def province_to_short(province):
    if province == "广东":
        return "GD"
    elif province == "天津":
        return "TJ"
    elif province == "山东":
        return "SD"
    elif province == "辽宁":
        return "LN"
    elif province == "江苏":
        return "JS"
    elif province == "黑龙江":
        return "HLJ"
    elif province == "吉林":
        return "JL"
    elif province == "福建":
        return "HLJ"
    elif province == "安徽":
        return "JL"
    elif province == '北京': 
        return 'BJ' 
    elif province == '湖南': 
        return 'HN' 
    elif province == '上海': 
        return 'SH' 
    elif province == '重庆': 
        return 'CQ' 
    elif province == '山西': 
        return 'SX' 
    elif province == '四川': 
        return 'SC' 
    elif province == '江西': 
        return 'JX' 
    elif province == '浙江': 
        return 'ZJ' 
    elif province == '湖北': 
        return 'HUB' 
    elif province == '河北': 
        return 'HEB' 
    elif province == '陕西': 
        return 'XX' 
    elif province == '广西': 
        return 'GX' 
    elif province == '内蒙古': 
        return 'NMG' 
    elif province == '云南': 
        return 'YN' 
    elif province == '宁夏': 
        return 'LX' 
    elif province == '甘肃': 
        return 'GS' 
    elif province == '河南': 
        return 'HEN' 
    elif province == 'GERMANY': 
        return 'DE' 
    elif province == 'ITALY': 
        return 'IT' 
    elif province == 'TAIWAN': 
        return 'TW' 
    elif province == 'SINGAPORE': 
        return 'SG' 
    elif province == '香港': 
        return 'HK' 
