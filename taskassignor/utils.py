import hashlib, time


# 辅助函数
def str_encrypt(string):
    """
    用于将string通过sha1算法生成唯一的r_id
    :param string: 传入需要转换的字符串
    :type string: str
    :return: 经过sha1计算的str
    """
    sha = hashlib.sha1(string.encode())
    encrypts = sha.hexdigest()
    return encrypts


def hash_id(assignor_id):
    return str(assignor_id)+str(time.time())