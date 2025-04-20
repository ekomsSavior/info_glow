import re
import subprocess
from info_glow import pastel_print, baby_spinner, save_results

def is_valid_domain(domain):
    # Basic domain validation
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$"
    return re.match(pattern, domain)

def run_command(cmd, timeout=10):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip().splitlines()
    except subprocess.TimeoutExpired:
        return [f"[ERROR] Command timed out: {cmd}"]
    except Exception as e:
        return [f"[ERROR] Command failed: {cmd} :: {e}"]

def domain_recon(domain):
    pastel_print(f"🔍 Running recon on: {domain}")
    baby_spinner("Looking up WHOIS & DNS...")

    results = []

    if not is_valid_domain(domain):
        results.append(f"[ERROR] Invalid domain format: {domain}")
        return results

    results.append("[WHOIS INFO]")
    results.extend(run_command(f"whois {domain}"))

    results.append("\n[DNS RECORDS]")
    results.extend(run_command(f"dig {domain} ANY +short"))

    return results

def handle_domain():
    domain = input("🌐 Enter domain (no https): ").strip()
    results = domain_recon(domain)
    for line in results:
        pastel_print(line)
    save_results(domain, results, tag="domain")
    print("")
