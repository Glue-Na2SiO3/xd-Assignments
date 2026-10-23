import hashlib
import itertools
import datetime

hash1 = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"

char_options = [['Q', 'q'], ['W', 'w'], ['%', '5'], ['8', '('], ['=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']]

def sha_encrypt(input_str):
    return hashlib.sha1(input_str.encode('utf-8')).hexdigest()

# 生成所有可能的字符组合
for combo in itertools.product(*char_options):
    # 对每个组合生成所有排列
    for permutation in itertools.permutations(combo):
        candidate = "".join(permutation)
        if sha_encrypt(candidate) == hash1:
            print("password:", candidate)
            break