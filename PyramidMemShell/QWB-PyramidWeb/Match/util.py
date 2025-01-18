import base64
import json
import uuid
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import hashlib

secret = str(uuid.uuid4())


def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key




def sign_data(private_key, data):
    rsakey = RSA.import_key(private_key)
    # 将JSON数据转换为字符串
    data_str = json.dumps(data)
    hash_obj = SHA256.new(data_str.encode('utf-8'))
    signature = pkcs1_15.new(rsakey).sign(hash_obj)
    return signature


def verify_signature(secret, data, signature, alg):
    # key, json_data, signature, alg
    if alg == 'RS':
        rsakey = RSA.import_key(secret)
        # 将JSON数据转换为字符串
        data_str = json.dumps(data)
        hash_obj = SHA256.new(data_str.encode('utf-8'))
        try:
            pkcs1_15.new(rsakey).verify(hash_obj, signature)
            print("Signature is valid. Transmitted data:", data)
            return True
        except (ValueError, TypeError):
            print("Signature is invalid.")
            return False
    elif alg == 'HS':
        hash_object = hashlib.sha256()
        data_bytes = (json.dumps(data) + secret.decode()).encode('utf-8')
        print(data_bytes)
        hash_object.update(data_bytes)
        hex_dig = hash_object.hexdigest()
        if hex_dig == signature.decode():
            return True
    else:
        return False


def data_encode(data, alg):
    if alg not in ['HS', 'RS']:
        raise "Algorithm must be HS or RS!"
    else:
        private_key, public_key = generate_keys()
        if alg == 'RS':
            signature = sign_data(private_key, data)
            data_bytes = json.dumps(data).encode('utf-8')
            encoded_data1 = base64.b64encode(data_bytes)  # data
            encoded_data2 = base64.b64encode(signature)  # signature
            print(encoded_data2)
            encoded_data3 = base64.b64encode(alg.encode('utf-8'))  # alg
            encoded_data4 = base64.b64encode(public_key)  # public_key
            encoded_data = encoded_data1.decode() + '.' + encoded_data2.decode() + '.' + encoded_data3.decode() + '.' + encoded_data4.decode()
            print("The encoded data is: ", encoded_data)
            return encoded_data
        else:
            hash_object = hashlib.sha256()
            data_bytes = (json.dumps(data) + secret).encode('utf-8')
            inputdata = json.dumps(data).encode('utf-8')
            hash_object.update(data_bytes)
            hex_dig = hash_object.hexdigest()
            signature = base64.b64encode(hex_dig.encode('utf-8'))
            encoded_data1 = base64.b64encode(inputdata)  # data
            encoded_data3 = base64.b64encode(alg.encode('utf-8'))  # alg
            encoded_data = encoded_data1.decode() + '.' + signature.decode() + '.' + encoded_data3.decode()
            print("The encoded data is: ", encoded_data)
            return encoded_data


def data_decode(encode_data):
    try:
        all_data = encode_data.split('.')
        sig_bytes = all_data[1].replace(' ', '+').encode('utf-8')
        print(sig_bytes)
        data = base64.b64decode(all_data[0].replace(' ', '+')).decode('utf-8')
        json_data = json.loads(data)
        signature = base64.b64decode(sig_bytes)
        alg = base64.b64decode(all_data[2]).decode('utf-8')
        key = secret
        if len(all_data) == 4: # self-defined key
            key_bytes = all_data[3].replace(' ', '+').encode('utf-8')
            key = base64.b64decode(key_bytes)  # bytes
        # 验证签名
        is_valid = verify_signature(key, json_data, signature, alg)
        if is_valid:
            return json_data
        else:
            return False
    except:
        raise "something error"


def read_html(filname):
    with open('./static/' + filname, 'r', encoding='utf-8') as file:
        # 读取文件内容
        html_content = file.read()
    return html_content
