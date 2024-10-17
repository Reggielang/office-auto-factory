import datetime
import os

import pandas as pd

from src.checks.handlers.check_df import verification_None, verification_id, verification_len, \
    verification_enum, verification_phone, verification_num
from src.checks.utils.log_utils import log


def process_params(params, data, log_func, file_path):
    input_data = params
    df = data.copy()
    # 分解文件路径
    path, filename = os.path.split(file_path)
    file_name_with_extension, file_extension = os.path.splitext(filename)

    log_func(f"输入的全部校验内容为   {params}")
    log_func(f"--------------------------------以下是校验内容--------------------------------")
    log.info(f"输入的全部校验内容为   {params}")
    try:
        save_time = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
        # 根据输入数据进行校验
        results = []
        # 标记是否应当中断处理
        should_stop = False

        # 标准校验
        for column, check_type in input_data['standard']:
            if should_stop:
                break
            if check_type == '空值校验':
                null_df1 = verification_None(df.copy(), column, log_func)
                results.append(null_df1)
            if check_type == '身份证校验':
                id_df = verification_id(df.copy(), column, log_func)
                results.append(id_df)
            if check_type == '手机校验':
                phone_df = verification_phone(df.copy(), column, log_func)
                results.append(phone_df)
            if check_type == '数值校验':
                num_df = verification_num(df.copy(), column, log_func)
                results.append(num_df)

        # 高阶校验
        for column, check_type, param in input_data['advanced']:
            if should_stop:
                break
            if check_type == '长度校验':
                len_df = verification_len(df.copy(), column, int(param), log_func)
                results.append(len_df)
            elif check_type == '枚举值校验':
                enum_dict = param.split(',')
                enum_df = verification_enum(df.copy(), enum_dict, column, log_func)
                results.append(enum_df)

        if not should_stop:
            # 保存结果
            combined_results = pd.concat(results, axis=1)
            combined_results.to_excel(os.path.join(path, f"{file_name_with_extension}_校验_{save_time}.xlsx"),
                                      index=False)
            log_func(f"数据校验已完成 校验文件已保存至工作目录 {path}")
        else:
            log_func("任务已被取消")


    except Exception as e:
        log_func(f"处理过程中出现错误: {str(e)}")

        def merge_dfs_with_unique_columns(dfs):
            # 创建一个空的DataFrame作为结果集
            merged_df = pd.DataFrame()
            for df in dfs:
                # 找出当前DataFrame中不在merged_df中的列
                new_columns = [col for col in df.columns if col not in merged_df.columns]
                # 如果有新的列，则将它们添加到结果集中
                if new_columns:
                    # 仅选取新列
                    new_data = df[new_columns]
                    # 将新列合并到结果集中
                    merged_df = pd.concat([merged_df, new_data], axis=1)
            return merged_df

        # 合并DataFrame
        if results:
            final_df = merge_dfs_with_unique_columns(results)
            new_file_path = os.path.join(path, f'{save_time}-{file_name_with_extension}-校验.xlsx')
            final_df.to_excel(new_file_path, index=False)
            log_func(f"所有校验完成，返回最终的 DataFrame, 文件已正常保存.文件名为{new_file_path}")
            log.info(f"所有校验完成，返回最终的 DataFrame, 文件已正常保存.文件名为{new_file_path}")
        else:
            log_func("没有可输出的DataFrame")
            log.info("没有可输出的DataFrame")


    except Exception as e:
        log_func(f"参数解析出现问题:{str(e)},无法生成最终校验文件")
        log.error(f"参数解析出现问题:{str(e)}")

    # print(params)
