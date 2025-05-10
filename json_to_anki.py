import json, html, os
from genanki import Model, Note, Deck, Package

# ------------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------------
JSON_FILE = "obesity_p2.json"  # file inside ./input/ (without .json extension)
DECK_NAME = "Adipose Biology"
MODEL_ID  = 1607392319                 # keep constant; change only if you rebuild note type
MEDIA_DIR = []                         # list of media files if you later add audio/images

# ------------------------------------------------------------------
# 2. NOTE (CARD) MODEL
# ------------------------------------------------------------------
model = Model(
    MODEL_ID,
    'Basic Markdown Model',
    fields=[
        {'name': 'Front'},       # 0 – Question
        {'name': 'Back'},        # 1 – Answer with markdown formatting
    ],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Front}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
    }],
    css='''
        .card {
            font-family: Arial, sans-serif;
            font-size: 16px;
            text-align: left;
            background-color: #FFFFFF;
            line-height: 1.4;
        }
        strong, b {
            font-weight: bold;
        }
        ul, ol {
            margin-left: 20px;
            padding-left: 0;
        }
        li {
            margin-bottom: 5px;
        }
    '''
)

# ------------------------------------------------------------------
# 3. UNIQUE DECK ID
# ------------------------------------------------------------------
def generate_deck_id(name: str) -> int:
    base = 2_147_483_647          # largest 32‑bit signed int
    return abs(hash(name)) % base

deck = Deck(generate_deck_id(DECK_NAME), DECK_NAME)

# Function to sanitize tags (replace spaces with underscores)
def sanitize_tags(tags):
    return [tag.replace(" ", "_") for tag in tags]

# ------------------------------------------------------------------
# 4. READ JSON AND CREATE NOTES
# ------------------------------------------------------------------
json_path = f"./input/{JSON_FILE}"
with open(json_path, encoding="utf-8") as f:
    cards = json.load(f)
    
    for card in cards:
        # Extract fields, apply HTML escaping
        front = html.escape(card['front'])
        back = html.escape(card['back'])
        
        # Create the note
        note = Note(
            model=model,
            fields=[front, back]
        )
        
        # Add tags if present, replacing spaces with underscores
        if 'tags' in card:
            note.tags = sanitize_tags(card['tags'])
            
        deck.add_note(note)

# ------------------------------------------------------------------
# 5. WRITE THE .APKG PACKAGE
# ------------------------------------------------------------------
out_dir = "./output"; os.makedirs(out_dir, exist_ok=True)
apkg_path = f"{out_dir}/{DECK_NAME.replace(' ', '_')}.apkg"
Package(deck, media_files=MEDIA_DIR).write_to_file(apkg_path)
print(f"Anki deck saved as {apkg_path}")