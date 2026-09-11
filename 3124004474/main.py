import tracemalloc

import jieba
import argparse
import re  # 正则模块，用来清洗数据
import time

def re_jieba(text):
    """
    数据预处理，除去空格换行标点符号，并进行分词
    :param text: 读取的文档数据
    :return: 包含分词的列表
    """
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)
    return jieba.lcut(text)

def n_gram(words, k = 2):
    """
    :param words: 已进行分词的数据列表
    :param k: 滑动窗口大小
    :return: N-Gram集合，所有滑动窗口片段构成的集合
    """
    shingle = set([tuple(words[i:i+k]) for i in range(0, len(words) - k + 1)])
    return shingle

def jaccard(shingle_list):
    """
    精确计算 jaccard ，以此表示两篇论文的重合度
    :param shingle_list: 需进行比较的论文列表
    :return: 重合度
    """
    inters = len(shingle_list[0] & shingle_list[1])
    uni = len(shingle_list[0] | shingle_list[1])
    return inters/uni

def main():
    # 创建一个参数解析器对象parser, description用于描述脚本功能, 通过python main.py -h查找帮助
    parser = argparse.ArgumentParser(description="对文本文件进行jieba分词")
    # 告诉解释器，需要接收一个命令行参数
    parser.add_argument("file_pathA", help="原文本文件路径")
    parser.add_argument("file_pathB", help="抄袭文本文件路径")
    parser.add_argument("file_pathC", help="答案文本文件路径")

    # 解析命令行参数，把拿到的所有参数打包放到args对象里，此时就可以args.file_path
    args = parser.parse_args()

    with open(args.file_pathA, "r", encoding="utf-8") as f:
        textA = f.read()
    with open(args.file_pathB, "r", encoding="utf-8") as f:
        textB = f.read()
    with open(args.file_pathC, "r", encoding="utf-8") as f:
        answer = float(f.read().strip())

    wordsA = re_jieba(textA)
    wordsB = re_jieba(textB)

    shingle_list = [n_gram(wordsA,2), n_gram(wordsB,2)]

    res = jaccard(shingle_list)

    print(f'两篇论文的重合度为：{res * 100:.2f}%')
    print(f'答案：{answer}')
    print(f'两者是否相同:{round(res*100,2) == answer}')

if __name__ == "__main__":
    time_begin = time.time()
    # tracemalloc.start()

    main()
    # 获取内存占用情况
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()

    time_end = time.time()
    run_time = time_end - time_begin
    print(f"运行时长：{run_time:.4f} 秒")
    # print(f"当前内存占用：{current / 1024 / 1024:.2f} MB")
    # print(f"内存峰值：{peak / 1024 / 1024:.2f} MB")



