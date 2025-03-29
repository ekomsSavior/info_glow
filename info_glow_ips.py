from info_glow import pastel_print, baby_spinner, save_results
from urllib.parse import quote
import requests
from colorama import Fore, Style

def search_ip(ip):
    pastel_print(f"Searching IP: {ip}")
    baby_spinner("Running geo IP lookup")
    results = []

    try:
        res = requests.get(f"http://ip-api.com/json/{quote(ip)}")
        data = res.json()
        for key in ["query", "country", "regionName", "city", "zip", "lat", "lon", "isp", "org", "as"]:
            results.append(f"{key}: {data.get(key)}")
    except Exception as e:
        results.append(f"[ERROR] IP lookup failed: {e}")

    # ✨ That’sThem Link ✨
    thatsthem_link = f"https://thatsthem.com/ip/{quote(ip)}"
    results.append("")
    results.append(f"Click for full public record lookup:")
    results.append(thatsthem_link)

    return results

def handle_ips():
    raw = input("Enter IP address(es), comma-separated: ")
    for ip in [i.strip() for i in raw.split(",")]:
        results = search_ip(ip)
        for line in results:
            if "thatsthem.com" in line:
                print(Fore.MAGENTA + "🔎 " + line + Style.RESET_ALL)
            else:
                pastel_print(line)
        save_results(ip, results, tag="ip")
        print("")
