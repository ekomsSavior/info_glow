from info_glow import pastel_print, baby_spinner, save_results

def search_plate(plate):
    pastel_print(f"Searching license plate: {plate}")
    baby_spinner("Suggesting recon sources")
    return [
        f"[DORK] site:findbyplate.com \"{plate}\"",
        f"[TIP] Try searching on local DMV or state government sites",
        f"[DORK] site:reddit.com \"{plate}\" OR car forums",
        f"[DORK] site:autoblog.com \"{plate}\"",
    ]

def handle_plates():
    plate = input("Enter license plate: ")
    results = search_plate(plate)
    for line in results:
        pastel_print(line)
    save_results(plate, results, tag="plate")
    print("")
