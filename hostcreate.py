import pandas as pd
import requests
import json

ZABBIX_URL = "http://zabbix.url.com/zabbix/api_jsonrpc.php" 
USERNAME = "USERNAME"  
PASSWORD = "PASSWORD"
def login_to_zabbix():
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "method": "user.login", 
        "params": {
            "username": USERNAME, 
            "password": PASSWORD  
        },
        "id": 1,
        "auth": None
    }

    response = requests.post(ZABBIX_URL, headers=headers, json=data)
    result = response.json()
    if "result" in result:
        print("Zabbix'e başarıyla giriş yapıldı!",result["result"])
        return result["result"]
    else:
        print("Zabbix'e giriş yapılamadı. Hata:", result)
        return None

def add_host_to_zabbix(auth_token, hostname, ip, port):
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": hostname, 
            "interfaces": [{
                "type": 1,  # Zabbix agent (ICMP ping için agent kullanıyoruz)
                "main": 1,
                "useip":1,
                "ip": str(ip),  
                "dns": "", 
                "port": port 
            }],
            "groups": [{
                "groupid": 10 # Zabbix'teki grup ID'si 
            }],
            "templates": [{
                "templateid": "10"  # Geçerli bir template ID'si
            }],
            "status": 0  # Host aktif
        },
        "auth": auth_token,
        "id": 1
    }

    response = requests.post(ZABBIX_URL, headers=headers, json=data)
    result = response.json()
    print("API Yanıtı:", json.dumps(result, indent=4))

    return result

def read_excel(file_path):
    df = pd.read_excel(file_path)
    print("Excel sütun adları:", df.columns) 
    return df

def main():
    auth_token = login_to_zabbix()

    if not auth_token:
        return

    file_path = "excledosyaniz.xlsx" 
    df = read_excel(file_path)

    for index, row in df.iterrows():
        hostname = row['Hostname']  # Excel'deki 'Hostname' sütunu
        ip = row['IP']  # Excel'deki 'IP' sütunu
        port = row['Port']  # Excel'deki 'Port' sütunu

        print(f"{hostname} ({ip}) ekleniyor...")

        result = add_host_to_zabbix(auth_token, hostname, ip, port)
        if "result" in result:
            print(f"Host {hostname} başarıyla eklendi!")
        else:
            print(f"{hostname} eklenirken bir hata oluştu: {result}")

if __name__ == "__main__":
    main()
