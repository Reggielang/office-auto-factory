from os.path import splitext

import pandas as pd

from src.checks.base import valid
from src.checks.utils.log_utils import log


def load_data(file):
    pd.options.display.float_format = '{:.0f}'.format
    _, ext = splitext(file)
    if ext in ('.xls', '.xlsx'):
        df = pd.read_excel(file)
    elif ext == '.csv':
        df = pd.read_csv(file)
    else:
        raise ValueError("无法校验该文件类型！")
    return df


def check_df(df, head=5):
    headDF = df.head(head)
    log.info(f"---------------------数据样例： {headDF} ---------------------")
    col = df.columns.tolist()
    log.info(f"--------------------- 数据列名：{col}  ---------------------")
    return df


def verification_None(df, column_name, log_func):
    """
       根据指定列名查找包含空值的行
       :param df: Pandas DataFrame
       :param columns: 需要检查的列名列表
       :return: 包含空值的行的 DataFrame
    """
    new_col = column_name + '-' + "空值校验"
    # 检查指定列是否包含空值
    df[new_col] = df[column_name].isnull()
    missing_values = df[df[new_col] == False].copy()
    missing_values = missing_values.reset_index(drop=True)
    if not missing_values.empty:
        log_func(
            f"---------------------列 '{column_name}' 没有通过空值校验 未通过空值校验数据行数：{len(missing_values)} ---------------------")
        return df

    log_func(f"---------------------列 '{column_name}' 通过空值校验，无空值 ---------------------")
    return df  # 返回空 DataFrame 表示没有找到空值


def verification_id(df, column_name, log_func):
    """
    校验 DataFrame 中指定列的身份证号码是否有效。
    参数:
    - df: 包含身份证号码的 DataFrame
    - column_name: 身份证号码所在的列名称，默认为 'id_number'
    """
    new_col = column_name + '-' + "身份证校验"
    df[new_col] = df[column_name].apply(valid.is_valid_id)
    # 筛选出不满足条件的行
    missing_values = df[df[new_col] == False].copy()
    missing_values = missing_values.reset_index(drop=True).replace(False, "身份证校验不通过")

    if not missing_values.empty:
        log_func(
            f"---------------------列 '{column_name}' 没有通过身份证校验 未通过身份证校验数据行数：{len(missing_values)} ---------------------")
        return df

    log_func(f"---------------------列 '{column_name}' 通过身份证校验 ---------------------")
    return df  # 返回空 DataFrame 表示没有找到空值


def verification_phone(df, column_name, log_func):
    new_col = column_name + '-' + "手机校验"
    df[new_col] = df[column_name].apply(valid.verify_phone_number)
    # 筛选出不满足条件的行
    missing_values = df[df[new_col] == False].copy()
    missing_values = missing_values.reset_index(drop=True).replace(False, "手机校验不通过")

    if not missing_values.empty:
        log_func(
            f"---------------------列 '{column_name}' 没有通过手机号码校验 未通过手机号码校验数据行数：{len(missing_values)} ---------------------")
        return df

    log_func(f"---------------------列 '{column_name}' 通过手机号码校验 ---------------------")
    return df  # 返回空 DataFrame 表示没有找到空值


def verification_enum(df, enum_dict, column_name, log_func):
    new_col = column_name + '-' + "枚举值校验"
    new_col2 = column_name + '-' + "未通过枚举校验的值"
    # 校验枚举值
    df = valid.verify_enum_values(df, enum_dict, column_name, new_col, new_col2)
    # 筛选出不满足条件的行
    missing_values = df[df[new_col] == False].copy()
    # missing_values = missing_values.reset_index(drop=True).replace(False, "枚举值校验不通过")

    # 记录未通过校验的信息
    if not missing_values.empty:
        log_func(
            f"---------------------列 '{column_name}' 没有通过枚举值校验 未通过枚举值校验数据行数：{len(missing_values)} ---------------------")
        return df

    log_func(f"---------------------列 '{column_name}' 通过枚举值校验 ---------------------")
    return df.drop(columns=[new_col2])


def verification_num(df, column_name, log_func):
    new_col = column_name + '-' + "数值校验"
    df[new_col] = df[column_name].apply(valid.verify_num)
    # 筛选出不满足条件的行
    missing_values = df[df[new_col] == False].copy()
    missing_values = missing_values.reset_index(drop=True).replace(False, "数值校验不通过")

    if not missing_values.empty:
        log_func(
            f"---------------------列 '{column_name}' 没有通过数值校验 未通过数值校验校验数据行数：{len(missing_values)} ---------------------")
        return df

    log_func(f"---------------------列 '{column_name}' 通过数值校验 ---------------------")
    return df  # 返回空 DataFrame 表示没有找到空值


def verification_len(df, column_name, length, log_func):
    new_col = column_name + '-' + "长度校验"
    df[new_col] = df[column_name].apply(lambda x: len(str(x)) == length)
    # 筛选出不满足条件的行
    missing_values = df[df[new_col] == False].copy()
    missing_values = missing_values.reset_index(drop=True).replace(False, "长度校验不通过")
    if not missing_values.empty:
        log_func(
            f"---------------------列 '{column_name}' 没有通过长度校验 未通过长度校验数据行数：{len(missing_values)} ---------------------")
        return missing_values

    log_func(f"---------------------列 '{column_name}' 通过长度校验 ---------------------")
    return df  # 返回空 DataFrame 表示没有找到空值

# if __name__ == '__main__':
#     df = check_df(load_data(r"D:\Bot\office-auto-factory\office-auto-factory\data\test.xlsx"))
#     # 调用函数
#
#     # # missing_rows = verification_None(df, 'materialcode')
#     # missing_rows = verification_id(df, 'materialcode')
#     # missing_rows = verification_phone(df, 'phone')
#     text = '12米定尺HRB400EФ12,b,c'
#     enum_dict = text.split(',')
#     missing_rows = verification_enum(df, enum_dict, 'specification')
#     # missing_rows = verification_num(df, 'number')
#     # missing_rows = verification_len(df, 'len', 9)
