import requests
import json
import sys
import os

from tqdm import tqdm

ASSETS_PATH = "./assets"
IMAGE_SOURCE_URL = "https://multi-deckplanet.us-southeast-1.linodeobjects.com/dbs_masters" 
# https://multi-deckplanet.us-southeast-1.linodeobjects.com/dbs_masters/BT13-037.webp

CARD_TYPES_MAPPING = {
    "LEADER":   "Leader",
    "BATTLE":   "Main_Deck",
    "EXTRA":    "Main_Deck",
    "UNISON":   "Main_Deck",
    "Z-BATTLE": "Z_Deck",
    "Z-EXTRA":  "Z_Deck",
    "Z-UNISON": "Z_Deck",
    "Z-LEADER": "Z_Deck"
}

def download_image(url: str, path: str):
    r = requests.get(url)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
        
        return True
    return False

def compare_series_cards(cards, card_series_metadata_path):
    with open(card_series_metadata_path, 'r', encoding='utf-8') as f:
        existing_cards = json.load(f)
        if existing_cards != cards:
            return True
        
        return False

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    print("Please provide a valid input file path.")
    sys.exit(1)

if input_file == "" or input_file is None:
    print("Please provide a valid input file path.")
    sys.exit(1)

if not os.path.exists(input_file):
    print(f"Input file '{input_file}' does not exist.")
    sys.exit(1)


cards_grouped_by_series = {}
with open(input_file, 'r', encoding='utf-8') as f:
    cards_data = json.load(f)

    for card in cards_data:
        series : str = card.get('card_series', 'Unknown Series')
        series_norm = series.replace(" ", "").strip()
        img_url = f'{IMAGE_SOURCE_URL}/{card["img_link"]}.webp'

        # card_series_path = f"{ASSETS_PATH}/{series_norm}"
        # if not os.path.exists(card_series_path):
        #     os.mkdir(card_series_path, exist_ok=True)

        card_entry = {
            f'{card["card_number"]}': {
                'id': card['card_number'],
                'face': {
                    'front': {
                        'name': card['card_name'],
                        'type': CARD_TYPES_MAPPING[card['card_type']],
                        'cost': card['card_energy_cost'],
                        'power': card['card_power'],
                        'Energy_cost': card['card_energy_cost'],
                        'image': img_url,
                        'isHorizontal': card['card_type'] == 'Z-EXTRA'
                    }
                },
                'Name': card['card_name'],
                'Type': card['card_type'],
                'Rarity': card['card_rarity'],
                'image': img_url,
                'Power': card['card_power'],
                'Color': card['card_color'],
                #'Energy_cost': card['card_energy_cost'],
                'Combo_cost': card['card_combo_cost'],
                'Combo_power': card['card_combo_power'],
                'Series': series,
                'Character': card['card_character'] if card['card_character'] is not None else [],
                #'era': card['card_era'],
                'Traits': card['card_traits'],
                'Banned': card['is_banned'],
                #'limited': card['is_limited'],
                #'limited_to': card['limited_to'],
                'Keywords': card['keywords'],
                #'z_energy_cost': card['z_energy_cost'],
                #'back_name': card['card_back_name'],
                #'back_power': card['card_back_power'],
                #'back_character': card['card_back_character'],
                #'back_era': card['card_back_era'],
                #'back_traits': card['card_back_traits'],
            }
        }

        if card['card_type'] == 'LEADER':
            card_entry[f'{card["card_number"]}']['face']['back'] = {
                'name': card['card_back_name'],
                'type': CARD_TYPES_MAPPING[card['card_type']],
                'cost': card['card_energy_cost'],
                'power': card['card_back_power'],
                'image': f'{IMAGE_SOURCE_URL}/{card["img_link"]}_b.webp',
                'isHorizontal': False
            }
        cards_grouped_by_series.setdefault(series_norm, {}).update(card_entry)

for series, cards in tqdm(cards_grouped_by_series.items(), desc="Generating card assets by series"):
    card_series_path = f"{ASSETS_PATH}/{series}"
    card_series_metadata_path = f'{card_series_path}/cards.json'
    if not os.path.exists(card_series_path) or not os.path.exists(card_series_metadata_path):
        os.makedirs(card_series_path, exist_ok=True)
        with open(card_series_metadata_path, 'w', encoding='utf-8') as f:
            json.dump(cards, f, indent=4, ensure_ascii=False)
    else:
        has_diff = compare_series_cards(cards, card_series_metadata_path)
        if has_diff:
            with open(card_series_metadata_path, 'w', encoding='utf-8') as f:
                json.dump(cards, f, indent=4, ensure_ascii=False)

    for card_id, card in tqdm(cards.items(), desc=f"Downloading images for series {series}", leave=False):
        card_image_path = f"{card_series_path}/{card['id']}.webp"
        if not os.path.exists(card_image_path):
            download_image(url=card['image'], path=card_image_path)
