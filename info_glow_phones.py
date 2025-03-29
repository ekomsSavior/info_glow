from info_glow import pastel_print, baby_spinner, save_results
from urllib.parse import quote
import requests
from colorama import Fore, Style

def search_phone(phone):
    pastel_print(f"Searching phone: {phone}")
    baby_spinner("Checking format & region")
    results = []

    try:
        res = requests.get(
            f"https://api.apilayer.com/number_verification/validate?number={quote(phone)}",
            headers={"apikey": "demo"}  # You can add your real API key here
        )
        if res.status_code == 200:
            data = res.json()
            results.append(f"Country: {data.get('country_name')}")
            results.append(f"Carrier: {data.get('carrier')}")
            results.append(f"Line type: {data.get('line_type')}")
        else:
            results.append("[ERROR] Could not validate phone.")
    except Exception as e:
        results.append(f"[ERROR] Phone lookup failed: {e}")

    # ✨ That’sThem Link ✨
    thatsthem_link = f"https://thatsthem.com/phone/{quote(phone)}"
    results.append("")
    results.append(f"Click for full public record lookup:")
    results.append(thatsthem_link)

    return results

def handle_phones():
    raw = input("Enter phone number(s), comma-separated: ")
    for phone in [p.strip() for p in raw.split(",")]:
        results = search_phone(phone)
        for line in results:
            if "thatsthem.com" in line:
                print(Fore.MAGENTA + "🔎 " + line + Style.RESET_ALL)
            else:
                pastel_print(line)
        save_results(phone, results, tag="phone")
        print("")
