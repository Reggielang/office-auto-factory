import re
from datetime import datetime


def is_valid_id(id_number):
    if len(str(id_number)) != 18:
        return False

    if not id_number[:-1].isdigit() or id_number[-1] not in '0123456789Xx':
        return False

    # 检查地区码
    region_codes = {
        "11": "北京市", "12": "天津市", "13": "河北省", "14": "山西省", "15": "内蒙古自治区",
        "21": "辽宁省", "22": "吉林省", "23": "黑龙江省", "31": "上海市", "32": "江苏省",
        "33": "浙江省", "34": "安徽省", "35": "福建省", "36": "江西省", "37": "山东省",
        "41": "河南省", "42": "湖北省", "43": "湖南省", "44": "广东省", "45": "广西壮族自治区",
        "46": "海南省", "50": "重庆市", "51": "四川省", "52": "贵州省", "53": "云南省",
        "54": "西藏自治区", "61": "陕西省", "62": "甘肃省", "63": "青海省", "64": "宁夏回族自治区",
        "65": "新疆维吾尔自治区", "71": "台湾省", "81": "香港特别行政区", "82": "澳门特别行政区"
    }

    region_code = id_number[:2]
    if region_code not in region_codes:
        return False

    # 检查生日码
    try:
        birth_date = datetime.strptime(id_number[6:14], '%Y%m%d')
    except ValueError:
        return False

    # 检查生日码是否合理
    min_birth_year = 1900  # 最小出生年份
    max_birth_year = datetime.now().year  # 当前年份
    if birth_date.year < min_birth_year or birth_date.year > max_birth_year:
        return False

    # 计算校验码
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_sum = sum(int(id_number[i]) * weights[i] for i in range(17))
    check_digit = str(check_sum % 11)
    valid_check_digits = '10X98765432'
    return id_number[-1].upper() == valid_check_digits[int(check_digit)]


def verify_phone_number(phone_number):
    # 手机号码正则表达式
    mobile_phone_pattern = r'^1[3-9]\d{9}$'
    try:
        # 先转为int,把浮点数的小数点去掉
        phone_number = int(phone_number)
        # 检查手机号码正则需要字符串
        if re.match(mobile_phone_pattern, str(phone_number)) and len(str(phone_number)) == 11:
            return True
        else:
            return False
    except:
        return False


def verify_enum_values(df, enum_dict, column, col1, col2):
    """
    校验DataFrame中指定列的值是否满足给定的枚举值集合，并添加一个新列来表示校验结果。
    参数:
    df : pandas.DataFrame
        包含需要校验的数据的DataFrame。
    enum_dict : dict
        字典，键为DataFrame的列名，值为该列允许的枚举值列表。
    column : str
        需要校验的列名。
    返回:
    pandas.DataFrame
        包含原始DataFrame的所有列以及一个新列，表示每行是否满足枚举条件。
    """
    # 使用apply方法来应用未通过枚举值的值获取函数

    df[col1] = df[column].apply(lambda x: True if x in enum_dict else False)
    df[col2] = df[column].apply(lambda x: x if x not in enum_dict else False)
    return df


def verify_num(number):
    return str(number).isdigit()


def verify_len(df, column, length):
    df["长度校验"] = df[column].apply(lambda x: len(str(x)) == length)
    return df
