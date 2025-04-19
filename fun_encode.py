"""
2025.03.18
encrypt and decrypt utils
"""
import sys
import csv
import argparse


def encrypt(s_key, s_in):
    """
    加密函数
    :param s_key: 密钥
    :param s_in: 待加密的字符串
    :return: 加密后的字符串（十六进制表示）
    """
    # 将密钥重复填充到与输入字符串相同的长度
    key = (s_key * (len(s_in) // len(s_key))) + s_key[:len(s_in) % len(s_key)]

    # 使用异或操作进行加密
    encrypted_bytes = bytes([ord(c1) ^ ord(c2) for c1, c2 in zip(s_in, key)])

    # 将加密后的字节转换为十六进制字符串
    encrypted_hex = encrypted_bytes.hex()

    return encrypted_hex


def decrypt(s_key, s_encrypted):
    """
    解密函数
    :param s_key: 密钥
    :param s_encrypted: 加密后的字符串（十六进制表示）
    :return: 解密后的字符串
    """
    # 将加密后的十六进制字符串还原为字节
    encrypted_bytes = bytes.fromhex(s_encrypted)

    # 将密钥重复填充到与加密后的字节相同的长度
    key = (s_key * (len(encrypted_bytes) // len(s_key))) + s_key[:len(encrypted_bytes) % len(s_key)] # noqa

    # 使用异或操作进行解密
    decrypted_bytes = bytes([b ^ ord(k) for b, k in zip(encrypted_bytes, key)])

    # 将解密后的字节转换为字符串
    decrypted_result = decrypted_bytes.decode('utf-8', errors='ignore')

    return decrypted_result


def encrypt_csv_column(file_in, file_ot, idx, s_key):
    """
    对 CSV 文件的第 idx 列调用加密函数，并输出到新的文件中

    :param file_in: 输入的 CSV 文件路径
    :param file_ot: 输出的 CSV 文件路径
    :param idx: 要加密的列索引（从 0 开始计数）
    :s_key: Secret Key
    """
    try:
        with open(file_in, mode='r', newline='', encoding='utf-8') as infile, \
             open(file_ot, mode='w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # 写入标题行（不加密）
            headers = next(reader, None)  # 读取第一行作为标题
            if headers:
                writer.writerow(headers)

            # 逐行读取并处理
            for row in reader:
                if len(row) > idx:  # 确保列索引有效
                    row[idx] = encrypt(s_key, row[idx])  # 对指定列调用加密函数
                writer.writerow(row)  # 写入新文件

        print(f"加密完成，结果已保存到 {file_ot}")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")


def main():
    parser = argparse.ArgumentParser(description="CSV 文件加密工具")
    parser.add_argument("--file_in", help="输入的 CSV 文件路径")
    parser.add_argument("--file_ot", default="output.csv", help="输出的 CSV 文件路径，默认为 output.csv") # noqa
    parser.add_argument("--idx", type=int, default=0, help="要加密的列索引，默认为第 1 列（从 0 开始）") # noqa
    parser.add_argument("--s_in", help="单个字符串输入，用于加密或解密")
    parser.add_argument("--key", help="Secret Key")
    parser.add_argument("--encode_type", choices=["encrypt", "decrypt"], help="加密或解密操作类型") # noqa

    args = parser.parse_args()

    if args.file_in:
        # 如果传入了 --file_in 参数，则对 CSV 文件进行加密
        encrypt_csv_column(args.file_in, args.file_ot, args.idx, args.key)
    elif args.s_in and args.encode_type:
        # 如果传入了 --s_in 和 --encode_type 参数，则对单个字符串进行加密或解密
        if args.encode_type == "encrypt":
            result = encrypt(args.key, args.s_in)
            print(f"加密结果：{result}")
        elif args.encode_type == "decrypt":
            result = decrypt(args.key, args.s_in)
            print(f"解密结果：{result}")
    else:
        print("请传入有效的参数。")


if __name__ == "__main__":
    """
    """
    main()

    sys.exit(0)

    # 测试代码
    s_key = "mysecretkey"
    s_in = "Hello, this is a test message!"

    encrypted = encrypt(s_key, s_in)
    print(f"加密后的字符串: {encrypted}")

    decrypted = decrypt(s_key, encrypted)
    print(f"解密后的字符串: {decrypted}")


"""
# noqa
python fun_encode.py --encode_type='encrypt' --key='xxx' --s_in='abc'
python fun_encode.py --encode_type='decrypt' --key='xxx' --s_in='191a1b'
python fun_encode.py --file_in='datas/account/account.csv' --file_ot='datas/account/encrypt.csv' --idx=2 --key='xxx'
"""
