#!/usr/bin/env python3

import os
import json
import time
import hashlib
import subprocess
from datetime import datetime
from urllib.parse import quote
import requests
from colorama import Fore, Style, init

init()

CONFIG_PATH = os.path.expanduser("~/.info_glow_config.json")

SERVICE_TAGS = {
    "bugcrowd": "Bug Bounty (Bugcrowd)",
    "google-site-verification": "Google Site Verification",
    "apple-domain-verification": "Apple Verification",
    "microsoft": "Microsoft Cloud",
    "ms-domain-verification": "Microsoft Verification",
    "atlassian": "Atlassian Services",
    "onetrust": "Compliance (OneTrust)",
    "logmein": "Remote Access (LogMeIn)",
    "adobe": "Adobe Cloud",
    "teamviewer": "Remote Access (TeamViewer)",
    "docker": "Docker Integration",
    "spf": "Email Sender Verification",
    "sendgrid": "SendGrid Email Infra",
    "zendesk": "Zendesk Support",
    "qualtrics": "Qualtrics Survey Tool",
    "ultipro": "HR Platform (UltiPro)",
    "knowbe4": "Security Awareness (KnowBe4)",
    "akam": "Akamai CDN",
    "ultradns": "UltraDNS Provider"
}

def pastel_banner():
    print(Fore.MAGENTA + r"""
██╗███╗   ██╗███████╗ ██████╗      ██████╗ ██╗      ██████╗ ██╗    ██╗    
██║████╗  ██║██╔════╝██╔═══██╗    ██╔════╝ ██║     ██╔═══██╗██║    ██║    
██║██╔██╗ ██║█████╗  ██║   ██║    ██║  ███╗██║     ██║   ██║██║ █╗ ██║    
██║██║╚██╗██║██╔══╝  ██║   ██║    ██║   ██║██║     ██║   ██║██║███╗██║    
██║██║ ╚████║██║     ╚██████╔╝    ╚██████╔╝███████╗╚██████╔╝╚███╔███╔╝    
╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝      ╚═════╝ ╚══════╝ ╚═════╝  ╚══╝╚══╝     
                    info glow v0.8 – Spectral Lens
                         by ekoms savior
""" + Style.RESET_ALL)

def show_menu():
    print(Fore.CYAN + """
[1] Search username(s)
[2] Search email(s)
[3] Domain recon
[4] Phone number search
[5] IP address search
[6] Physical address search
[7] License plate search
[8] VIN number search
[9] Quit
""" + Style.RESET_ALL)

def pastel_print(msg):
    print(Fore.LIGHTMAGENTA_EX + "★ " + msg + Style.RESET_ALL)

def save_results(name, results, tag="info_glow"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("output/reports", exist_ok=True)

    txt_path = f"output/reports/{tag}_{name}_{timestamp}.txt"
    md_path = f"output/reports/{tag}_{name}_{timestamp}.md"
    html_path = f"output/reports/{tag}_{name}_{timestamp}.html"

    with open(txt_path, "w") as f:
        f.write(f"Info Glow OSINT Report for: {name}\n\n")
        for line in results:
            f.write(line + "\n")

    with open(md_path, "w") as f:
        f.write(f"# Info Glow OSINT Report: `{name}`\n\n")
        for line in results:
            f.write(f"- {line}\n")

    with open(html_path, "w") as f:
        f.write(f"<html><head><title>Info Glow Report - {name}</title></head><body>")
        f.write(f"<h2>Info Glow OSINT Report for <code>{name}</code></h2><ul>")
        for line in results:
            f.write(f"<li>{line}</li>")
        f.write("</ul></body></html>")

    pastel_print(f"Report saved as:\n  📄 {txt_path}\n  📝 {md_path}\n  🌐 {html_path}")

def baby_spinner(text="Scanning"):
    print(Fore.YELLOW + text + " ", end="", flush=True)
    for dot in "⋆⋆⋆⋆":
        print(dot, end="", flush=True)
        time.sleep(0.3)
    print(Style.RESET_ALL)

def auto_label_dns(dns_lines):
    labeled = []
    for line in dns_lines:
        tag_found = False
        for keyword, label in SERVICE_TAGS.items():
            if keyword.lower() in line.lower():
                labeled.append(f"{line}  →  {label}")
                tag_found = True
                break
        if not tag_found:
            labeled.append(line)
    return labeled

def domain_recon(domain):
    pastel_print(f"Running recon on: {domain}")
    baby_spinner("WHOIS, DNS, Nmap & Nikto incoming ✨")
    results = []

    # WHOIS
    try:
        whois = subprocess.getoutput(f"whois {domain}")
        results.append("[WHOIS INFO]")
        results.extend(whois.splitlines())
    except Exception as e:
        results.append(f"[ERROR] WHOIS failed: {e}")

    # DNS
    try:
        dig_raw = subprocess.getoutput(f"dig {domain} ANY +short")
        dns_lines = dig_raw.splitlines()
        results.append("\n[DNS RECORDS]")
        labeled_dns = auto_label_dns(dns_lines)
        results.extend(labeled_dns)
    except Exception as e:
        results.append(f"[ERROR] DIG failed: {e}")

    # NMAP
    try:
        nmap_scan = subprocess.getoutput(f"nmap -T4 -Pn -F {domain}")
        results.append("\n[NMAP SCAN - Common Ports]")
        results.extend(nmap_scan.splitlines())
    except Exception as e:
        results.append(f"[ERROR] Nmap failed: {e}")

    # NIKTO
    try:
        nikto = subprocess.getoutput(f"nikto -host {domain}")
        results.append("\n[WEB SCAN - Nikto Results]")
        results.extend(nikto.splitlines())
    except Exception as e:
        results.append(f"[ERROR] Nikto failed: {e}")

    return results

def main():
    pastel_banner()
    while True:
        show_menu()
        choice = input(Fore.YELLOW + "Choose your sparkle option: " + Style.RESET_ALL)

        if choice == "1":
            from info_glow_usernames import handle_usernames
            handle_usernames()

        elif choice == "2":
            from info_glow_emails import handle_emails
            handle_emails()

        elif choice == "3":
            domain = input("Enter domain (no https): ")
            results = domain_recon(domain)
            for line in results:
                pastel_print(line)
            save_results(domain, results, tag="domain")
            print("")

        elif choice == "4":
            from info_glow_phones import handle_phones
            handle_phones()

        elif choice == "5":
            from info_glow_ips import handle_ips
            handle_ips()

        elif choice == "6":
            from info_glow_addresses import handle_addresses
            handle_addresses()

        elif choice == "7":
            from info_glow_plates import handle_plates
            handle_plates()

        elif choice == "8":
            from info_glow_vins import handle_vins
            handle_vins()

        elif choice == "9":
            pastel_print("Bye bye for now! Stay sparkly ✨")
            break

        else:
            pastel_print("That’s not a valid option, cutie!")

if __name__ == "__main__":
    main()
