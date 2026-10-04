# Auto-generated obfuscated build (do not edit)
_SEC_SALT = 2715234182

def _sec_string(enc, _s=_SEC_SALT):
    import base64 as _b64
    try:
        _b = _b64.b64decode(str(enc).encode("ascii"))
        _k = (_s & 0xffffffff).to_bytes(4, "big")
        _out = bytearray()
        for _i in range(len(_b)):
            _out.append(_b[_i] ^ _k[_i & 3])
        return bytes(_out).decode("utf-8", errors="replace")
    except Exception:
        return ""

"""
V5 SHIMUL SNI FINDER SCRIPT 2026 PREMIUM
Updated with:
- UNLIMITED SCANN_NO FREEZE (Option 8)
- CREATE FILE FORMAT FOR ANTI DPI (Option 11)
- Responsive main menu UI
- Fixed datetime error in Option 8
- Fixed Option 2 back-to-menu handling
- Fixed Option 4 multiprocessing crash (ThreadPoolExecutor)
"""
import asyncio
import aiohttp
import ipaddress
import ssl
import socket
import re
import pyperclip
import shutil
import time
import sys
import json
from colorama import init, Fore, Style
from tqdm import tqdm
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
import os
import multithreading
import websocket
import subprocess
from colorama import Fore, Style, init
try:
    import pycurl
except Exception:
    pycurl = None
from io import BytesIO
import subprocess
import signal
from termcolor import colored
import math
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
import urllib.parse
from collections import OrderedDict, deque
import platform
import threading
import queue
import select
from dataclasses import dataclass, field
init(autoreset=True)
RESULTS_FILE = 'V4.txt'
STATE_FILE = 'scan_state.json'

def handle_sigint(signal, frame):
    print(f'{Fore.RED}\nProgram interrupted. Exiting gracefully...{Style.RESET_ALL}')
    sys.exit(0)
signal.signal(signal.SIGINT, handle_sigint)

def get_build_prop_info():
    try:
        cmd = 'getprop'
        output = subprocess.check_output(cmd, shell=True).decode()
        props = {}
        for line in output.split('\n'):
            if '[ro.serialno]' in line or '[ro.product.model]' in line or '[ro.product.brand]' in line:
                key = line.split('[')[1].split(']')[0]
                value = line.split('[')[2].split(']')[0]
                props[key] = value
        return props
    except:
        return {}

def get_cpu_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[1].strip()
    except:
        return ''

def get_device_id():
    identifiers = []
    build_props = get_build_prop_info()
    for key in sorted(build_props.keys()):
        identifiers.append(str(build_props[key]))
    try:
        cmd = 'settings get secure android_id'
        android_id = subprocess.check_output(cmd, shell=True).decode().strip()
        identifiers.append(android_id)
    except:
        pass
    cpu_serial = get_cpu_serial()
    if cpu_serial:
        identifiers.append(cpu_serial)
    if not identifiers:
        system_files = ['/sys/class/android_usb/android0/iSerial', '/sys/class/net/wlan0/address', '/sys/class/net/eth0/address']
        for file_path in system_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        identifiers.append(content)
            except:
                continue
    device_string = '|'.join([str(x) for x in identifiers if x])
    if not device_string:
        device_string = 'fallback_identifier'
    device_hash = hashlib.sha256(device_string.encode()).hexdigest()
    formatted_id = '-'.join([device_hash[i:i + 4] for i in range(0, 16, 4)])
    return formatted_id.upper()
SERVER_DAYS_REMAINING = 36500  # Lifetime mode for this owner-controlled build

def days_remaining():
    return SERVER_DAYS_REMAINING

def _format_days():
    d = days_remaining()
    if d >= 36500:
        return '∞ LIFETIME'
    return str(d)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def append_to_v4(content):
    """Append results to V4.txt"""
    try:
        with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
    except Exception as e:
        print(f'{Fore.RED}Error writing to V4.txt: {e}{Style.RESET_ALL}')

async def fetch_status(session, url, semaphore):
    try:
        async with semaphore:
            async with session.get(url, timeout=2) as response:
                server = response.headers.get('Server', 'Unknown')
                return (response.status, server)
    except asyncio.TimeoutError:
        return (None, 'Timeout')
    except Exception as e:
        return (None, f'Error: {e}')

async def scan_ip(ip, total_ips, index, server_dict, semaphore):
    url = f'http://{ip}'
    async with aiohttp.ClientSession() as session:
        status, server = await fetch_status(session, url, semaphore)
        if status and status != 302 and ('Error' not in server):
            server_dict[ip] = (status, server)
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.flush()
            result_line = f'{Fore.GREEN}{ip}: {Fore.CYAN}{status} {Fore.MAGENTA}{server}'
            print(result_line)
            append_to_v4(result_line)
        scanned = index + 1
        progress = scanned / total_ips
        speed = scanned / (time.time() - start_time)
        progress_line = f'\rIPs scanned: {Fore.CYAN}{scanned}/{total_ips}{Style.RESET_ALL} ({progress * 100:.2f}%) - Speed: {Fore.CYAN}{speed:.2f} IPs/s{Style.RESET_ALL}'
        sys.stdout.write(progress_line)
        sys.stdout.flush()

async def scan_cidr_block(cidr_block):
    network = ipaddress.ip_network(cidr_block, strict=False)
    total_ips = network.num_addresses
    ips = network.hosts()
    server_dict = {}
    semaphore = asyncio.Semaphore(300)
    global start_time
    start_time = time.time()
    chunk_size = 1000
    ip_list = list(ips)
    print(f'{Fore.RED}{Style.BRIGHT}ACTIVE IPS ALIVE\n' + '-' * 20)
    for i in range(0, len(ip_list), chunk_size):
        chunk = ip_list[i:i + chunk_size]
        tasks = [scan_ip(str(ip), total_ips, i + j, server_dict, semaphore) for j, ip in enumerate(chunk)]
        await asyncio.gather(*tasks)
    end_time = time.time()
    duration = end_time - start_time
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    total_scanned = len(server_dict)
    speed = total_scanned / duration if duration > 0 else 0
    print(f'\n{Fore.YELLOW}Time taken for scanning: {duration:.2f} seconds')
    print(f'{Fore.YELLOW}Scanning speed: {Fore.CYAN}{speed:.2f} IPs per second{Style.RESET_ALL}')

async def scan_multiple_cidr_blocks(cidr_blocks):
    for cidr_block in cidr_blocks:
        try:
            ipaddress.ip_network(cidr_block, strict=False)
            print(f'\nScanning CIDR block: {cidr_block}')
            await scan_cidr_block(cidr_block)
        except ValueError:
            print(f"{Fore.RED}Invalid CIDR block '{cidr_block}'. Skipping.")

async def ip_scanner():
    clear_screen()
    title = f'{Fore.RED}{Style.BRIGHT}SHIMUL IP SCANNER V5 UPDATED  {Style.RESET_ALL}'
    subtitle = f'{Fore.CYAN}CREATOR TELEGRAM: @shimul00889{Style.RESET_ALL}'
    logo = f'{Fore.RED}{Style.BRIGHT}DEVELOPER IS NOT RESPONSIBLE FOR ANY HARM TO YOUR NETWORK\n' + '░░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄░░░░░░░\n' + '░░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄░░░░\n' + '░░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█░░░\n' + '░░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░░█░░\n' + '░▄▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░░█░\n' + '█░▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒░█\n' + '█░▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█\n' + '░█░▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█░\n' + '░░█░░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█░░\n' + '░░░█░░░░██░░▀█▄▄▄█▄▄█▄████░█░░░\n' + '░░░░█░░░░▀▀▄░█░░░█░█▀██████░█░░\n' + '░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█░░\n' + '░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░▒░░░█░\n' + '░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░░░░█░\n' + '░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░░░░█░░\n' + f'{Style.RESET_ALL}'
    print(title)
    print(subtitle)
    print(logo)
    while True:
        cidr_input = input('Enter IP CIDR blocks (e.g., 192.167.0.0/16,192.168.0.0/16): ')
        cidr_blocks = [cidr.strip() for cidr in cidr_input.split(',')]
        await scan_multiple_cidr_blocks(cidr_blocks)
        continue_scanning = input('Do you want to scan more CIDR blocks? (yes/no): ').strip().lower()
        if continue_scanning != 'yes':
            print('Exiting the scanner.')
            break

class HostnameTracker:

    def __init__(self):
        self.hostnames = OrderedDict()
        self.count = 0
        self.lock = threading.Lock()

    def add(self, hostname):
        hostname_hash = hashlib.md5(hostname.encode()).hexdigest()
        with self.lock:
            if hostname_hash not in self.hostnames:
                self.hostnames[hostname_hash] = hostname
                self.count += 1
                return True
            return False

    def get_hostnames(self):
        return list(self.hostnames.values())

class RateLimiter:

    def __init__(self, max_workers):
        self.last_request_time = 0
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(max_workers)

    def wait(self):
        with self.semaphore:
            with self.lock:
                elapsed = time.time() - self.last_request_time
                if elapsed < 1.0:
                    time.sleep(1.0 - elapsed)
                self.last_request_time = time.time()

class ReverseIPScannerV2:

    def __init__(self):
        self.session = self._create_session()
        self.rate_limiter = RateLimiter(5)
        self.results = {}
        self.failed_ips = {}
        self.hostname_tracker = HostnameTracker()
        self.scanned_ips = 0
        self.lock = threading.Lock()
        self.progress = 0
        self.running = False
        self.error_log = None

    def _create_session(self):
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9'})
        adapter = requests.adapters.HTTPAdapter(max_retries=10, pool_connections=5, pool_maxsize=5)
        session.mount('https://', adapter)
        return session

    def scan_ip(self, ip):
        retries = 10
        backoff = 1
        ip_str = str(ip)
        while retries > 0:
            try:
                self.rate_limiter.wait()
                url = f'https://rapiddns.io/sameip/{urllib.parse.quote(ip_str)}'
                response = self.session.get(url, timeout=20)
                response.raise_for_status()
                if 'blocked' in response.text.lower() or 'captcha' in response.text.lower():
                    with self.lock:
                        if self.error_log:
                            self.error_log.write(f'[{datetime.datetime.now()}] Warning: Blocked/captcha for {ip_str}, retries left: {retries}\n')
                    retries -= 1
                    backoff = min(backoff * 2, 16)
                    time.sleep(2 * backoff)
                    continue
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', {'id': 'table'})
                if not table:
                    return []
                hostnames = []
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        hostname = cols[0].get_text(strip=True)
                        if hostname:
                            hostnames.append(hostname)
                return hostnames
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    backoff = min(backoff * 2, 16)
                    with self.lock:
                        if self.error_log:
                            self.error_log.write(f'[{datetime.datetime.now()}] Rate limit hit for {ip_str}\n')
                else:
                    with self.lock:
                        if self.error_log:
                            self.error_log.write(f'[{datetime.datetime.now()}] HTTP Error for {ip_str}: {str(e)}\n')
            except Exception as e:
                with self.lock:
                    if self.error_log:
                        self.error_log.write(f'[{datetime.datetime.now()}] Error for {ip_str}: {str(e)}\n')
            retries -= 1
            if retries > 0:
                backoff = min(backoff * 2, 16)
                time.sleep(2 * backoff)
        with self.lock:
            if ip_str not in self.failed_ips:
                self.failed_ips[ip_str] = 0
            self.failed_ips[ip_str] += 1
        return []

    def scan_batch(self, ip_list, output_file, start_idx):
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_ip = {executor.submit(self.scan_ip, ip): ip for ip in ip_list}
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    hostnames = future.result()
                    ip_str = str(ip)
                    if hostnames:
                        with self.lock:
                            self.results[ip_str] = hostnames
                        with open(output_file, 'a', encoding='utf-8') as f:
                            for hostname in hostnames:
                                if self.hostname_tracker.add(hostname):
                                    f.write(f'{hostname}\n')
                    with self.lock:
                        self.scanned_ips += 1
                        self.progress = start_idx + ip_list.index(ip) + 1
                        if ip_str in self.failed_ips and hostnames:
                            del self.failed_ips[ip_str]
                except Exception as e:
                    ip_str = str(ip)
                    with self.lock:
                        if ip_str not in self.failed_ips:
                            self.failed_ips[ip_str] = 0
                        self.failed_ips[ip_str] += 1

    def start_scan(self, ip_or_cidr, output_file):
        self.running = True
        try:
            self.error_log = open('scan_errors.log', 'a')
            ip_inputs = [x.strip() for x in ip_or_cidr.split(',')]
            ip_list = []
            for input_item in ip_inputs:
                try:
                    network = ipaddress.ip_network(input_item, strict=False)
                    if network.num_addresses > 1:
                        ip_list.extend(list(network.hosts()))
                    else:
                        ip_list.append(network.network_address)
                except ValueError:
                    ip_list.append(ipaddress.ip_address(input_item))
            total_ips = len(ip_list)
            attempt = 1
            MAX_TOTAL_ATTEMPTS = 3
            BATCH_SIZE = 256
            while ip_list and attempt <= MAX_TOTAL_ATTEMPTS:
                current_ip_list = ip_list[:]
                ip_list = []
                for i in range(0, len(current_ip_list), BATCH_SIZE):
                    batch = current_ip_list[i:i + BATCH_SIZE]
                    self.scan_batch(batch, output_file, i)
                    if not self.running:
                        break
                with self.lock:
                    ip_list = [ipaddress.ip_address(ip) for ip, count in self.failed_ips.items() if count < 10 * MAX_TOTAL_ATTEMPTS]
                attempt += 1
                time.sleep(2)
            return total_ips
        except Exception as e:
            print(f'{Fore.RED}Scan error: {str(e)}{Style.RESET_ALL}')
            return 0
        finally:
            self.running = False
            if self.error_log:
                self.error_log.close()

async def reverse_ip_scanner_v2():
    clear_screen()
    print(f'{Fore.YELLOW}V4 REVERSE IP Scanner{Style.RESET_ALL}')
    print(f'{Fore.CYAN}Telegram: @shimul00889{Style.RESET_ALL}')
    while True:
        ip_input = input(f"{Fore.CYAN}Enter IP or CIDR block (e.g., 1.2.3.4 or 1.2.3.0/24, multiple separated by commas, or 'back'): {Style.RESET_ALL}").strip()
        if ip_input.lower() in ['back', 'exit', 'quit', 'q']:
            return
        output_file = input(f"{Fore.CYAN}Enter output file name (e.g., results.txt, or 'back'): {Style.RESET_ALL}").strip()
        if output_file.lower() in ['back', 'exit', 'quit', 'q']:
            return
        if not output_file:
            output_file = 'reverse_results.txt'
        if os.path.exists(output_file):
            os.remove(output_file)
        if os.path.exists('scan_errors.log'):
            os.remove('scan_errors.log')
        print(f'\n{Fore.GREEN}Starting scan...{Style.RESET_ALL}')
        scanner = ReverseIPScannerV2()
        start_time = time.time()
        scan_thread = threading.Thread(target=scanner.start_scan, args=(ip_input, output_file))
        scan_thread.daemon = True
        scan_thread.start()
        total_ips = 0
        try:
            ip_inputs = [x.strip() for x in ip_input.split(',')]
            for input_item in ip_inputs:
                try:
                    network = ipaddress.ip_network(input_item, strict=False)
                    total_ips += len(list(network.hosts())) if network.num_addresses > 1 else 1
                except ValueError:
                    total_ips += 1
        except:
            total_ips = 1
        try:
            with tqdm(total=total_ips, desc=f'{Fore.CYAN}Scanning IPs{Style.RESET_ALL}', bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.CYAN, Style.RESET_ALL)) as pbar:
                last_progress = 0
                while scanner.running or scanner.scanned_ips < total_ips:
                    with scanner.lock:
                        current_progress = scanner.progress
                        failed_count = len(scanner.failed_ips)
                    if current_progress > last_progress:
                        pbar.update(current_progress - last_progress)
                        last_progress = current_progress
                    pbar.set_postfix({'Hostnames': scanner.hostname_tracker.count, 'Failed': failed_count})
                    time.sleep(0.1)
                pbar.update(scanner.scanned_ips - last_progress)
        except Exception as e:
            print(f'{Fore.RED}Progress display error: {e}{Style.RESET_ALL}')
        elapsed = time.time() - start_time
        print(f'{Fore.GREEN}\nScan completed in {elapsed:.2f} seconds{Style.RESET_ALL}')
        print(f'{Fore.GREEN}Total unique hostnames found: {scanner.hostname_tracker.count}{Style.RESET_ALL}')
        if scanner.failed_ips:
            print(f'{Fore.YELLOW}Warning: {len(scanner.failed_ips)} IPs failed to scan{Style.RESET_ALL}')
        while True:
            choice = input(f'\n{Fore.YELLOW}1. Scan another\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
            if choice == '1':
                break
            elif choice == '2':
                return
            else:
                print(f'{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}')

def extract_root_domain(user_input):
    try:
        clean = re.sub('^.*://|/.*$|:.*$|@.*$', '', user_input)
        parts = clean.lower().split('.')
        second_level_domains = {'co', 'com', 'org', 'net', 'gov', 'edu', 'ac', 'go', 'mil', 'ne', 'or', 'nic', 'biz', 'info', 'name', 'pro', 'sch', 'web', 'tv', 'police', 'plc', 'ltd', 'inc', 'school', 'university', 'aero', 'post', 'tel', 'int', 'arpa', 'asia', 'app', 'blog', 'shop', 'club', 'dev', 'site', 'store', 'tech', 'press', 'ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st', 'su', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 'za', 'zm', 'zw', 'go.ke', 'co.ke'}
        if len(parts) >= 3:
            tld = parts[-1]
            sld = parts[-2]
            if len(tld) == 2 and sld in second_level_domains:
                return '.'.join(parts[-3:])
            if len(tld) == 2:
                return '.'.join(parts[-2:])
        country_tld_patterns = [('\\.co\\.([a-z]{2})$', 3), ('\\.ac\\.([a-z]{2})$', 3), ('\\.gov\\.([a-z]{2})$', 3), ('\\.edu\\.([a-z]{2})$', 3), ('\\.org\\.([a-z]{2})$', 3), ('\\.net\\.([a-z]{2})$', 3), ('\\.com\\.([a-z]{2})$', 3)]
        clean_lower = clean.lower()
        for pattern, keep_parts in country_tld_patterns:
            if re.search(pattern, clean_lower):
                return '.'.join(parts[-keep_parts:])
        if len(parts) > 2:
            return '.'.join(parts[-2:])
        return clean
    except:
        return None

def query_crtsh(domain):
    url = f'https://crt.sh/?q=%.{domain}&output=json'
    subdomains = set()
    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            for entry in response.json():
                names = entry.get('name_value', '')
                for name in re.split('\\n|,|\\t', names):
                    name = re.sub('^\\*\\.?', '', name.strip().lower())
                    if re.fullmatch('^([a-z0-9-]+\\.)*[a-z]{2,}$', name):
                        if name.endswith(domain) or name == domain:
                            subdomains.add(name)
    except:
        pass
    return subdomains

async def tls_scanner():
    clear_screen()
    print(colored('\n┌──────────────────────────────────────────────────────┐            \n│      ┌──────────────────────────────────────────┐    │            \n│  ┌───┼─────                                     ┼────┼            \n┼──┼───┼─SUBDOMAIN G- MASTER GENERATOR            │    │            \n│  │   │                                          │    ┼─────┐      \n│  │   │ │NOTE IT SUPPORTS FILE.TXT & HOSTNAME INPUT   │     │      \n┼──┼───┼─┘      ┌─   │                            │    │     │      \n│  ├───┼────────┼───►│SHIMUL MASTERS TOOL V5    ┼────┼     │      \n│  │   │        │    │                            │    │     │      \n│      │        │    │                            │    │     │      \n│      │        │   ┌────────────────────────────────────────▼─────┐\n│      │        │   │ OWNER @SHIMUL https://t.me/shimul00889│\n└──────│────────┴───│─────────────────────────────│────┘           │\n       │            └──────────────────────────────────────────────┘\n       └──────────────────────────────────────────┘                 \n', 'cyan', attrs=['bold']))
    while True:
        target = input(colored('\n[?] Enter domain/file (q to quit): ', 'yellow')).strip()
        if target.lower() in ('q', 'quit'):
            break
        if os.path.isfile(target):
            domains = []
            try:
                with open(target, 'r') as f:
                    for line in f:
                        domain = extract_root_domain(line.strip())
                        if domain and re.match('^([a-z0-9-]+\\.)+[a-z]{2,}$', domain):
                            domains.append(domain)
            except Exception as e:
                print(colored(f'[!] File error: {str(e)}', 'red'))
                continue
            if not domains:
                print(colored('[-] No valid domains in file', 'red'))
                continue
            total = len(domains)
            print(colored(f'\n[+] Scanning {total} domains...', 'blue'))
            all_subs = set()
            for idx, domain in enumerate(domains, 1):
                sys.stdout.write(f'\rProcessing {idx}/{total} ({idx / total * 100:.1f}%)')
                sys.stdout.flush()
                all_subs.update(query_crtsh(domain))
            sys.stdout.write('\n')
            if not all_subs:
                print(colored('[-] No subdomains found', 'red'))
                continue
            filename = input(colored('[?] Save to file (e.g., subs.txt): ', 'yellow')).strip()
            if not filename:
                filename = 'subdomains.txt'
            try:
                with open(filename, 'w') as f:
                    f.write('\n'.join(sorted(all_subs)))
                print(colored(f'\n[+] Results saved to {filename}', 'green'))
            except Exception as e:
                print(colored(f'[!] Save error: {str(e)}', 'red'))
        else:
            domain = extract_root_domain(target)
            if not domain or not re.match('^([a-z0-9-]+\\.)+[a-z]{2,}$', domain):
                print(colored('[!] Invalid domain format', 'red'))
                continue
            print(colored(f'\n[+] Scanning {domain}...', 'blue'))
            results = query_crtsh(domain)
            if not results:
                print(colored('[-] No subdomains found', 'red'))
                continue
            filename = input(colored('[?] Save to file (e.g., output.txt): ', 'yellow')).strip()
            if not filename:
                filename = f"{domain.replace('.', '_')}_subs.txt"
            try:
                with open(filename, 'w') as f:
                    f.write('\n'.join(sorted(results)))
                print(colored(f'\n[+] Results saved to {filename}', 'green'))
            except Exception as e:
                print(colored(f'[!] Save error: {str(e)}', 'red'))
CYAN = '\x1b[96m'
MAGENTA = '\x1b[95m'
BOLD = '\x1b[1m'
DIM = '\x1b[2m'
RESET = '\x1b[0m'
TITLE = f'{CYAN}\n _   _  ___  ____ _____ _   _    _    __  __ _____\n| | | |/ _ \\/ ___|_   _| \\ | |  / \\  |  \\/  | ____|\n| |_| | | | \\___ \\ | | |  \\| | / _ \\ | |\\/| |  _|\n|  _  | |_| |___) || | | |\\  |/ ___ \\| |  | | |___\n|_| |_|\\___/|____/ |_| |_| \\_/_/   \\_\\_|  |_|_____\n / _| / _ \\  / \\  | \\ | | \\ | | ____|  _ \\   _| || |_\n \\___ \\| | | |/ _ \\ |  \\| |  \\| |  _| | |_) | |_  ..  _|\n ___) | |_| / ___ \\| |\\  | |\\  | |___|  _ <  |_      _|\n|____/ \\___/_/   \\_\\_| \\_|_| \\_|_____|_| \\_\\   |_||_|\n{RESET}'
SERVER_DB = [('cloudflare', 'Cloudflare'), ('nginx', 'NGINX'), ('apache', 'Apache'), ('cloudfront', 'CloudFront'), ('akamai', 'Akamai'), ('microsoft-iis', 'IIS'), ('tengine', 'Tengine'), ('fastly', 'Fastly'), ('bunny', 'BunnyCDN'), ('amsel', 'Amselweb'), ('openresty', 'OpenResty'), ('litespeed', 'LiteSpeed'), ('caddy', 'Caddy'), ('vercel', 'Vercel'), ('heroku', 'Heroku'), ('gunicorn', 'Gunicorn'), ('uwsgi', 'uWSGI'), ('tomcat', 'Tomcat'), ('jetty', 'Jetty'), ('node', 'Node.js'), ('express', 'Express'), ('haproxy', 'HAProxy'), ('varnish', 'Varnish'), ('squid', 'Squid'), ('caddy', 'Caddy'), ('netlify', 'Netlify'), ('sucuri', 'Sucuri'), ('incapsula', 'Incapsula'), ('f5-bigip', 'F5 BIG-IP'), ('zope', 'Zope'), ('webrick', 'WEBrick'), ('puma', 'Puma'), ('unicorn', 'Unicorn'), ('kestrel', 'Kestrel'), ('lighttpd', 'Lighttpd')]

def detect_server(headers):
    if 'cf-ray' in headers:
        return 'Cloudflare'
    if 'x-vercel-id' in headers:
        return 'Vercel'
    server_header = headers.get('server', '').lower()
    for pattern, name in SERVER_DB:
        if pattern in server_header:
            return name
    via_header = headers.get('via', '').lower()
    for pattern, name in SERVER_DB:
        if pattern in via_header:
            return f'{name} (Via)'
    return 'Unknown'

def check_host(hostname):
    if pycurl is None:
        return None
    c = pycurl.Curl()
    try:
        c.setopt(c.URL, f'http://{hostname}')
        c.setopt(c.TIMEOUT, 2)
        c.setopt(c.CONNECTTIMEOUT, 1)
        c.setopt(c.NOBODY, True)
        headers = []
        c.setopt(c.HEADERFUNCTION, headers.append)
        c.perform()
        header_dict = {}
        for h in headers:
            if b':' in h:
                k, v = h.decode('latin-1').split(':', 1)
                header_dict[k.strip().lower()] = v.strip()
        status = c.getinfo(c.RESPONSE_CODE)
        if status == 302:
            return None
        return (hostname, status, detect_server(header_dict))
    except pycurl.error as e:
        return None if e.args and e.args[0] in [6, 7, 28, 35, 56] else (hostname, 'Error', 'Unknown')
    finally:
        c.close()

async def file_scanner():
    while True:
        clear_screen()
        print(TITLE)
        try:
            filename = input("Enter path to file with hostnames (or 'back'): ").strip()
            if filename.lower() in ['back', 'exit', 'quit', 'q']:
                return
            if not os.path.exists(filename):
                print(f"{Fore.RED}Error: File '{filename}' not found.{Style.RESET_ALL}")
                choice = input(f'{Fore.YELLOW}1. Try again\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
                if choice == '2':
                    return
                continue
            with open(filename, 'r') as f:
                hostnames = list({line.strip() for line in f if line.strip()})
                total = len(hostnames)
                if not total:
                    print(f'{Fore.YELLOW}No valid hostnames found in file.{Style.RESET_ALL}')
                    choice = input(f'{Fore.YELLOW}1. Try another file\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
                    if choice == '2':
                        return
                    continue
                print(f'\n{BOLD}Scanning {total} hosts (with server detection){RESET}\n')
                start_time = time.time()
                processed = 0
                found = 0
                lock = threading.Lock()

                def update_progress(result=None, error_msg=None):
                    nonlocal processed, found
                    with lock:
                        processed += 1
                        elapsed = time.time() - start_time
                        speed = processed / elapsed if elapsed > 0 else 0
                        sys.stdout.write('\r\x1b[K')
                        if result:
                            host, status, server = result
                            result_line = f'{CYAN}{host}{RESET}: {MAGENTA}{status}{RESET} [{MAGENTA}{server}{RESET}]'
                            sys.stdout.write(f'{result_line}\n')
                            append_to_v4(result_line)
                            found += 1
                        if error_msg:
                            sys.stdout.write(f'\r{DIM}Progress: {processed}/{total} | {speed:.1f}/s | Found: {found} | Err: {error_msg[:25]}{RESET}')
                        else:
                            sys.stdout.write(f'\r{DIM}Progress: {processed}/{total} | {speed:.1f}/s | Found: {found}{RESET}')
                        sys.stdout.flush()
                max_workers = min(50, (os.cpu_count() or 2) * 4)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_host = {executor.submit(check_host, hostname): hostname for hostname in hostnames}
                    for future in as_completed(future_to_host):
                        try:
                            result = future.result()
                            update_progress(result=result)
                        except Exception as e:
                            update_progress(error_msg=str(e))
                sys.stdout.write('\r\x1b[K')
                elapsed = time.time() - start_time
                print(f'\n{DIM}Completed in {elapsed:.1f}s | Found: {found} active hosts{RESET}')
        except KeyboardInterrupt:
            print(f'\n{Fore.YELLOW}Scan interrupted by user.{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}')
        while True:
            print(f'\n{Fore.CYAN}Options:{Style.RESET_ALL}')
            print(f'{Fore.GREEN}1. Scan another file{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}2. Return to main menu{Style.RESET_ALL}')
            choice = input(f'{Fore.CYAN}Enter your choice (1-2): {Style.RESET_ALL}').strip()
            if choice == '1':
                break
            elif choice == '2':
                return
            else:
                print(f'{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}')
title_proxy = f'{Fore.RED}{Style.BRIGHT}PROXY  SCANNER SHIMUL - V5 MASTERS {Style.RESET_ALL}'
subtitle_proxy = f'{Fore.CYAN}CREATOR TELEGRAM: @shimul00889{Style.RESET_ALL}'
title_v2 = f'{Fore.RED}\x1b[1VERSION 4 🆂🅲🅰🅽🅽🅴🆁\x1b[0m{Style.RESET_ALL}'
subtitle_v2 = f'{Fore.BLUE}₮ɆⱠɆ₲Ɽ₳₥ ₲ⱤØɄ₱: https://t.me/shimul00889{Style.RESET_ALL}'
owner_proxy = f'{Fore.CYAN}O҉W҉N҉E҉R҉: https://t.me/shimul00889{Style.RESET_ALL}'
logo_proxy = f'\n    {Fore.RED}\x1b[1m\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠃⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⢛⠒⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣄⡈⠓⢄⠠⡀⠀⠀⠀⣄⣷⠀⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣷⠀⠈⠱⡄⠑⣌⠆⠀⠀⡜⢻⠀⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠳⡆⠐⢿⣆⠈⢿⠀⠀⡇⠘⡆⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣷⡇⠀⠀⠈⢆⠈⠆⢸⠀⠀⢣⠀⠀⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠈⢂⠀⡇⠀⠀⢨⠓⣄⠀⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣦⣤⠖⡏⡸⠀⣀⡴⠋⠀⠈⠢⡀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠁⣹⣿⣿⣿⣷⣾⠽⠖⠊⢹⣀⠄⠀⠀⠀⠈⢣⡀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⣇⣰⢫⢻⢉⠉⠀⣿⡆⠀⠀⡸⡏⠀⠀⠀⠀⠀⠀⢇\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡇⡇⠈⢸⢸⢸⠀⠀⡇⡇⠀⠀⠁⠻⡄⡠⠂⠀⠀⠀⠘\n    ⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠓⡇⠀⠸⡆⢸⠀⢠⣿⠀⠀⠀⠀⣰⣿⣵⡆⠀⠀⠀⠀\n    ⠈⢻⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣦⣀⡇⠀⢧⡇⠀⠀⢺⡟⠀⠀⠀⢰⠉⣰⠟⠊⣠⠂⠀⡸\n    ⠀⠀⢻⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢧⡙⠺⠿⡇⠀⠘⠇⠀⠀⢸⣧⠀⠀⢠⠃⣾⣌⠉⠩⠭⠍⣉⡇\n    ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣋⠀⠈⠀⡳⣧⠀⠀⠀⠀⠀⢸⡏⠀⠀⡞⢰⠉⠉⠉⠉⠉⠓⢻⠃\n    ⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⢀⣀⠠⠤⣤⣤⠤⠞⠓⢠⠈⡆⠀⢣⣸⣾⠆⠀⠀⠀⠀⠀⢀⣀⡼⠁⡿⠈⣉⣉⣒⡒⠢⡼⠀\n    ⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣎⣽⣶⣤⡶⢋⣤⠃⣠⡦⢀⡼⢦⣾⡤⠚⣟⣁⣀⣀⣀⣀⠀⣀⣈⣀⣠⣾⣅⠀⠑⠂⠤⠌⣩⡇⠀\n    ⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣺⢁⣞⣉⡴⠟⡀⠀⠀⠀⠁⠸⡅⠀⠈⢷⠈⠏⠙⠀⢹⡛⠀⢉⠀⠀⠀⣀⣀⣼⡇⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡟⢡⠖⣡⡴⠂⣀⣀⣀⣰⣁⣀⣀⣸⠀⠀⠀⠀⠈⠁⠀⠀⠈⠀⣠⠜⠋⣠⠁⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢿⣿⣿⣷⡟⢋⣥⣖⣉⠀⠈⢁⡀⠤⠚⠿⣷⡦⢀⣠⣀⠢⣄⣀⡠⠔⠋⠁⠀⣼⠃⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⠈⠻⣿⣿⢿⣛⣩⠤⠒⠉⠁⠀⠀⠀⠀⠀⠉⠒⢤⡀⠉⠁⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣤⣤⠴⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠤⠀⠀⠀⠀⠀⢩⠇⠀⠀⠀\n    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n    ' + '\x1b[0m'

def display_banner():
    print(logo_proxy)
    print(title_proxy.center(80))
    print(subtitle_proxy.center(80))
    print(title_v2.center(80))
    print(subtitle_v2.center(80))
    print(owner_proxy.center(80))
    print('\n' + '=' * 80 + '\n')

class BugScanner(multithreading.MultiThreadRequest):
    threads: int

    def request_connection_error(self, *args, **kwargs):
        return 1

    def request_read_timeout(self, *args, **kwargs):
        return 1

    def request_timeout(self, *args, **kwargs):
        return 1

    def convert_host_port(self, host, port):
        return host + (f':{port}' if port not in ['80', '443'] else '')

    def get_url(self, host, port, uri=None):
        port = str(port)
        protocol = 'https' if port == '443' else 'http'
        return f'{protocol}://{self.convert_host_port(host, port)}' + (f'/{uri}' if uri is not None else '')

    def init(self):
        self._threads = getattr(self, '_threads', 30)
        self._threads = self.threads or self._threads

    def complete(self):
        pass

class DirectScanner(BugScanner):
    method_list = []
    host_list = []
    port_list = []
    isp_redirects = ['http://safaricom.zerod.live/?c=77', 'http://91.220.208.30', 'https://jio.com/BalanceExhaust', 'https://portal.ncnd.vodacom.co.tz']

    def log_info(self, **kwargs):
        for x in ['status_code', 'server']:
            kwargs[x] = kwargs.get(x, '')
        location = kwargs.get('location')
        if location:
            if location.startswith(f"https://{kwargs['host']}"):
                kwargs['status_code'] = f"{kwargs['status_code']:<4}"
            else:
                kwargs['host'] += f' -> {location}'
        messages = []
        base_message = ['\x1b[36m{method:<6}\x1b[0m', '\x1b[35m{status_code:<4}\x1b[0m', '{server:<17}', '\x1b[94m{port:<4}\x1b[0m', '\x1b[92m{host:<22}\x1b[0m']
        if 'ips' in kwargs and kwargs['ips']:
            base_message.append('\x1b[93m{ips:<15}\x1b[0m')
        messages.append('  '.join(base_message))
        super().log('  '.join(messages).format(**kwargs))

    def get_task_list(self):
        for method in self.filter_list(self.method_list):
            for host in self.filter_list(self.host_list):
                for port in self.filter_list(self.port_list):
                    yield {'method': method.upper(), 'host': host, 'port': port}

    def resolve_host_to_ips(self, host):
        try:
            ips = socket.gethostbyname_ex(host)[2]
            return ','.join(ips)
        except (socket.gaierror, socket.herror):
            return ''

    def is_ip_address(self, host):
        try:
            socket.inet_aton(host)
            return True
        except socket.error:
            return False

    def init(self):
        super().init()
        self.log_info(method='Method', status_code='Code', server='Server', port='Port', host='Host', ips='')
        self.log_info(method='------', status_code='----', server='------', port='----', host='----', ips='')

    def task(self, payload):
        method = payload['method']
        host = payload['host']
        port = payload['port']
        try:
            response = self.request(method, self.get_url(host, port), retry=1, timeout=3, allow_redirects=False)
        except Exception as e:
            return
        if response is not None:
            status_code = response.status_code
            server = response.headers.get('server', '')
            location = response.headers.get('location', '')
            if status_code == 302 and location in self.isp_redirects:
                return
            if status_code and status_code != 302:
                ips = self.resolve_host_to_ips(host) if not self.is_ip_address(host) else ''
                data = {'method': method, 'host': host, 'port': port, 'status_code': status_code, 'server': server, 'location': location, 'ips': ips}
                self.task_success(data)
                self.log_info(**data)

class ProxyScanner(DirectScanner):
    proxy = []

    def log_replace(self, *args):
        super().log_replace(':'.join(self.proxy), *args)

    def request(self, *args, **kwargs):
        proxy = self.get_url(self.proxy[0], self.proxy[1])
        return super().request(*args, proxies={'http': proxy, 'https': proxy}, **kwargs)

def generate_ips_from_cidr(cidr):
    ip_list = []
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        for ip in network.hosts():
            ip_list.append(str(ip))
    except ValueError as e:
        print('Error:', e)
    return ip_list

def process_file(filename):
    host_list = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                if '/' in line:
                    host_list.extend(generate_ips_from_cidr(line))
                else:
                    host_list.append(line)
            except ValueError as e:
                pass
    return host_list

def proxy_scanner_main():
    while True:
        clear_screen()
        display_banner()
        while True:
            proxy_input = input("Enter proxy:port (or 'back' to return): ").strip()
            if proxy_input.lower() in ['back', 'exit', 'quit', 'q']:
                return
            if ':' not in proxy_input:
                print(f'{Fore.RED}Invalid proxy format. Use proxy:port{Style.RESET_ALL}')
                choice = input(f'{Fore.YELLOW}1. Try again\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
                if choice == '2':
                    return
                continue
            proxy_host, proxy_port = proxy_input.split(':')
            filename = input('Enter the file name (e.g., file.txt): ').strip()
            if filename.lower() in ['back', 'exit', 'quit', 'q']:
                break
            try:
                host_list = process_file(filename)
            except FileNotFoundError:
                print(f"{Fore.RED}Error: File '{filename}' not found.{Style.RESET_ALL}")
                choice = input(f'{Fore.YELLOW}1. Try again\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
                if choice == '2':
                    return
                continue
            scanner = ProxyScanner()
            scanner.proxy = [proxy_host, proxy_port]
            scanner.method_list = ['GET']
            scanner.host_list = host_list
            scanner.port_list = ['80', '443']
            scanner.threads = 30
            scanner.start()
            while True:
                choice = input(f'{Fore.MAGENTA}Do you want to scan again? (yes/no): {Style.RESET_ALL}').strip().lower()
                if choice in ['yes', 'no']:
                    break
                print("Invalid choice. Please enter 'yes' or 'no'.")
            if choice == 'no':
                print('Exiting the program. Goodbye!')
                break
AQUA = '\x1b[96m'
YELLOW = '\x1b[93m'
ORANGE = '\x1b[38;5;214m'
GREEN = '\x1b[92m'
BRIGHT_GREEN = '\x1b[1;32m'
RESET = '\x1b[0m'

def extract_domains(text):
    domain_regex = '\\b(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,}\\b'
    return set(re.findall(domain_regex, text))

def save_to_file(domains, filename):
    with open(filename, 'w') as file:
        for domain in domains:
            file.write(domain + '\n')
    print(f'{GREEN}Output saved in {filename}{RESET}')
    print(f'{GREEN}Total extracted domains: {len(domains)}{RESET}')

def center_text(text, width=40):
    return text.center(width)

def domain_extractor():
    while True:
        clear_screen()
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print(f'\x1b[31m\x1b[1mDOMAIN COLLECTOR  FROM TEXT CONTEXT\x1b[0m')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print('░░░░░▄▄▄▄▄░▄░▄░▄░▄')
        print('▄▄▄▄██▄████▀█▀█▀█▀██▄')
        print('▀▄▀▄▀▄████▄█▄█▄█▄█████')
        print('\x1b[31m▒▀▀▀▀▀▀▀▀██▀▀▀▀██▀▒▄██\x1b[0m')
        print('▒▒▒▒▒▒▒▒▀▀▒▒▒▒▀▀▄▄██▀▒')
        print(f'{BRIGHT_GREEN}Select an option:{RESET}')
        print(f'{AQUA}1) Extract from file (csv/json/txt){RESET}')
        print(f'{AQUA}2) Extract from text content{RESET}')
        print()
        print(f'{BRIGHT_GREEN}c: Clear  e: Exit{Style.RESET_ALL}')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        choice = input(f'{BRIGHT_GREEN}Select: {RESET}').strip()
        if choice == '1':
            print()
            file_name = input(f'{YELLOW}Enter file name: {RESET}').strip()
            output_file = input(f'{YELLOW}File name for output: {RESET}').strip()
            try:
                with open(file_name, 'r') as f:
                    text = f.read()
                domains = extract_domains(text)
                print()
                print(f'{ORANGE}Domains extracted:{RESET}')
                for domain in domains:
                    print(f'{ORANGE}{domain}{RESET}')
                save_to_file(domains, output_file)
            except FileNotFoundError:
                print(f'{YELLOW}File not found. Please check the file name and try again.{RESET}')
        elif choice == '2':
            print()
            terminal_width = shutil.get_terminal_size().columns
            print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(center_text(f'{YELLOW}Paste your text content below{RESET}', terminal_width))
            print(center_text(f'{YELLOW}and when finished, type done..{RESET}', terminal_width))
            print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            user_input = ''
            while True:
                line = input()
                if 'done..' in line.lower():
                    break
                user_input += line + '\n'
            domains = extract_domains(user_input)
            print()
            print(f'{ORANGE}Domains extracted:{RESET}')
            for domain in domains:
                print(f'{ORANGE}{domain}{RESET}')
            output_file = input(f'{YELLOW}File name for output: {RESET}').strip()
            save_to_file(domains, output_file)
        elif choice.lower() == 'c':
            print('\x1bc', end='')
        elif choice.lower() == 'e':
            print(f'{YELLOW}Exiting program. Goodbye!{RESET}')
            break
        else:
            print(f'{YELLOW}Invalid choice. Please select 1, 2, c, or e.{RESET}')

async def fetch_status_custom_port(session, url, semaphore):
    try:
        async with semaphore:
            async with session.get(url, timeout=2) as response:
                server = response.headers.get('Server', 'Unknown')
                return (response.status, server)
    except asyncio.TimeoutError:
        return (None, 'Timeout')
    except Exception as e:
        return (None, f'Error: {e}')

async def scan_ip_custom_port(ip, port, total_ips, index, server_dict, semaphore):
    url = f'http://{ip}:{port}'
    async with aiohttp.ClientSession() as session:
        status, server = await fetch_status_custom_port(session, url, semaphore)
        if status and status != 302 and ('Error' not in server):
            server_dict[ip] = (status, server, port)
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            sys.stdout.flush()
            result_line = f'{Fore.GREEN}{ip}:{port}: {Fore.CYAN}{status} {Fore.MAGENTA}{server}'
            print(result_line)
            append_to_v4(result_line)
        scanned = index + 1
        progress = scanned / total_ips
        speed = scanned / (time.time() - start_time)
        progress_line = f'\rIPs scanned: {Fore.CYAN}{scanned}/{total_ips}{Style.RESET_ALL} ({progress * 100:.2f}%) - Speed: {Fore.CYAN}{speed:.2f} IPs/s{Style.RESET_ALL}'
        sys.stdout.write(progress_line)
        sys.stdout.flush()

async def scan_cidr_block_custom_port(cidr_block, port):
    network = ipaddress.ip_network(cidr_block, strict=False)
    total_ips = network.num_addresses
    ips = network.hosts()
    server_dict = {}
    semaphore = asyncio.Semaphore(300)
    global start_time
    start_time = time.time()
    chunk_size = 1000
    ip_list = list(ips)
    print(f'{Fore.RED}{Style.BRIGHT}ACTIVE IPS ALIVE ON PORT {port}\n' + '-' * 20)
    for i in range(0, len(ip_list), chunk_size):
        chunk = ip_list[i:i + chunk_size]
        tasks = [scan_ip_custom_port(str(ip), port, total_ips, i + j, server_dict, semaphore) for j, ip in enumerate(chunk)]
        await asyncio.gather(*tasks)
    end_time = time.time()
    duration = end_time - start_time
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    total_scanned = len(server_dict)
    speed = total_scanned / duration if duration > 0 else 0
    print(f'\n{Fore.YELLOW}Time taken for scanning: {duration:.2f} seconds')
    print(f'{Fore.YELLOW}Scanning speed: {Fore.CYAN}{speed:.2f} IPs per second{Style.RESET_ALL}')

async def scan_multiple_cidr_blocks_custom_port(cidr_blocks, port):
    for cidr_block in cidr_blocks:
        try:
            ipaddress.ip_network(cidr_block, strict=False)
            print(f'\nScanning CIDR block: {cidr_block} on port {port}')
            await scan_cidr_block_custom_port(cidr_block, port)
        except ValueError:
            print(f"{Fore.RED}Invalid CIDR block '{cidr_block}'. Skipping.")

async def custom_port_scanner():
    while True:
        clear_screen()
        title = f'{Fore.RED}{Style.BRIGHT}CUSTOM PORT SCANNER ANY 443/22/8080/....... {Style.RESET_ALL}'
        subtitle = f'{Fore.CYAN}CREATOR TELEGRAM: @shimul00889{Style.RESET_ALL}'
        logo = f'{Fore.RED}{Style.BRIGHT}DEVELOPER IS NOT RESPONSIBLE FOR ANY HARM TO YOUR NETWORK\n' + '░░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄░░░░░░░\n' + '░░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄░░░░\n' + '░░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█░░░\n' + '░░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░░█░░\n' + '░▄▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░░█░\n' + '█░▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒░█\n' + '█░▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█\n' + '░█░▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█░\n' + '░░█░░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█░░\n' + '░░░█░░░░██░░▀█▄▄▄█▄▄█▄████░█░░░\n' + '░░░░█░░░░▀▀▄░█░░░█░█▀██████░█░░\n' + '░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█░░\n' + '░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░▒░░░█░\n' + '░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░░░░█░\n' + '░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░░░░█░░\n' + f'{Style.RESET_ALL}'
        print(title)
        print(subtitle)
        print(logo)
        while True:
            cidr_input = input("Enter IP CIDR blocks (e.g., 192.167.0.0/16,192.168.0.0/16) or 'back': ").strip()
            if cidr_input.lower() in ['back', 'exit', 'quit', 'q']:
                return
            port_input = input('Enter the port to scan (e.g., 80, 443): ')
            try:
                port = int(port_input)
                if port < 1 or port > 65535:
                    print(f'{Fore.RED}Invalid port number. Port must be between 1 and 65535.{Style.RESET_ALL}')
                    continue
            except ValueError:
                print(f'{Fore.RED}Invalid port input. Please enter a valid port number.{Style.RESET_ALL}')
                continue
            cidr_blocks = [cidr.strip() for cidr in cidr_input.split(',')]
            await scan_multiple_cidr_blocks_custom_port(cidr_blocks, port)
            while True:
                continue_scanning = input('Do you want to scan more CIDR blocks? (yes/no): ').strip().lower()
                if continue_scanning in ['yes', 'no']:
                    break
                print(f"{Fore.RED}Invalid input. Please enter 'yes' or 'no'.{Style.RESET_ALL}")
            if continue_scanning != 'yes':
                break

def unlimited_scanner_no_freeze():
    """Super Fast HTTP Status Checker – Filters out 302 and errors, keeps all other responses"""
    RED_BOLD = '\x1b[1;31m'
    GREEN_BOLD = '\x1b[1;32m'
    YELLOW_BOLD = '\x1b[1;33m'
    CYAN_BOLD = '\x1b[1;36m'
    WHITE_BOLD = '\x1b[1;37m'
    BLUE_BOLD = '\x1b[1;34m'
    MAGENTA_BOLD = '\x1b[1;35m'
    RESET = '\x1b[0m'
    CLEAR_SCREEN = '\x1b[2J\x1b[H'
    STATUS_COLORS = {'200': GREEN_BOLD, '201': GREEN_BOLD, '202': GREEN_BOLD, '203': GREEN_BOLD, '204': GREEN_BOLD, '301': YELLOW_BOLD, '302': YELLOW_BOLD, '303': YELLOW_BOLD, '304': YELLOW_BOLD, '307': YELLOW_BOLD, '308': YELLOW_BOLD, '400': RED_BOLD, '401': RED_BOLD, '403': RED_BOLD, '404': RED_BOLD, '405': RED_BOLD, '500': RED_BOLD, '501': RED_BOLD, '502': RED_BOLD, '503': RED_BOLD, '504': RED_BOLD}

    def get_status_color(status_code):
        if status_code in STATUS_COLORS:
            return STATUS_COLORS[status_code]
        if status_code.isdigit():
            code = int(status_code)
            if 200 <= code < 300:
                return GREEN_BOLD
            elif 300 <= code < 400:
                return YELLOW_BOLD
            elif 400 <= code < 500:
                return RED_BOLD
            elif 500 <= code < 600:
                return RED_BOLD
        return WHITE_BOLD

    def clear_screen():
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()

    def get_terminal_width():
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80

    def get_terminal_height():
        try:
            return shutil.get_terminal_size().lines
        except:
            return 24

    def print_header():
        term_width = get_terminal_width()
        effective_width = max(term_width, 40)
        logo_lines = ['▒▒▒▒▒▒▒▒▄▄▄▄▄▄▄▄▒▒▒▒▒▒', '▒▒█▒▒▒▄██████████▄▒▒▒▒', '▒█▐▒▒▒████████████▒▒▒▒', '▒▌▐▒▒██▄▀██████▀▄██▒▒▒', '▐┼▐▒▒██▄▄▄▄██▄▄▄▄██▒▒▒', '▐┼▐▒▒██████████████▒▒▒', '▐▄▐████─▀▐▐▀█─█─▌▐██▄▒', '▒▒█████──────────▐███▌', '▒▒█▀▀██▄█─▄───▐─▄███▀▒', '▒▒█▒▒███████▄██████▒▒▒', '▒▒▒▒▒██████████████▒▒▒', '▒▒▒▒▒█████████▐▌██▌▒▒▒', '▒▒▒▒▒▐▀▐▒▌▀█▀▒▐▒█▒▒▒▒▒', '▒▒▒▒▒▒▒▒▒▒▒▐▒▒▒▒▌▒▒▒▒▒']
        title = 'SUPER FAST HTTP SCANNER – KEEP ALL EXCEPT 302 & ERRORS'
        subtitle = 'Live Results | Auto-Resume | Multi-Port'
        print(RED_BOLD + '=' * effective_width + RESET)
        if len(title) > effective_width - 2:
            title = title[:effective_width - 5] + '...'
        print(RED_BOLD + title.center(effective_width) + RESET)
        if len(subtitle) > effective_width - 2:
            subtitle = subtitle[:effective_width - 5] + '...'
        print(CYAN_BOLD + subtitle.center(effective_width) + RESET)
        print(RED_BOLD + '=' * effective_width + RESET)
        for line in logo_lines:
            if len(line) > effective_width - 2:
                line = line[:effective_width - 2]
            print(RED_BOLD + line.center(effective_width) + RESET)
        print(RED_BOLD + '=' * effective_width + RESET)
        print()

    def find_output_files(input_file):
        input_dir = os.path.dirname(input_file)
        input_basename = os.path.splitext(os.path.basename(input_file))[0]
        output_files = []
        search_dir = input_dir if input_dir else '.'
        for file in os.listdir(search_dir):
            if file.startswith(f'{input_basename}_results') and file.endswith('.txt'):
                full_path = os.path.join(search_dir, file)
                output_files.append(full_path)
        output_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return output_files

    def get_host_count_from_file(filename):
        try:
            with open(filename, 'r') as f:
                return sum((1 for line in f if line.strip()))
        except:
            return 0

    def read_processed_hosts(output_file):
        processed = set()
        try:
            with open(output_file, 'r') as f:
                for line in f:
                    if ':' in line and '→' not in line:
                        host = line.split(':', 1)[0].strip()
                        if host:
                            processed.add(host)
        except:
            pass
        return processed

    class FastHTTPChecker:

        def __init__(self, timeout=0.8, port=80):
            self.timeout = timeout
            self.port = port
            self.request_template = 'GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'

        def check_http_fast(self, hostname, ip, port=None):
            if port is None:
                port = self.port
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.connect((ip, port))
                time.sleep(0.05)
                request = self.request_template.format(hostname)
                sock.send(request.encode('ascii', errors='ignore'))
                response_data = []
                start_time = time.time()
                while time.time() - start_time < self.timeout:
                    try:
                        ready = select.select([sock], [], [], 0.05)
                        if ready[0]:
                            chunk = sock.recv(1024)
                            if not chunk:
                                break
                            response_data.append(chunk)
                            if len(response_data) >= 2:
                                break
                        else:
                            continue
                    except socket.timeout:
                        break
                    except:
                        break
                if response_data:
                    response = b''.join(response_data).decode('utf-8', errors='ignore')
                    status_code = 'unknown'
                    if response.startswith('HTTP/'):
                        try:
                            first_line = response.split('\n')[0]
                            parts = first_line.split()
                            if len(parts) >= 2:
                                status_code = parts[1]
                        except:
                            pass
                    server = 'unknown'
                    response_lower = response.lower()
                    if 'server:' in response_lower:
                        lines = response.split('\n')
                        for line in lines[:10]:
                            if line.lower().startswith('server:'):
                                server = line.split(':', 1)[1].strip()
                                break
                    return (status_code, server)
                return ('no-response', None)
            except socket.timeout:
                return ('timeout', None)
            except ConnectionRefusedError:
                return ('refused', None)
            except Exception:
                return ('error', None)
            finally:
                if sock:
                    try:
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                    except:
                        pass

    def read_file_chunks(filename, processed_hosts, start_line=0, chunk_size=50):
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for _ in range(start_line):
                    try:
                        next(f)
                    except StopIteration:
                        break
                chunk = []
                current_line = start_line
                for line in f:
                    line = line.strip()
                    if line and (not line.startswith('#')):
                        parts = line.split()
                        if len(parts) >= 2:
                            hostname = parts[0]
                            ip = parts[1]
                            if hostname not in processed_hosts:
                                chunk.append((current_line, hostname, ip))
                                current_line += 1
                                if len(chunk) >= chunk_size:
                                    yield chunk
                                    chunk = []
                            else:
                                current_line += 1
                if chunk:
                    yield chunk
        except Exception as e:
            print(f'\n{RED_BOLD}Error reading file: {e}{RESET}')
            sys.exit(1)

    def worker(task_queue, result_queue, checker):
        while True:
            try:
                task = task_queue.get(timeout=0.1)
                if task is None:
                    break
                line_num, hostname, ip = task
                status_code, server = checker.check_http_fast(hostname, ip)
                result_queue.put((line_num, hostname, ip, status_code, server))
                time.sleep(0.001)
            except queue.Empty:
                continue
            except Exception:
                continue

    def print_update(scanned, total, found, errors, elapsed, last_results, results_display, output_file, port):
        term_width = get_terminal_width()
        effective_width = max(term_width, 40)
        sys.stdout.write(CLEAR_SCREEN)
        print_header()
        percent = scanned / total * 100 if total > 0 else 0
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        speed = scanned / elapsed if elapsed > 0 else 0
        bar_length = min(20, effective_width - 60)
        if bar_length < 5:
            bar_length = 5
        filled = int(bar_length * scanned / total) if total > 0 else 0
        bar = '█' * filled + '▒' * (bar_length - filled)
        status_line = f'[{timestamp}] {bar} {scanned}/{total} ({percent:.1f}%) | Found:{found} Errors:{errors} {speed:.1f}/s'
        if len(status_line) > effective_width - 1:
            status_line = status_line[:effective_width - 4] + '...'
        print(RED_BOLD + status_line + RESET)
        output_info = f'Output: {output_file} | Port: {port} | Total Results: {len(results_display)}'
        if len(output_info) > effective_width - 1:
            output_info = output_info[:effective_width - 4] + '...'
        print(CYAN_BOLD + output_info + RESET)
        print(RED_BOLD + '-' * min(effective_width, 50) + RESET)
        print(f'{GREEN_BOLD}=== ALL LIVE RESULTS ({len(results_display)} total) ==={RESET}')
        print(f'{YELLOW_BOLD}Scroll up to see all results{RESET}')
        print(RED_BOLD + '-' * min(effective_width, 50) + RESET)
        if results_display:
            display_results = results_display[-50:] if len(results_display) > 50 else results_display
            for line in display_results:
                if len(line) > effective_width - 2:
                    line = line[:effective_width - 5] + '...'
                print(line)
            if len(results_display) > 50:
                print(f'{CYAN_BOLD}... and {len(results_display) - 50} more results (scroll up to see all){RESET}')
        else:
            print(f'{YELLOW_BOLD}Waiting for results...{RESET}')
        print(RED_BOLD + '-' * min(effective_width, 50) + RESET)
        if last_results:
            h, ip_addr, s, sv = last_results[-1]
            short_h = h[:15] + '..' if len(h) > 15 else h
            status_color = get_status_color(s)
            last_line = f'Last: {CYAN_BOLD}{short_h}{RESET}:{YELLOW_BOLD}{port}{RESET} '
            last_line += f'→ {status_color}{s}{RESET}'
            if sv and sv != 'unknown':
                last_line += f' [{MAGENTA_BOLD}{sv[:10]}{RESET}]'
            if ip_addr:
                last_line += f' ({BLUE_BOLD}{ip_addr}{RESET})'
            print(YELLOW_BOLD + 'Last: ' + last_line + RESET)
        print(RED_BOLD + '=' * min(effective_width, 40) + RESET)
        print(f'{YELLOW_BOLD}Press Ctrl+C to stop | Scroll up/down to see all results{RESET}')
        sys.stdout.flush()

    def format_result_line(hostname, ip, port, status_code, server):
        status_color = get_status_color(status_code)
        line = f'{CYAN_BOLD}{hostname}{RESET}:{YELLOW_BOLD}{port}{RESET} '
        line += f'→ {status_color}{status_code}{RESET}'
        if ip:
            line += f' ({BLUE_BOLD}{ip}{RESET})'
        if server and server != 'unknown':
            line += f' [{MAGENTA_BOLD}{server[:15]}{RESET}]'
        return line

    def count_total_lines(filename):
        try:
            with open(filename, 'rb') as f:
                return sum((1 for _ in f))
        except:
            return 0
    while True:
        clear_screen()
        print_header()
        try:
            workers_input = input(f'{YELLOW_BOLD}Threads (1-50, default 20):{RESET} ').strip()
            workers = int(workers_input) if workers_input else 20
            workers = max(1, min(50, workers))
        except:
            workers = 20
        try:
            timeout_input = input(f'{YELLOW_BOLD}Timeout seconds (0.3-3, default 0.8):{RESET} ').strip()
            timeout = float(timeout_input) if timeout_input else 0.8
            timeout = max(0.3, min(3, timeout))
        except:
            timeout = 0.8
        try:
            port_input = input(f'{YELLOW_BOLD}Port (default 80):{RESET} ').strip()
            port = int(port_input) if port_input else 80
            port = max(1, min(65535, port))
        except:
            port = 80
        while True:
            input_file = input(f'\n{YELLOW_BOLD}Hosts file (hostname IP per line):{RESET} ').strip()
            if os.path.isfile(input_file):
                break
            print(f'{RED_BOLD}File not found{RESET}')
        while True:
            output_file = input(f'\n{YELLOW_BOLD}Output file:{RESET} ').strip()
            if output_file:
                if not output_file.endswith('.txt'):
                    output_file += '.txt'
                break
            print(f'{RED_BOLD}Please enter an output file name{RESET}')
        if os.path.exists(output_file):
            print(f"\n{CYAN_BOLD}Output file '{os.path.basename(output_file)}' already exists.{RESET}")
            print(f'{YELLOW_BOLD}Choose an option:{RESET}')
            print(f'  1. Resume from where you left off')
            print(f'  2. Start fresh (overwrite file)')
            print(f'  3. Use a different filename')
            while True:
                choice = input(f'\n{YELLOW_BOLD}Enter choice (1, 2, or 3):{RESET} ').strip()
                if choice == '1':
                    processed_hosts = read_processed_hosts(output_file)
                    start_line = get_host_count_from_file(output_file)
                    resume_mode = True
                    print(f'\n{GREEN_BOLD}✓ Resuming from existing scan{RESET}')
                    print(f'  Already processed: {len(processed_hosts)} hosts')
                    print(f'  Resume from line: {start_line}')
                    input(f'\n{YELLOW_BOLD}Press Enter to continue...{RESET}')
                    break
                elif choice == '2':
                    resume_mode = False
                    start_line = 0
                    processed_hosts = set()
                    print(f'\n{YELLOW_BOLD}Starting fresh scan (overwriting existing file)...{RESET}')
                    input(f'\n{YELLOW_BOLD}Press Enter to continue...{RESET}')
                    break
                elif choice == '3':
                    base, ext = os.path.splitext(output_file)
                    i = 1
                    while True:
                        new_file = f'{base}_{i}{ext}'
                        if not os.path.exists(new_file):
                            output_file = new_file
                            break
                        i += 1
                    resume_mode = False
                    start_line = 0
                    processed_hosts = set()
                    print(f'\n{GREEN_BOLD}Using new file: {output_file}{RESET}')
                    input(f'\n{YELLOW_BOLD}Press Enter to continue...{RESET}')
                    break
                else:
                    print(f'{RED_BOLD}Invalid choice. Please enter 1, 2, or 3.{RESET}')
        else:
            print(f'\n{CYAN_BOLD}New output file: {os.path.basename(output_file)}{RESET}')
            print(f'{YELLOW_BOLD}Choose scan option:{RESET}')
            print(f'  1. Start from beginning (line 0)')
            print(f'  2. Start from specific line number')
            while True:
                choice = input(f'\n{YELLOW_BOLD}Enter choice (1 or 2):{RESET} ').strip()
                if choice == '1':
                    resume_mode = False
                    start_line = 0
                    processed_hosts = set()
                    print(f'\n{GREEN_BOLD}Starting from beginning (line 0){RESET}')
                    break
                elif choice == '2':
                    while True:
                        try:
                            start_line_input = input(f'{YELLOW_BOLD}Enter line number to start from:{RESET} ').strip()
                            if start_line_input:
                                start_line = int(start_line_input)
                                if start_line >= 0:
                                    resume_mode = False
                                    processed_hosts = set()
                                    print(f'\n{GREEN_BOLD}Starting from line: {start_line}{RESET}')
                                    break
                                else:
                                    print(f'{RED_BOLD}Please enter a positive number or 0{RESET}')
                            else:
                                print(f'{RED_BOLD}Please enter a number{RESET}')
                        except ValueError:
                            print(f'{RED_BOLD}Invalid input. Please enter a valid number.{RESET}')
                    break
                else:
                    print(f'{RED_BOLD}Invalid choice. Please enter 1 or 2.{RESET}')
            input(f'\n{YELLOW_BOLD}Press Enter to continue...{RESET}')
        total_lines = count_total_lines(input_file)
        if start_line > total_lines:
            print(f'{RED_BOLD}Warning: Start line ({start_line}) exceeds total lines ({total_lines}){RESET}')
            start_line = 0
            print(f'{YELLOW_BOLD}Reset to start from beginning (line 0){RESET}')
            input(f'\n{YELLOW_BOLD}Press Enter to continue...{RESET}')
        clear_screen()
        checker = FastHTTPChecker(timeout=timeout, port=port)
        task_queue = queue.Queue(maxsize=workers * 5)
        result_queue = queue.Queue()
        threads = []
        for _ in range(workers):
            t = threading.Thread(target=worker, args=(task_queue, result_queue, checker))
            t.daemon = True
            t.start()
            threads.append(t)
        try:
            out_f = open(output_file, 'a' if resume_mode else 'w', buffering=1)
        except Exception as e:
            print(f'{RED_BOLD}Error opening output file: {e}{RESET}')
            sys.exit(1)
        scanned = start_line
        found = 0
        errors = 0
        last_results = deque(maxlen=3)
        results_display = []
        start_time = time.time()
        last_update = 0
        try:
            for chunk in read_file_chunks(input_file, processed_hosts, start_line, chunk_size=50):
                for task in chunk:
                    task_queue.put(task)
                    time.sleep(0.0005)
                results_needed = len(chunk)
                results_received = 0
                while results_received < results_needed:
                    try:
                        line_num, hostname, ip, status_code, server = result_queue.get(timeout=0.5)
                        results_received += 1
                        scanned += 1
                        unwanted = {'302', 'timeout', 'refused', 'error', 'no-response'}
                        if status_code not in unwanted:
                            out_f.write(f"{hostname}:{port} {status_code} : {server or 'unknown'}\n")
                            out_f.flush()
                            found += 1
                            result_line = format_result_line(hostname, ip, port, status_code, server)
                            results_display.append(result_line)
                        else:
                            errors += 1
                        last_results.append((hostname, ip, status_code, server))
                        current_time = time.time()
                        if current_time - last_update >= 0.2:
                            elapsed = time.time() - start_time
                            print_update(scanned, total_lines, found, errors, elapsed, last_results, results_display, output_file, port)
                            last_update = current_time
                    except queue.Empty:
                        continue
        except KeyboardInterrupt:
            print(f'\n\n{YELLOW_BOLD}⚠ Scan stopped by user{RESET}')
            elapsed = time.time() - start_time
            print(f'{GREEN_BOLD}Results Summary:{RESET}')
            print(f'  Scanned: {scanned} hosts')
            print(f'  Found: {found} hosts')
            print(f'  Errors/Filtered: {errors} hosts')
            if elapsed > 0:
                print(f'  Speed: {scanned / elapsed:.1f}/s')
            print(f'  Resume from line: {scanned}')
            print(f'  Output: {output_file}')
        except Exception as e:
            print(f'\n{RED_BOLD}Error: {e}{RESET}')
        finally:
            for _ in threads:
                task_queue.put(None)
            for t in threads:
                t.join(timeout=1)
            elapsed = time.time() - start_time
            speed = scanned / elapsed if elapsed > 0 else 0
            out_f.close()
            print(f'\n\n{GREEN_BOLD}✓ SCAN COMPLETE{RESET}')
            print(f'{GREEN_BOLD}═══ Results Summary ═══{RESET}')
            print(f'  Total scanned: {scanned} hosts')
            print(f'  Valid found: {found} hosts')
            print(f'  Errors/Filtered: {errors} hosts')
            print(f'  Time: {elapsed:.1f}s')
            print(f'  Speed: {speed:.1f} hosts/s')
            print(f'  Output: {output_file}')
            if results_display:
                print(f'  Total results: {len(results_display)}')
        while True:
            print(f'\n{CYAN_BOLD}Options:{RESET}')
            print(f'{GREEN_BOLD}1. Scan another file{RESET}')
            print(f'{YELLOW_BOLD}2. Return to main menu{RESET}')
            choice = input(f'{CYAN_BOLD}Enter your choice (1-2): {RESET}').strip()
            if choice == '1':
                break
            elif choice == '2':
                return
            else:
                print(f'{RED_BOLD}Invalid choice. Please enter 1 or 2.{RESET}')

def show_banner():
    print(f'\n{Fore.RED}DOMAIN FINDER ANY COUNTRY V5 @PREMIUM{Style.RESET_ALL}')
    print(f'{Fore.CYAN}')
    print('  /|  |\\            /|  |\\  ')
    print(' /|  |\\            /|  |\\ ')
    print('/ |  | \\          / |  | \\ ')
    print('| |  | |          | |  | | ')
    print('\\  \\/  /  __  __  \\  \\/  / ')
    print(' \\    /  / /  \\ \\  \\    /  ')
    print('  \\  /   \\ \\__/ /   \\  /   ')
    print('  \\  /   /      \\   \\  /   ')
    print(' _ \\ \\__/ O    O \\__/ / _  ')
    print(' \\\\ \\___          ___/ //   ')
    print('_  \\\\___/  ______  \\___//  _')
    print('\\\\  ----(          )----  //')
    print(' \\\\_____( ________ )_____// ')
    print('  ~-----(          )-----~ _')
    print('   _____( ________ )_____  \\\\')
    print('  /,----(          )----  _//')
    print(' //     (  ______  )     /  \\ ')
    print(' ~       \\        /      \\  / ')
    print('          \\  __  /       / /  ')
    print('           \\    /       / /   ')
    print('            \\   \\      / /    ')
    print('             \\   ~----~ /     ')
    print('              \\________/      ')
    print(f'{Style.RESET_ALL}')

def extract_hostnames(text):
    try:
        text = re.sub('\\d{8,}|[\\*\\?%]', '', text)
        potential = re.findall('(?:(?:[a-z0-9-]+\\.)+[a-z]{2,})', text.lower())
        valid = []
        for host in potential:
            host = host.strip('.-')
            parts = host.split('.')
            if 4 <= len(host) <= 253 and len(parts) >= 2 and (len(parts[-1]) >= 2) and (not any((p.startswith('-') or p.endswith('-') or len(p) > 63 for p in parts))):
                valid.append(host)
        return list(dict.fromkeys(valid))
    except Exception as e:
        print(f'{Fore.YELLOW}Warning: Error extracting hostnames: {str(e)}{Style.RESET_ALL}')
        return []

def scrape_crtsh(domain_suffix, max_retries=3):
    base_url = 'https://crt.sh/'
    params = {'q': f"%.{domain_suffix.lstrip('.')}", 'output': 'json'}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                try:
                    data = response.json()
                    domains = []
                    for item in data:
                        if 'name_value' in item:
                            domains.extend((d.strip().lower() for d in re.split('[\\n,]', item['name_value']) if d.strip()))
                    return domains
                except json.JSONDecodeError:
                    params.pop('output', None)
                    continue
            response = requests.get(base_url, params={'q': f"%.{domain_suffix.lstrip('.')}"}, headers=headers, timeout=2)
            return re.findall('(?:[a-z0-9-]+\\.)+[a-z]{2,}', response.text.lower())
        except requests.RequestException as e:
            print(f'{Fore.YELLOW}Attempt {attempt + 1}/{max_retries} failed: {str(e)}')
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
    return []

async def domain_finder():
    while True:
        try:
            clear_screen()
            show_banner()
            while True:
                print(f"\n{Fore.CYAN}Enter domain suffix (e.g., .ke, .org, .com) or 'back': {Style.RESET_ALL}", end='')
                domain_suffix = input().strip().lower()
                if domain_suffix.lower() in ['back', 'exit', 'quit', 'q']:
                    return
                if not domain_suffix:
                    print(f'{Fore.RED}Please enter a domain suffix.{Style.RESET_ALL}')
                    continue
                if not domain_suffix.startswith('.'):
                    domain_suffix = f'.{domain_suffix}'
                print(f'{Fore.CYAN}Scanning From DATABASE API  for *{domain_suffix} domains...{Style.RESET_ALL}')
                with tqdm(total=100, bar_format=f'{Fore.CYAN}{{l_bar}}{{bar:20}}{{r_bar}}{{bar:-20b}}', ncols=70) as pbar:
                    try:
                        raw_domains = scrape_crtsh(domain_suffix)
                        pbar.update(40)
                        filtered_domains = extract_hostnames('\n'.join(raw_domains))
                        pbar.update(30)
                        final_domains = sorted(set(filtered_domains), key=lambda x: (len(x.split('.')), x))
                        pbar.update(30)
                    except Exception as e:
                        print(f'{Fore.RED}Error during scanning: {str(e)}{Style.RESET_ALL}')
                        final_domains = []
                if not final_domains:
                    print(f'{Fore.YELLOW}No valid domains found for *{domain_suffix}{Style.RESET_ALL}')
                    choice = input(f'{Fore.YELLOW}1. Try another suffix\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
                    if choice == '2':
                        return
                    continue
                while True:
                    print(f'\n{Fore.GREEN}Found {len(final_domains)} domains.{Style.RESET_ALL}')
                    print(f'{Fore.CYAN}1. Save to file')
                    print('2. Scan another domain')
                    print('3. Return to main menu')
                    print(f'{Style.RESET_ALL}')
                    choice = input(f'{Fore.CYAN}Select option (1-3): {Style.RESET_ALL}').strip()
                    if choice == '1':
                        filename = input(f'{Fore.CYAN}Enter filename (e.g., domains.txt): {Style.RESET_ALL}').strip()
                        if not filename:
                            filename = f"domains_{domain_suffix.strip('.')}.txt"
                        try:
                            with open(filename, 'w') as f:
                                f.write('\n'.join(sorted(final_domains)))
                            print(f'{Fore.GREEN}Successfully saved {len(final_domains)} domains to {filename}{Style.RESET_ALL}')
                        except Exception as e:
                            print(f'{Fore.RED}Error saving file: {str(e)}{Style.RESET_ALL}')
                        input(f'{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}')
                        break
                    elif choice == '2':
                        break
                    elif choice == '3':
                        return
                    else:
                        print(f'{Fore.RED}Invalid choice. Please select 1-3.{Style.RESET_ALL}')
        except KeyboardInterrupt:
            print(f'\n{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}')
            return
        except Exception as e:
            print(f'{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}')
            input(f'{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}')

def load_hostnames_simple(file_path, start_line):
    """Load hostnames starting from a specific line number."""
    try:
        with open(file_path, 'r') as f:
            for _ in range(start_line):
                next(f, None)
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f'{Fore.RED}File not found: {file_path}{Style.RESET_ALL}')
        return None
    except Exception as e:
        print(f'{Fore.RED}Error reading file: {e}{Style.RESET_ALL}')
        return None

class AdvancedHostnameScannerSimple:

    def __init__(self):
        self.SERVER_MAPPINGS = {'Apache': ['Apache', 'Apache/2', 'Apache/2.2', 'Apache/2.4', 'httpd'], 'Nginx': ['nginx', 'NGINX', 'Tengine'], 'Microsoft-IIS': ['Microsoft-IIS', 'IIS', 'Microsoft-HTTPAPI'], 'LiteSpeed': ['LiteSpeed', 'Litespeed', 'LiteSpeedTech'], 'OpenResty': ['openresty'], 'Caddy': ['caddy'], 'Gunicorn': ['gunicorn'], 'uWSGI': ['uWSGI'], 'Cherokee': ['Cherokee'], 'Tomcat': ['Apache-Coyote', 'Tomcat'], 'Jetty': ['Jetty'], 'Lighttpd': ['lighttpd'], 'Cloudflare': ['cloudflare', 'CF', 'CloudFlare'], 'Imperva': ['imperva', 'incapsula'], 'Akamai': ['AkamaiGHost', 'AkamaiNetStorage', 'Akamai'], 'Fastly': ['Fastly', 'fastly'], 'AWS CloudFront': ['CloudFront'], 'Google Cloud CDN': ['Google Frontend', 'gws'], 'BunnyCDN': ['bunnycdn', 'BunnyCDN'], 'Amazon S3': ['AmazonS3', 'S3'], 'Netlify': ['Netlify'], 'WP Engine': ['WP Engine', 'WPE-'], 'Kinsta': ['Kinsta'], 'Heroku': ['heroku', 'Heroku'], 'Firebase': ['Firebase'], 'Vercel': ['Vercel'], 'DigitalOcean': ['DONODE'], 'Azure': ['Azure', 'ARR', 'WAWS'], 'Other': ['Server', 'server'], 'Unknown': []}

    def detect_server(self, server_header):
        if not server_header:
            return 'Unknown'
        server_header = server_header.lower()
        for server, patterns in self.SERVER_MAPPINGS.items():
            for pattern in patterns:
                if pattern.lower() in server_header:
                    return server
        return 'Other'

    def get_http_response_fast(self, hostname, port=80, timeout=2):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((hostname, port))
                s.send(f'HEAD / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n'.encode())
                response = b''
                while True:
                    data = s.recv(1024)
                    if not data or b'\r\n\r\n' in response:
                        break
                    response += data
                return response.decode(errors='ignore').split('\r\n\r\n')[0]
        except:
            return None

    def scan_host_fast(self, hostname):
        hostname = hostname.strip()
        if not hostname:
            return (hostname, None, None)
        headers = self.get_http_response_fast(hostname)
        if not headers:
            return (hostname, None, None)
        status_code = None
        server_header = None
        lines = headers.split('\r\n')
        if len(lines) > 0:
            try:
                status_code = int(lines[0].split(' ')[1])
            except:
                pass
        for line in lines[1:]:
            if line.lower().startswith('server:'):
                server_header = line.split(':', 1)[1].strip()
                break
        server_name = self.detect_server(server_header)
        return (hostname, status_code, server_name)

    def run_scan_fast(self, file_path, results_file, start_line):
        try:
            with open(results_file, 'w') as outfile:
                hostnames = load_hostnames_simple(file_path, start_line)
                if hostnames is None:
                    print(f'{Fore.RED}Cannot load hostnames from file.{Style.RESET_ALL}')
                    return
                futures = set()
                with ThreadPoolExecutor(max_workers=100) as executor:
                    for _ in range(1000):
                        try:
                            hostname = next(hostnames)
                            if hostname:
                                futures.add(executor.submit(self.scan_host_fast, hostname))
                        except StopIteration:
                            break
                    pbar = tqdm(desc='Scanning hosts', unit='hosts')
                    try:
                        while futures:
                            done, _ = wait(futures, return_when=FIRST_COMPLETED)
                            for future in done:
                                futures.remove(future)
                                result = future.result()
                                if result[1] and result[1] != 302:
                                    result_line = f'{result[0]} : {result[1]} : {result[2]}'
                                    outfile.write(result_line + '\n')
                                    outfile.flush()
                                    append_to_v4(result_line)
                                pbar.update(1)
                                try:
                                    hostname = next(hostnames)
                                    if hostname:
                                        futures.add(executor.submit(self.scan_host_fast, hostname))
                                except StopIteration:
                                    pass
                    except KeyboardInterrupt:
                        print(f'{Fore.YELLOW}\nScan paused by user.{Style.RESET_ALL}')
                        return
                    pbar.close()
        except Exception as e:
            print(f'{Fore.RED}Error in scan: {e}{Style.RESET_ALL}')
            return

async def option_10_advanced_hostname_scanner():
    """
    OPTION 10: Advanced Hostname Scanner with error handling
    """
    while True:
        try:
            clear_screen()
            print(f'\n{Fore.RED}{Style.BRIGHT}ADVANCED HOSTNAME SCANNER (ANTI DPI){Style.RESET_ALL}')
            print(f'{Fore.CYAN}Telegram: @shimul00889{Style.RESET_ALL}')
            print(f"{Fore.YELLOW}Type 'back' at any time to return to main menu{Style.RESET_ALL}")
            scanner = AdvancedHostnameScannerSimple()
            while True:
                input_file = input(f"\n{Fore.CYAN}Enter path to hostnames file (or 'back'): {Style.RESET_ALL}").strip()
                if input_file.lower() in ['back', 'exit', 'quit', 'q']:
                    return
                if not input_file:
                    print(f'{Fore.YELLOW}Please enter a file path.{Style.RESET_ALL}')
                    continue
                if not os.path.isfile(input_file):
                    print(f'{Fore.RED}File not found: {input_file}{Style.RESET_ALL}')
                    while True:
                        choice = input(f'{Fore.YELLOW}1. Try again\n2. Return to main menu\nChoose (1-2): {Style.RESET_ALL}').strip()
                        if choice == '1':
                            break
                        elif choice == '2':
                            return
                        else:
                            print(f'{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}')
                    continue
                break
            while True:
                results_file = input(f"{Fore.CYAN}Enter results file name (default: host_results.txt, or 'back'): {Style.RESET_ALL}").strip()
                if results_file.lower() in ['back', 'exit', 'quit', 'q']:
                    return
                if not results_file:
                    results_file = 'host_results.txt'
                    break
                if not re.match('^[\\w\\-. ]+$', results_file):
                    print(f'{Fore.RED}Invalid file name. Use only letters, numbers, dots, hyphens, and underscores.{Style.RESET_ALL}')
                    continue
                break
            while True:
                print(f'\n{Fore.CYAN}Choose scan mode:{Style.RESET_ALL}')
                print(f'{Fore.WHITE}1 = NEW scan (start from line 0){Style.RESET_ALL}')
                print(f'{Fore.WHITE}2 = RESUME scan from specific line{Style.RESET_ALL}')
                print(f"{Fore.YELLOW}Type 'back' to return{Style.RESET_ALL}")
                mode = input(f"{Fore.CYAN}Enter choice (1/2 or 'back'): {Style.RESET_ALL}").strip()
                if mode.lower() in ['back', 'exit', 'quit', 'q']:
                    return
                if mode == '1':
                    start_line = 0
                    print(f'{Fore.GREEN}Starting NEW scan...{Style.RESET_ALL}')
                    break
                elif mode == '2':
                    while True:
                        resume_input = input(f"{Fore.CYAN}Enter line number to resume from (or 'back'): {Style.RESET_ALL}").strip()
                        if resume_input.lower() in ['back', 'exit', 'quit', 'q']:
                            return
                        if resume_input.isdigit():
                            start_line = int(resume_input)
                            if start_line >= 0:
                                print(f'{Fore.GREEN}Resuming from line {start_line}...{Style.RESET_ALL}')
                                break
                            else:
                                print(f'{Fore.RED}Line number must be 0 or greater.{Style.RESET_ALL}')
                        else:
                            print(f'{Fore.RED}Invalid number. Please enter a valid line number.{Style.RESET_ALL}')
                    break
                else:
                    print(f'{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}')
            print(f'\n{Fore.CYAN}Starting scan...{Style.RESET_ALL}')
            scanner.run_scan_fast(input_file, results_file, start_line)
            print(f'\n{Fore.GREEN}Scan completed! Results saved to {results_file}{Style.RESET_ALL}')
            while True:
                print(f'\n{Fore.CYAN}What would you like to do next?{Style.RESET_ALL}')
                print(f'{Fore.GREEN}1. Scan another file{Style.RESET_ALL}')
                print(f'{Fore.YELLOW}2. Return to main menu{Style.RESET_ALL}')
                choice = input(f'{Fore.CYAN}Enter your choice (1-2): {Style.RESET_ALL}').strip()
                if choice == '1':
                    break
                elif choice == '2':
                    return
                else:
                    print(f'{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}')
        except KeyboardInterrupt:
            print(f'\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}')
            return
        except Exception as e:
            print(f'{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}')
            time.sleep(2)
            return

async def create_anti_dpi_format():
    """DNS Resolver v6.2 - Deduplication & Complete Resolution"""
    RED_BOLD = '\x1b[1;31m'
    GREEN_BOLD = '\x1b[1;32m'
    YELLOW_BOLD = '\x1b[1;33m'
    CYAN_BOLD = '\x1b[1;36m'
    RESET = '\x1b[0m'

    @dataclass
    class Stats:
        processed: int = 0
        success: int = 0
        failed: int = 0
        written: int = 0
        duplicates: int = 0
        start_time: float = field(default_factory=time.time)
        lock: threading.Lock = field(default_factory=threading.Lock)

        def update(self, processed=0, success=0, failed=0, written=0, duplicates=0):
            with self.lock:
                self.processed += processed
                self.success += success
                self.failed += failed
                self.written += written
                self.duplicates += duplicates
                return (self.processed, self.success, self.failed, self.written, self.duplicates)

        @property
        def rate(self):
            with self.lock:
                elapsed = time.time() - self.start_time
                return self.processed / elapsed if elapsed > 0 else 0

    class ProgressDisplay:

        def __init__(self, total: int, unique: int):
            self.total = total
            self.unique = unique
            self.last_len = 0
            self.start = time.time()

        def fmt(self, n):
            if n >= 1000000000:
                return f'{n / 1000000000.0:.1f}B'
            if n >= 1000000:
                return f'{n / 1000000.0:.1f}M'
            if n >= 1000:
                return f'{n / 1000.0:.0f}K'
            return str(n)

        def show(self, stats: Stats, current: str=''):
            proc, succ, fail, writ, dup = stats.update()
            pct = min(100, int(proc * 100 / self.total)) if self.total else 0
            bar = '=' * (pct // 5) + '>' + ' ' * (20 - pct // 5 - 1)
            if pct == 100:
                bar = '=' * 20
            rate = stats.rate / 1000
            line = f'\r[{bar}] {pct:3d}% | {self.fmt(proc):>6} | ✓{self.fmt(succ):>5} | ✗{self.fmt(fail):>5} | 🔄{self.fmt(dup):>5} | 💾{self.fmt(writ):>5} | {rate:.1f}K/s | {current[:20]:<20}'
            sys.stdout.write('\r' + ' ' * self.last_len + '\r')
            sys.stdout.write(line)
            sys.stdout.flush()
            self.last_len = len(line)

        def done(self):
            sys.stdout.write('\n')

    class ImmediateWriter:

        def __init__(self, filename: str):
            self.filename = filename
            self.file = open(filename, 'w', buffering=1, encoding='utf-8', errors='replace')
            self.lock = threading.Lock()
            self._closed = False
            self.seen_hostnames = set()

        def write(self, hostname: str, ip: str) -> bool:
            with self.lock:
                if not self._closed:
                    if hostname in self.seen_hostnames:
                        return False
                    line = f'{hostname}\t{ip}\n'
                    self.file.write(line)
                    self.file.flush()
                    os.fsync(self.file.fileno())
                    self.seen_hostnames.add(hostname)
                    return True
            return False

        def close(self):
            with self.lock:
                if not self._closed:
                    self.file.close()
                    self._closed = True

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()

    def resolve_getaddrinfo(hostname: str) -> str:
        try:
            result = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
            if result:
                ip = result[0][4][0]
                return ip
        except socket.gaierror:
            pass
        except Exception:
            pass
        return None

    def count_lines_and_deduplicate(filename: str) -> tuple:
        size = os.path.getsize(filename)
        print(f'📊 Analyzing {size / 1000000000.0:.2f} GB file...')
        total = 0
        unique_hostnames = set()
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                hostname = line.strip()
                if hostname and (not hostname.startswith('#')):
                    total += 1
                    unique_hostnames.add(hostname)
        return (total, len(unique_hostnames))

    async def run_dns_resolver():
        print('=' * 85)
        print('   🌐 DNS RESOLVER v6.2 - Deduplication & Complete Resolution')
        print('   Clean format: hostname<tab>ip (no # prefix, no duplicates)')
        print('=' * 85)
        print()
        infile = input(f'{CYAN_BOLD}📥 Input file: {RESET}').strip().strip('"\'')
        if not os.path.exists(infile):
            print(f'{RED_BOLD}❌ File not found{RESET}')
            return
        outfile = input(f'{CYAN_BOLD}📤 Output file: {RESET}').strip().strip('"\'')
        if os.path.exists(outfile):
            if input(f'{YELLOW_BOLD}⚠️  Overwrite {outfile}? (y/N): {RESET}').lower() != 'y':
                return
        size = os.path.getsize(infile)
        print(f'\n📦 {size / 1000000000.0:.2f} GB input')
        if size > 20000000000.0:
            concurrency = 1000
            print('🚀 ULTRA mode: 1000 concurrent')
        elif size > 2000000000.0:
            concurrency = 500
            print('⚡ HIGH mode: 500 concurrent')
        else:
            concurrency = 200
            print('🔹 NORMAL mode: 200 concurrent')
        total, unique = count_lines_and_deduplicate(infile)
        duplicates = total - unique
        print(f'🎯 {total:,} total hostnames')
        print(f'📊 {unique:,} unique hostnames')
        if duplicates > 0:
            print(f'🔄 {duplicates:,} duplicates (will be resolved once)')
        print()
        if total == 0:
            print('❌ Empty file')
            return
        stats = Stats()
        progress = ProgressDisplay(total, unique)
        sem = asyncio.Semaphore(concurrency)
        shutdown = False
        seen_for_processing = set()

        def signal_handler(s, f):
            nonlocal shutdown
            shutdown = True
            print('\n⚠️  Shutting down gracefully...')
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        print('🚀 Resolving (results saved immediately, duplicates skipped)...')
        print('=' * 85)
        with ThreadPoolExecutor(max_workers=concurrency) as executor, ImmediateWriter(outfile) as writer:
            loop = asyncio.get_event_loop()
            pending = set()

            async def resolve_one(hostname: str):
                if shutdown:
                    return
                async with sem:
                    ip = await loop.run_in_executor(executor, resolve_getaddrinfo, hostname)
                    is_duplicate = False
                    written = False
                    if ip:
                        written = await loop.run_in_executor(executor, writer.write, hostname, ip)
                        if written:
                            stats.update(success=1, written=1)
                        else:
                            is_duplicate = True
                            stats.update(success=1, duplicates=1)
                    else:
                        stats.update(failed=1)
                    stats.update(processed=1)
                    if stats.processed % 10 == 0:
                        progress.show(stats, hostname)
            with open(infile, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    if shutdown:
                        break
                    hostname = line.strip()
                    if not hostname or hostname.startswith('#'):
                        continue
                    if hostname in seen_for_processing:
                        stats.update(processed=1, duplicates=1)
                        continue
                    seen_for_processing.add(hostname)
                    task = asyncio.create_task(resolve_one(hostname))
                    pending.add(task)
                    if len(pending) >= concurrency:
                        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
                        for t in done:
                            try:
                                await t
                            except:
                                pass
            if pending and (not shutdown):
                await asyncio.gather(*pending, return_exceptions=True)
        progress.done()
        proc, succ, fail, writ, dup = stats.update()
        elapsed = time.time() - stats.start_time
        print('=' * 85)
        print(f'✅ COMPLETE')
        print(f'   Total processed: {proc:,}')
        print(f'   Unique hostnames: {unique:,}')
        print(f'   Successful resolutions: {succ:,}')
        print(f'   Failed resolutions: {fail:,}')
        print(f'   Duplicates skipped: {dup:,}')
        print(f'   Written to file: {writ:,}')
        print(f'   Time: {elapsed / 60:.1f} minutes @ {stats.rate:.0f}/s')
        if os.path.exists(outfile):
            fsize = os.path.getsize(outfile)
            print(f'   Output: {outfile} ({fsize / 1000000.0:.1f} MB)')
            print(f'\n📄 Verifying output...')
            with open(outfile, 'r', encoding='utf-8') as f:
                output_lines = f.readlines()
                output_hostnames = set()
                for line in output_lines:
                    hostname = line.split('\t')[0] if '\t' in line else line.strip()
                    output_hostnames.add(hostname)
                if len(output_lines) == len(output_hostnames):
                    print(f'   ✅ No duplicates found in output ({len(output_lines):,} lines)')
                else:
                    print(f'   ⚠️  Found {len(output_lines) - len(output_hostnames)} duplicates in output')
            print(f'\n📄 Sample output:')
            with open(outfile, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= 3:
                        break
                    print(f'   {line.strip()}')
    while True:
        clear_screen()
        print(f"{CYAN_BOLD}{'=' * 60}{RESET}")
        print(f'{GREEN_BOLD}   CREATE FILE FORMAT FOR ANTI DPI (DNS RESOLVER v6.2){RESET}')
        print(f"{CYAN_BOLD}{'=' * 60}{RESET}")
        print()
        try:
            await run_dns_resolver()
        except KeyboardInterrupt:
            print(f'\n{YELLOW_BOLD}⚠️  Interrupted{RESET}')
        except Exception as e:
            print(f'\n{RED_BOLD}💥 Error: {e}{RESET}')
        print()
        while True:
            print(f'{CYAN_BOLD}Options:{RESET}')
            print(f'{GREEN_BOLD}1. Run another resolution{RESET}')
            print(f'{YELLOW_BOLD}2. Return to main menu{RESET}')
            choice = input(f'{CYAN_BOLD}Enter your choice (1-2): {RESET}').strip()
            if choice == '1':
                break
            elif choice == '2':
                return
            else:
                print(f'{RED_BOLD}Invalid choice. Please enter 1 or 2.{RESET}')

def option_12_exit():
    print(f'\n{Fore.YELLOW}Exiting program...{Style.RESET_ALL}')
    try:
        state_data = {'last_exit': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'results_file': RESULTS_FILE, 'remaining_days': days_remaining()}
        with open(STATE_FILE, 'w') as f:
            json.dump(state_data, f, indent=2)
        print(f'{Fore.GREEN}State saved successfully.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.YELLOW}Warning: Could not save state: {e}{Style.RESET_ALL}')
    try:
        if 'LAST_RUN_FILE' in globals():
            update_last_run_date()
    except:
        pass
    print(f'{Fore.CYAN}Goodbye!{Style.RESET_ALL}')
    sys.exit(0)

async def main_menu():
    while True:
        clear_screen()
        try:
            term_width = shutil.get_terminal_size().columns
        except:
            term_width = 80
        border = '═' * (min(term_width, 80) - 2)
        print(f'{Fore.RED}{Style.BRIGHT}╔{border}╗{Style.RESET_ALL}')
        title_text = 'V5 SHIMUL SNI FINDER SCRIPT 2026 PREMIUM'
        print(f'{Fore.RED}{Style.BRIGHT}║{title_text.center(len(border))}║{Style.RESET_ALL}')
        print(f'{Fore.RED}{Style.BRIGHT}╚{border}╝{Style.RESET_ALL}')
        print()
        if term_width >= 75:
            logo = f'''{Fore.RED}{Style.BRIGHT}\n                _,.-----.,_\n               ,-~           ~-.\n              ,^___           ___^.\n            /~"   ~"   .   "~   "~\\\n           Y  ,--._    I    _.--.  Y\n            | Y     ~-. | ,-~     Y |\n            | |        }}:{{        | |\n            j l       / | \\       ! l\n         .-~  (__,.--" .^. "--.,__)  ~-.\n        (           / / | \\ \\           )\n         \\.____,   ~  \\/"\\/  ~   .____,/\n          ^.____                 ____.^\n             | |T ~\\  !   !  /~ T| |\n             | |l   _ _ _ _ _   !| |\n             | l \\/V V V V V V\\/ j |\n             l  \\ \\|_|_|_|_|_|/ /  !\n              \\  \\[T T T T T TI/  /\n               \\  `^-^-^-^-^-^'  /\n                \\               /\n                 \\.           ,/\n                   "^-.___,-^"{Style.RESET_ALL}'''
        else:
            logo = f'{Fore.RED}{Style.BRIGHT}\n      ▄▄▄▄▄▄▄▄▄▄▄\n     ▐░░░░░░░░░░░▌\n     ▐░█▀▀▀▀▀▀▀▀▀░▌\n     ▐░▌       ▐░▌\n     ▐░▌       ▐░▌\n     ▐░▌       ▐░▌\n      ▀▀▀▀▀▀▀▀▀▀▀▀\n{Style.RESET_ALL}'
        print(logo)
        print()
        remaining_days = days_remaining()
        print(f'{Fore.CYAN}{Style.BRIGHT}DAYS REMAINING: {Fore.GREEN}{_format_days()}{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}OWNER: https://t.me/shimul00889{Style.RESET_ALL}')
        print(f'{Fore.CYAN}GROUP: https://t.me/shimul00889{Style.RESET_ALL}')
        print()
        menu_options = [('1', 'IP SCANNER CIDR / MULTI-CIDR'), ('2', 'REVERSE IP SCANNER V5'), ('3', 'SUBDOMAIN GENERATOR'), ('4', 'FILE.TXT SCANNER (SMALL FILE)'), ('5', 'PROXY SCANNER'), ('6', 'DOMAIN EXTRACTOR'), ('7', 'CUSTOM PORT SCANNER (443,80,8080 etc)'), ('8', 'UNLIMITED SCANN_NO FREEZE (HOSTNAME:IP)'), ('9', 'DOMAIN FINDER ANY COUNTRY (e.g .ke,.org,.com)'), ('10', 'ANTI DPI SCANNER FILE.TXT'), ('11', 'CREATE FILE FORMAT FOR ANTI DPI (DNS RESOLVER)'), ('12', 'EXIT')]
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╔{' MAIN MENU V5 '.center(len(border), '═')}╗{Style.RESET_ALL}")
        for num, desc in menu_options:
            print(f'  {Fore.GREEN}{num}.{Style.RESET_ALL} {Fore.CYAN}{desc}{Style.RESET_ALL}')
        print(f"{Fore.MAGENTA}{'═' * min(term_width, 80)}{Style.RESET_ALL}")
        print()
        while True:
            try:
                choice = input(f'{Fore.CYAN}Select an option (1-12): {Style.RESET_ALL}').strip()
                if choice == '1':
                    await ip_scanner()
                    break
                elif choice == '2':
                    await reverse_ip_scanner_v2()
                    break
                elif choice == '3':
                    await tls_scanner()
                    break
                elif choice == '4':
                    await file_scanner()
                    break
                elif choice == '5':
                    proxy_scanner_main()
                    break
                elif choice == '6':
                    domain_extractor()
                    break
                elif choice == '7':
                    await custom_port_scanner()
                    break
                elif choice == '8':
                    unlimited_scanner_no_freeze()
                    break
                elif choice == '9':
                    await domain_finder()
                    break
                elif choice == '10':
                    await option_10_advanced_hostname_scanner()
                    break
                elif choice == '11':
                    await create_anti_dpi_format()
                    break
                elif choice == '12':
                    option_12_exit()
                    break
                else:
                    print(f'{Fore.RED}Invalid choice. Please select a valid option (1-12).{Style.RESET_ALL}')
            except KeyboardInterrupt:
                print(f'\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}')
                time.sleep(1)
                break
            except Exception as e:
                print(f'{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}')
                print(f'{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}')
                time.sleep(2)
                break

def run_engine():
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        f.write('Scan Results Log - V4.txt\n')
        f.write('=' * 50 + '\n')
        f.write(f'Scan session started: {datetime.datetime.now()}\n\n')
    asyncio.run(main_menu())

if __name__ == "__main__":
    run_engine()
