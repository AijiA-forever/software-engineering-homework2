import argparse
import re
from collections import Counter


def clean(text):
    """
    数据预处理，除去空格换行标点符号
    :param text: 读取的文档数据
    :return: 只含汉字、字母、数字的字符串
    """
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)


def counter_jaccard(counter_a, counter_b):
    """
    以字符为单位计算 jaccard，重复出现的字符按出现次数参与计算
    :param counter_a: 原文本的字符计数器
    :param counter_b: 抄袭文本的字符计数器
    :return: 重合度
    """
    inters = sum((counter_a & counter_b).values())
    uni = sum((counter_a | counter_b).values())
    return inters / uni


def main():
    # 创建一个参数解析器对象parser, description用于描述脚本功能, 通过python char_check.py -h查找帮助
    parser = argparse.ArgumentParser(description="按字符出现次数对文本文件进行查重")
    # 告诉解释器，需要接收两个命令行参数
    parser.add_argument("file_pathA", help="原文本文件路径")
    parser.add_argument("file_pathB", help="抄袭文本文件路径")

    # 解析命令行参数，把拿到的所有参数打包放到args对象里，此时就可以args.file_path
    args = parser.parse_args()

    with open(args.file_pathA, "r", encoding="utf-8") as f:
        textA = f.read()
    with open(args.file_pathB, "r", encoding="utf-8") as f:
        textB = f.read()

    res = counter_jaccard(Counter(clean(textA)), Counter(clean(textB))) * 100

    print(f'两篇论文的重合度为：{res:.2f}%')


if __name__ == "__main__":
    main()
