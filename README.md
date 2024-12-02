# Http-MultiFlooder
This method is a **mixed multi-layer attack** combining **asynchronous HTTPS flooding** and **proxied raw socket flooding** to target web servers. It is designed to maximize impact by leveraging both advanced HTTP request simulation and raw traffic generation.

#### Key Features:  
1. **Asynchronous HTTPS Flooding**:  
   - Utilizes `aiohttp` to send a massive number of HTTPS requests asynchronously.  
   - Customizable headers simulate real-world browser traffic, including user agents, caching, and platform-specific settings.  
   - Proxies are integrated to maintain anonymity and bypass IP filtering.

2. **Proxied Socket Flooding**:  
   - Sends raw HTTP requests directly through socket connections.  
   - Dynamic URL parsing ensures requests include the correct paths and headers.  
   - Advanced headers mimic real browser behavior to evade detection.

3. **Stealth and Adaptability**:  
   - Requests include realistic browser-like attributes (e.g., `sec-fetch-mode`, `sec-fetch-site`, `User-Agent`, etc.).  
   - HTTPS support ensures compatibility with secure servers.  
   - Proxy rotation spreads traffic across multiple IPs to avoid blocking.

#### How It Works:  
- The script first parses the target URL to ensure valid path handling.  
- For HTTPS flooding, it asynchronously sends requests with randomized headers and proxies.  
- For socket flooding, it opens raw connections and floods the target with customized HTTP requests through proxies.

This method is powerful, flexible, and designed to stress-test web servers using a combination of high-concurrency HTTPS requests and raw socket-level floods.
"""

### Install the requirements
```
pip install -r requirements.txt
```
### Usage
```
python start.py <target> <port> <threads> <proxyfile>
```
- Example: python start.py https://website.com 443 6 proxy.txt
- Good proxies more power, recommend VPS 4cores or 8cores
