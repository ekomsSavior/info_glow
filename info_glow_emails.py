from info_glow import pastel_print, baby_spinner, save_results
import requests
import hashlib
from urllib.parse import quote

import os
import json

CONFIG_PATH = os.path.expanduser("~/.info_glow_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)


def search_email(email):
    pastel_print(f"Searching email: {email}")
    baby_spinner("Checking PGP & Gravatar")
    results = []

    # PGP Key
    try:
        res = requests.get(f"https://keys.openpgp.org/vks/v1/by-email/{quote(email)}")
        if "-----BEGIN PGP PUBLIC KEY BLOCK-----" in res.text:
            results.append("[FOUND] PGP public key available.")
        else:
            results.append("[NOT FOUND] No PGP public key found.")
    except Exception as e:
        results.append(f"[ERROR] PGP check failed: {e}")

    # Gravatar
    try:
        h = hashlib.md5(email.lower().strip().encode()).hexdigest()
        g_url = f"https://www.gravatar.com/avatar/{h}?d=404"
        g_res = requests.get(g_url)
        if g_res.status_code == 200:
            results.append(f"[FOUND] Gravatar profile: {g_url}")
        else:
            results.append("[NOT FOUND] No Gravatar profile.")
    except Exception as e:
        results.append(f"[ERROR] Gravatar failed: {e}")

    # Hunter-style tip + Dorking
    domain = email.split("@")[-1]
    results.append(f"[TIP] Check: https://hunter.io/email-finder/{domain}")
    results.append(f"[DORK] site:pastebin.com \"{email}\"")
    results.append(f"[DORK] site:telegram.org \"{email}\"")
    results.append(f"[DORK] site:exploit.intext:\"{email}\"")

    # Optional: HaveIBeenPwned
    config = load_config()
    hibp_key = config.get("hibp_api_key")
    if not hibp_key:
        pastel_print("No HIBP API key found. Want to add it now? (enter to skip)")
        hibp_key = input("HIBP Key: ")
        if hibp_key:
            config["hibp_api_key"] = hibp_key
            save_config(config)

    if hibp_key:
        baby_spinner("Checking HaveIBeenPwned")
        try:
            headers = {"hibp-api-key": hibp_key, "User-Agent": "info_glow"}
            res = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=headers)
            if res.status_code == 200:
                breaches = res.json()
                results.append(f"[BREACHED] {len(breaches)} breach(es):")
                for b in breaches:
                    results.append(f" - {b['Name']}")
            elif res.status_code == 404:
                results.append("[SAFE] No breaches found 🎉")
            else:
                results.append(f"[UNKNOWN] HIBP status: {res.status_code}")
        except Exception as e:
            results.append(f"[ERROR] HIBP failed: {e}")

    return results

def handle_emails():
    raw = input("Enter email(s), comma-separated: ")
    for email in [e.strip() for e in raw.split(",")]:
        results = search_email(email)
        for line in results:
            pastel_print(line)
        save_results(email, results, tag="email")
        print("")
