import requests , threading , uuid , os , ctypes
from colorama import Fore , init
init(autoreset=True)
class InstagramSwapper:
    def __init__(self):
        self.sess = requests.session()
        self.attempts = 0
        self.green = Fore.LIGHTGREEN_EX
        self.red = Fore.LIGHTRED_EX
        self.reset = Fore.RESET
        self.yellow = Fore.LIGHTYELLOW_EX
        self.magenta = Fore.LIGHTMAGENTA_EX
        self.N = 0
        self.N2 = 0
        self.uuid = uuid.uuid4()
        self.headers_instagram_api = {
            "Host": "i.instagram.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 123.1.0.26.114 (iPhoneXR)",
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Connection-Type": "WIFI",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "keep-alive"
        }
    def http_request(self, url, headers, data=None, cookies=None, post=None, get=None):
        if post:
            if data and cookies:
                return requests.post(url, headers=headers, data=data, cookies=cookies)
            elif data and not cookies:
                return requests.post(url, headers=headers, data=data)
            elif cookies and not data:
                return requests.post(url, headers=headers, cookies=cookies)
        elif get:
            if data and cookies:
                return requests.get(url, headers=headers, data=data, cookies=cookies)
            elif data and not cookies:
                return requests.get(url, headers=headers, data=data)
            elif cookies and not data:
                return requests.get(url, headers=headers, cookies=cookies)
    def login(self, username_or_email, password):
        self.req_login = self.http_request('https://i.instagram.com/api/v1/accounts/login/', self.headers_instagram_api, {"_uuid": self.uuid, "password": password, "username": username_or_email, "device_id": username_or_email, "login_attempt_count":"0", "_csrftoken":"missing"}, False, True, False)
        if 'logged_in_user' in self.req_login.text:
            print(f'[{self.green}+{self.reset}] Successfully Login > @{username_or_email}')
            self.cookies_api = self.req_login.cookies
            self.get_info_account(self.cookies_api)
        elif 'cha' in self.req_login.text:
            self.secure(self.cookies_api, self.req_login.json(), username_or_email)
        else:
            print(f'{self.req_login.text}\n[{self.red}+{self.reset}] Press Enter To Exit')
            input()
            exit(0)
    def secure(self, cookies, request_login, username_or_email):
        self.challenge = request_login['challenge']['api_path']
        self.get_info_secure = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, False, cookies, False, True).json()
        try:
            self.email_secure = self.get_info_secure['step_data']['email']
        except:
            print(f'[{self.red}+{self.reset}] Not Found Email')
            self.email_secure = ''
        try:
            self.phone_number_secure = self.get_info_secure["step_data"]["phone_number"]
        except:
            print(f'[{self.red}+{self.reset}] Not Found Phone Number')
            self.phone_number_secure = ''
        if not self.email_secure == '' and not self.phone_number_secure == '':
            print(f'[{self.green}+{self.reset}] 1 - {self.email_secure}\n[{self.green}+{self.reset}] 2 : {self.phone_number_secure}')
            self.mode_choice = int(input())
            if self.mode_choice == 1:
                self.send_secure = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"choice": 1, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False).json()
                self.contact_point = self.send_secure['step_data']['contact_point']
                print(f'[{self.green}+{self.reset}] Successfully Send Code To {self.contact_point}')
                print(f'[{self.green}+{self.reset}] Code : ', end='')
                self.code = input()
                self.check_code = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"security_code": self.code, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False)
                if 'logged_in_user' in self.check_code.text:
                    self.cookies_api = self.check_code.cookies
                    print(f'[{self.green}+{self.reset}] Successfully Login > @{username_or_email}')
                    self.get_info_account(self.cookies_api)
                else:
                    print(f'{self.check_code.text}\n[{self.red}+{self.reset}] Press Enter To Exit')
                    input()
                    exit(0)
            elif self.mode_choice == 2:
                self.send_secure = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"choice": 2, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False).json()
                self.contact_point = self.send_secure['step_data']['contact_point']
                print(f'[{self.green}+{self.reset}] Successfully Send Code To {self.contact_point}')
                print(f'[{self.green}+{self.reset}] Code : ', end='')
                self.code = input()
                self.check_code = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"security_code": self.code, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False)
                if 'logged_in_user' in self.check_code.text:
                    self.cookies_api = self.check_code.cookies
                    print(f'[{self.green}+{self.reset}] Successfully Login > @{username_or_email}')
                    self.get_info_account(self.cookies_api)
                else:
                    print(f'{self.check_code.text}\n[{self.red}+{self.reset}] Press Enter To Exit')
                    input()
                    exit(0)
        elif not self.email_secure == '' and self.phone_number == '':
            self.send_secure = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"choice": 1, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False).json()
            self.contact_point = self.send_secure['step_data']['contact_point']
            print(f'[{self.green}+{self.reset}] Successfully Send Code To {self.contact_point}')
            print(f'[{self.green}+{self.reset}] Code : ', end='')
            self.code = input()
            self.check_code = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"security_code": self.code, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False)
            if 'logged_in_user' in self.check_code.text:
                self.cookies_api = self.check_code.cookies
                print(f'[{self.green}+{self.reset}] Successfully Login > @{username_or_email}')
                self.get_info_account(self.cookies_api)
            else:
                print(f'{self.check_code.text}\n[{self.red}+{self.reset}] Press Enter To Exit')
                input()
                exit(0)
        elif not self.phone_number == '' and self.email == '':
            self.send_secure = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"choice": 2, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False).json()
            self.contact_point = self.send_secure['step_data']['contact_point']
            print(f'[{self.green}+{self.reset}] Successfully Send Code To {self.contact_point}')
            print(f'[{self.green}+{self.reset}] Code : ', end='')
            self.code = input()
            self.check_code = self.http_request(f'https://i.instagram.com/api/v1{self.challenge}', self.headers_instagram_api, {"security_code": self.code, "_uuid": self.uuid, "_uid": self.uuid, "_csrftoken": "missing"}, cookies, True, False)
            if 'logged_in_user' in self.check_code.text:
                self.cookies_api = self.check_code.cookies
                print(f'[{self.green}+{self.reset}] Successfully Login > @{username_or_email}')
                self.get_info_account(self.cookies_api)
            else:
                print(f'{self.check_code.text}\n[{self.red}+{self.reset}] Press Enter To Exit')
                input()
                exit(0)
        else:
            exit(0)
    def get_info_account(self, cookies_api):
        self.cookies_api = cookies_api
        self.headers_instagram_web = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36", "x-csrftoken": self.cookies_api["csrftoken"], "x-ig-app-id": "936619743392459", "x-instagram-ajax": "0c15f4d7d44a", "x-requested-with": "XMLHttpRequest"}
        self.req_get_info = self.http_request('https://www.instagram.com/accounts/edit/?__a=1', self.headers_instagram_web, False, self.cookies_api, False, True).json()
        try:
            self.email = self.req_get_info["form_data"]["email"]
        except:
            print(f'[{self.red}+{self.reset}] Not Found Email')
            self.email = ''
        try:
            self.first_name = self.req_get_info["form_data"]["first_name"]
        except:
            print(f'[{self.red}+{self.reset}] Not Found First Name')
            self.first_name = ''
        try:
            self.phone_number = self.req_get_info["form_data"]["phone_number"]
        except:
            print(f'[{self.red}+{self.reset}] Not Found Phone Number')
            self.phone_number = ''
        print(f'[{self.green}+{self.reset}] Target : ', end='')
        self.target = input()
        print(f'[{self.green}+{self.reset}] Thread : ', end='')
        self.thread_n = int(input())
        ctypes.windll.user32.MessageBoxW(0, f'Click Ok To Start', 'Instagram Swapper', 0)
        self.threads = []
        for _ in range(self.thread_n * 10):
            self.thread_m = threading.Thread(target=self.swapper)
            self.thread_m.start()
            self.threads.append(self.thread_m)
    def swapper(self):
        while 1:
            try:
                self.request_swapper_set_username = self.sess.post('https://i.instagram.com/api/v1/accounts/set_username/', headers=self.headers_instagram_api, data={'username': self.target}, cookies=self.cookies_api, timeout=3).status_code
                if self.request_swapper_set_username == 200 and self.N == 0:
                    self.N = 1
                    print(f'\n[{self.green}+{self.reset}] Successfully Swapped : @{self.target}')
                    ctypes.windll.user32.MessageBoxW(0, f'Successfully Swapped : @{self.target}', 'Instagram Swapper', 0)
                    input()
                    exit(0)
                elif self.request_swapper_set_username == 429 and self.N == 0:
                    self.N = 1
                    print(f'\n[{self.red}+{self.reset}] Spam On Set Username')
                elif self.request_swapper_set_username == 400 and self.N == 0:
                    self.attempts +=1
                    print(f'\r[1] Attempts : {self.attempts}', end='')
                self.request_swapper_web = self.sess.post('https://www.instagram.com/accounts/edit/', headers=self.headers_instagram_web, data={"first_name": self.first_name, "email": self.email, "username": self.target, "phone_number": self.phone_number, "biography": 'Successfully Swapped', "external_url": "", "chaining_enabled": "on"}, cookies=self.cookies_api, timeout=3).status_code
                if self.request_swapper_web == 200 and self.N2 == 0:
                    self.N2 = 1
                    print(f'\n[{self.green}+{self.reset}] Successfully Swapped : @{self.target}')
                    ctypes.windll.user32.MessageBoxW(0, f'Successfully Swapped : @{self.target}', 'Instagram Swapper', 0)
                    input()
                    exit(0)
                elif self.request_swapper_web == 400 and self.N2 == 0:
                    self.attempts +=1
                    print(f'\r[2] Attempts : {self.attempts}', end='')
            except:
                pass
if __name__ == '__main__':
    os.system("cls")
    i = InstagramSwapper()
    print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Username Or Email : ', end='')
    username_or_email = input()
    print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Password : ', end='')
    password = input()
    i.login(username_or_email, password)
