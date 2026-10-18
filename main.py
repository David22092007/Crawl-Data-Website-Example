import hashlib
import base64
from requests import Session
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,en-US;q=0.9,en;q=0.8,ja;q=0.7,en-GB-oxendict;q=0.6',
    'access-control-allow-origin': '*',
    'brand': 'Chrome 155.0.0.0 Google Inc. vi Asia/Bangkok',
    'content-type': 'application/json',
    'currentlang': 'vi',
    'neutral': '0',
    'origin': 'https://hk-semsplus.goodwe.com',
    'os': 'Windows 10.0 desktop',
    'priority': 'u=1, i',
    'referer': 'https://hk-semsplus.goodwe.com/',
    'sec-ch-ua': '"Google Chrome";v="155", "Chromium";v="155", "Not(A:Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'token': '{"uid":"","timestamp":0,"token":"","client":"semsPlusWeb","version":"","language":"vi"}',
    'traceparent': '00-bc868d2158b12dff0a0ba1b09ebbbb1e-19625176dcf0d996-01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36',
    #'uuid': '25239440-3795-4cd7-998e-21043f1d0883',
    #'x-signature': 'Y2UzMzg1MGJhY2VkMGI2ZWE2OGJiNDA1NjI1ZmY4ZmI5OWM5MWNhNGRmYWJkZDNhNTJlMTgwZTQ1NzAxYWY3YkAxNzkyMzA2MzUzNDgy',
    #'cookie': '_gcl_au=1.1.447280268.1792248686; _ga=GA1.1.73672611.1792248687; _fbp=fb.1.1792248687277.957085597901943588; _ga_LMZCT1FQVJ=GS2.1.s1792248686$o1$g1$t1792248717$j29$l0$h916337173; _c_WBKFRo=iBSxj2TRkxHdC6MErCb7T6CCzqknieQbnazLbEfs; i18next=vi; _ga_ZRN08C42NP=GS2.1.s1792303376$o2$g1$t1792306344$j32$l0$h0',
}

def generate_login_pwd(password):
    md5_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    final_payload = base64.b64encode(md5_hash.encode('utf-8')).decode('utf-8')    
    return final_payload
json_data = {
    'account': 'hogiahuy99810@gmail.com',
    'pwd': generate_login_pwd("Huy@1234"),
    'agreement': 1,
    'isLocal': False,
    'isChinese': False,
}
s = Session()

# 2. Cập nhật headers mặc định cho toàn bộ session (tùy chọn nhưng khuyên dùng)
s.headers.update(headers)

# 3. Sử dụng s.post() thay vì gọi s(...) trực tiếp
response = s.post(
    'https://hk-semsplus.goodwe.com/web/sems/sems-user/api/v1/auth/cross-login',
    json=json_data,
)
headers=response.headers
print("Status Code:", response.status_code)
print("Response:", response.text)
if response.status_code == 200:
    try:
        response_json = response.json()
        real_token = response_json.get('data', {}).get('token', '')
        real_uid = response_json.get('data', {}).get('uid', '')
        
        if real_token:
            # Tạo chuỗi JSON cho header 'token' y như định dạng ban đầu nhưng có dữ liệu thật
            new_token_header = f'{{"uid":"{real_uid}","timestamp":0,"token":"{real_token}","client":"semsPlusWeb","version":"","language":"vi"}}'

            s.headers.update({
                'token': new_token_header
            })
            
            # 3. Tiến hành gọi API lấy data
            user_response = s.get('https://hk-gateway.semsportal.com/web/sems/sems-user/api/v1/user/get-user')
            print("User Data:", user_response.text)
        else:
            print("Không tìm thấy Token trong response đăng nhập.")
            
    except Exception as e:
        print("Lỗi parse JSON:", e)
else:
    print("Đăng nhập thất bại. Chắc chắn do thiếu hoặc sai x-signature!")
