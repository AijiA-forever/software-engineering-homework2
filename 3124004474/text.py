import time

from main import *
import os

def batch_check(original_dir="test_cases\\original",plagiarism_dir="test_cases\\plagiarism",
                result_dir="test_cases\\result", answer_dir="test_cases\\answer"):
    """
    批量查重：自动配对 original 与 plagiarism 中的同名文件，结果保存到 result 文件夹
    """
    # 创建结果文件夹
    os.makedirs(result_dir, exist_ok=True)

    # 获取原文件列表，按文件名排序
    orig_files = sorted([f for f in os.listdir(original_dir) if f.endswith(".txt")])

    if not orig_files:
        print(f"[错误] 在 {original_dir} 文件夹中没有找到 txt 文件")
        return

    print(f"共找到{len(orig_files)}个原文件")

    for idx, orig_files in enumerate(orig_files, 1):
        orig_path = os.path.join(original_dir, orig_files)
        plag_path = os.path.join(plagiarism_dir, orig_files.replace("orig", "plag"))
        answer_path = os.path.join(answer_dir, orig_files.replace("orig", "ans"))
        result_path = os.path.join(result_dir, orig_files.replace("orig", "result"))

        if not os.path.exists(plag_path):
            print(f"error!不存在{orig_path}对应的抄袭文件")
            continue

        # 资源消耗评估
        t0 = time.time()
        # tracemalloc.start()

        with open(orig_path, "r", encoding="utf-8") as f:
            text1 = f.read()
            word1 = re_jieba(text1)
        with open(plag_path, "r", encoding="utf-8") as f:
            text2 = f.read()
            word2 = re_jieba(text2)
        with open(answer_path, "r", encoding="utf-8") as f:
            answer = float(f.read())

        shingle_list = [n_gram(word1, 2), n_gram(word2, 2)]

        res = jaccard(shingle_list) * 100

        is_common = (res * 0.9 <= answer <= res * 1.1)

        # 资源消耗评估
        run_time = time.time() - t0
        # current, peak = tracemalloc.get_traced_memory()
        # tracemalloc.stop()

        with open(result_path, "w", encoding="utf-8") as f:
            f.write(f'原论文字符数：{len(text1)}\n')
            f.write(f'抄袭版论文字符数：{len(text2)}\n')
            f.write(f'两篇论文的重合度为：{res:.2f}%\n')
            f.write(f'答案：{answer}\n')
            f.write(f'两者是否相似：{is_common == True}\n')
            if answer != 0:
                f.write(f'两者相差比例：{abs(res - answer) / answer * 100:.2f}%\n')
            f.write(f'运行时间：{run_time:.4f}秒\n')

        # with open(result_path, "a", encoding="utf-8") as f:
        #     f.write(f"最大内存占用：{peak/1024/1024:.4f}MB\n")

batch_check()