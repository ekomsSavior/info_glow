from info_glow import pastel_print, baby_spinner, save_results
from urllib.parse import quote
from colorama import Fore, Style

def search_vin(vin):
    pastel_print(f"Searching VIN: {vin}")
    baby_spinner("Decoding vehicle info")
    results = []

    results.append(f"[DECODE] https://vpic.nhtsa.dot.gov/decoder/?vin={quote(vin)}")
    results.append(f"[DORK] site:vehiclehistory.com \"{vin}\"")
    results.append(f"[DORK] site:carfax.com \"{vin}\"")
    results.append(f"[TIP] Look for VINs on insurance, dealer, or auction sites")

    # ✨ That’sThem Link ✨
    thatsthem_link = f"https://thatsthem.com/search?q={quote(vin)}"
    results.append("")
    results.append("Click for full public record lookup:")
    results.append(thatsthem_link)

    return results

def handle_vins():
    vin = input("Enter VIN: ")
    results = search_vin(vin)
    for line in results:
        if "thatsthem.com" in line:
            print(Fore.MAGENTA + "🔎 " + line + Style.RESET_ALL)
        else:
            pastel_print(line)
    save_results(vin, results, tag="vin")
    print("")
