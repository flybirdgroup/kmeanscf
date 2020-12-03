
# data clean up, replace duplicated province name into same format
from Utilities.utility import province_to_short


def data_cleanup(df):
    df = df.replace('广东省','广东').replace('江苏省','江苏').replace('HONG KONG','香港')
    df['PROVINCE'] = df['PROVINCE'].apply(lambda x: province_to_short(x))

    # change Chinese into English
    df = df.rename(columns={"销售团队": "Sales_TEAM", "发票日期": "Invoice_date", "合同号": "Contract_NO","不含税单价":"price"})

    # process missing value 缺失值处理 - 因为数据量还是比较大,暂时dropna方法去掉
    df.dropna(inplace=True)
    return df