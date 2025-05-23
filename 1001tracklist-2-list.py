import requests
from bs4 import BeautifulSoup

def fetch_1001tracklist(url, debug=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    if debug:
        print(f"Ophalen URL: {url}")

    resp = requests.get(url, headers=headers)

    if debug:
        print(f"Status code: {resp.status_code}")

    if resp.status_code != 200:
        print("Fout bij ophalen pagina, check URL of internetverbinding.")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')

    tracks = soup.find_all("div", id=lambda x: x and x.startswith("tlp") and x.endswith("_content"))

    if debug:
        print(f"Aantal tracks gevonden: {len(tracks)}")
        if len(tracks) == 0:
            print("Geen track-divs gevonden, mogelijk is de HTML-structuur gewijzigd.")
    
    result = []
    for i, track_div in enumerate(tracks):
        if debug:
            print(f"\nTrack {i+1} HTML preview:\n{track_div.prettify()[:500]}")

        artiest = track_div.find("meta", itemprop="byArtist")
        titel = track_div.find("meta", itemprop="name")
        url_track = track_div.find("meta", itemprop="url")

        artiest_text = artiest['content'] if artiest else "Onbekende artiest"
        titel_text = titel['content'] if titel else "Onbekende track"
        url_text = f"https://www.1001tracklists.com{url_track['content']}" if url_track else None

        if debug:
            print(f"Artiest: {artiest_text}")
            print(f"Track: {titel_text}")
            print(f"URL: {url_text if url_text else 'Geen track URL'}")

        result.append((artiest_text, titel_text, url_text))
    
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Gebruik: python3 test.py <1001tracklist-url> [--debug] [--show-url]")
        sys.exit(1)

    url = sys.argv[1]
    debug = False
    show_url = False

    for arg in sys.argv[2:]:
        if arg == "--debug":
            debug = True
        elif arg == "--show-url":
            show_url = True

    tracks = fetch_1001tracklist(url, debug=debug)

    if not debug:
        for artiest, titel, url_track in tracks:
            if show_url and url_track:
                print(f"{artiest} - {titel} | {url_track}")
            else:
                print(f"{artiest} - {titel}")
