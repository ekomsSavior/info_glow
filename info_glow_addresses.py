from info_glow import pastel_print, baby_spinner, save_results
from urllib.parse import quote
from colorama import Fore, Style

def search_address(address):
    pastel_print(f"Searching address: {address}")
    baby_spinner("Generating dork suggestions")
    results = []

    results.append(f"[MAP] https://www.google.com/maps/search/{quote(address)}")
    results.append(f"[DORK] site:zillow.com \"{address}\"")
    results.append(f"[DORK] site:facebook.com/events \"{address}\"")
    results.append(f"[DORK] site:linkedin.com \"{address}\"")
    results.append(f"[DORK] site:nextdoor.com \"{address}\"")

    # ✨ That’sThem Link ✨
    thatsthem_link = f"https://thatsthem.com/address/{quote(address)}"
    results.append("")
    results.append("Click for full public record lookup:")
    results.append(thatsthem_link)

    return results

def handle_addresses():
    address = input("Enter physical address: ")
    results = search_address(address)
    for line in results:
        if "thatsthem.com" in line:
            print(Fore.MAGENTA + "🔎 " + line + Style.RESET_ALL)
        else:
            pastel_print(line)
    save_results(address, results, tag="address")
    print("")

