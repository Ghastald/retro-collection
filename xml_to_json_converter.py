
import os
import xml.etree.ElementTree as ET
import json
import re

INPUT_FOLDER = "./xml"
OUTPUT_FOLDER = "./data"
IMAGE_FOLDER = "./images"

def sanitize_filename(path):
    name = os.path.basename(path)
    name = re.sub(r'\.(zip|7z|rar|chd|gba|gb|nes|sfc|bin|iso|cue|img)$', '', name, flags=re.IGNORECASE)
    return name

def extract_game_data(xml_path, platform_code):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    games = []

    for game in root.findall("Game"):
        title = game.findtext("Title", default="").strip()
        if re.search(r"(?i)(disc|cd|disk)[\s_-]?[2-9]", title):
            continue  # skip Disc 2+

        genre = game.findtext("Genre", default="").strip()
        release_date = game.findtext("ReleaseDate", default="").strip()
        developer = game.findtext("Developer", default="").strip()
        publisher = game.findtext("Publisher", default="").strip()
        notes = game.findtext("Notes", default="").strip()
        path = game.findtext("ApplicationPath", default="").strip()

        clean_name = sanitize_filename(path)
        image_path = f"/images/{platform_code}/{clean_name}.png"

        games.append({
            "title": title,
            "genre": genre,
            "release_date": release_date,
            "developer": developer,
            "publisher": publisher,
            "synopsis": notes,
            "image": image_path
        })

    return games

def convert_all():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".xml"):
            platform_code = file.lower().split(" ")[0][:4]  # crude platform guessing
            input_path = os.path.join(INPUT_FOLDER, file)
            output_path = os.path.join(OUTPUT_FOLDER, f"{platform_code}.json")
            games = extract_game_data(input_path, platform_code)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(games, f, indent=2, ensure_ascii=False)
            print(f"✅ {file} → {platform_code}.json with {len(games)} games")

if __name__ == "__main__":
    convert_all()
