import pandas as pd

from src.checks.handlers.check_df import verification_num, verification_phone, verification_enum, verification_None


def perform_verifications(df, verifications):
    """
    根据提供的元组列表对 DataFrame 进行一系列校验。

    参数:
    - df: 要校验的 DataFrame
    - verifications: 元组列表，每个元组包含 (列名, 校验函数名, 是否进行非空校验)

    返回:
    - 校验后的 DataFrame
    """
    from collections import defaultdict
    errors = defaultdict(list)

    # 定义一个字典来存储校验函数
    verification_functions = {
        'function1': verification_num,
        'function2': verification_phone,
        'function3': verification_enum,
    }

    for column, func_name, check_none in verifications:
        if check_none:
            # 如果需要检查非空，则先执行非空校验
            none_errors = verification_None(df, [column])
            if not none_errors.empty:
                errors[column].extend(none_errors['未通过校验原因'].tolist())

        if func_name in verification_functions:
            verification_func = verification_functions[func_name]
            # 执行特定的校验函数
            result_df = verification_func(df, column_name=column)

            # 收集校验错误
            if '未通过校验原因' in result_df.columns:
                error_rows = result_df[result_df['未通过校验原因'] == False]
                if not error_rows.empty:
                    errors[column].extend(error_rows['未通过校验原因'].tolist())

    # 根据错误信息更新原始 DataFrame
    for col, error_list in errors.items():
        df.loc[df[col].isin(error_list), '未通过校验原因'] = error_list

    return df


# 示例数据
data = {
    'materialid': [1, 2, 3, 4, 5],
    'rentunit': ['A', 'B', 'C', 'D', 'E'],
    'pushstatus': [True, False, True, False, True]
}
df = pd.DataFrame(data)

# 需要校验的列和对应函数
verifications = [
    ('materialid', 'function1', False),
    ('rentunit', 'function2', True),
    ('pushstatus', 'function3', True)
]

# 执行校验
result_df = perform_verifications(df, verifications)
print(result_df)
