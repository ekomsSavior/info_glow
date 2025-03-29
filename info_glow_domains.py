from info_glow import pastel_print, baby_spinner, save_results
import subprocess

def domain_recon(domain):
    pastel_print(f"Running recon on: {domain}")
    baby_spinner("Looking up WHOIS & DNS")
    results = []

    try:
        whois = subprocess.getoutput(f"whois {domain}")
        results.append("[WHOIS INFO]")
        results.extend(whois.splitlines())
    except Exception as e:
        results.append(f"[ERROR] WHOIS failed: {e}")

    try:
        dig = subprocess.getoutput(f"dig {domain} ANY +short")
        results.append("\n[DNS RECORDS]")
        results.extend(dig.splitlines())
    except Exception as e:
        results.append(f"[ERROR] DIG failed: {e}")

    return results

def handle_domain():
    domain = input("Enter domain (no https): ")
    results = domain_recon(domain)
    for line in results:
        pastel_print(line)
    save_results(domain, results, tag="domain")
    print("")
