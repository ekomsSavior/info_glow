from info_glow import pastel_print, baby_spinner, save_results
import requests
from urllib.parse import quote

def search_username(username):
    pastel_print(f"Searching username: {username}")
    safe = quote(username)
    platforms = {
        "GitHub": f"https://github.com/{safe}",
        "Twitter": f"https://twitter.com/{safe}",
        "Instagram": f"https://instagram.com/{safe}",
        "Reddit": f"https://www.reddit.com/user/{safe}",
        "TikTok": f"https://www.tiktok.com/@{safe}",
        "YouTube": f"https://www.youtube.com/@{safe}",
        "Medium": f"https://medium.com/@{safe}",
        "Pinterest": f"https://www.pinterest.com/{safe}/",
        "Tumblr": f"https://{safe}.tumblr.com",
        "Dev.to": f"https://dev.to/{safe}",
        "VK": f"https://vk.com/{safe}",
        "Mastodon": f"https://mastodon.social/@{safe}",
        "Keybase": f"https://keybase.io/{safe}",
        "HackerNews": f"https://news.ycombinator.com/user?id={safe}",
        "Product Hunt": f"https://www.producthunt.com/@{safe}",
    }

    results = []
    baby_spinner("Checking platforms")
    for site, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results.append(f"[FOUND] {site}: {url}")
            elif response.status_code == 404:
                results.append(f"[NOT FOUND] {site}: {url}")
            else:
                results.append(f"[UNKNOWN] {site}: {url} (Status: {response.status_code})")
        except Exception as e:
            results.append(f"[ERROR] {site}: {url} - {e}")
    return results

def handle_usernames():
    raw = input("Enter username(s), comma-separated: ")
    for username in [u.strip() for u in raw.split(",")]:
        results = search_username(username)
        for line in results:
            pastel_print(line)
        save_results(username, results, tag="user")
        print("")
