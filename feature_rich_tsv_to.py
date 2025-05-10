import csv, html, os
from genanki import Model, Note, Deck, Package

# ------------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------------
TSV_NAME   = "greek_slang_deck"        # file inside ./input/  (without .tsv)
DECK_NAME  = "greek_slang_deck"
MODEL_ID   = 1607392319                  # keep constant; change only if you rebuild note type
MEDIA_DIR  = []                          # list of media files if you later add audio

# ------------------------------------------------------------------
# 2. NOTE (CARD) MODEL – 4 FIELDS
# ------------------------------------------------------------------
model = Model(
    MODEL_ID,
    'Greek Root Model',
    fields=[
        {'name': 'Front'},       # 0 – Greek word
        {'name': 'Back'},        # 1 – English meaning
        {'name': 'Example_GR'},  # 2 – Greek example
        {'name': 'Example_EN'},  # 3 – English example
    ],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Front}}<hr><div style="font-size:80%; color:#555;">{{Example_GR}}</div>',
        'afmt': '{{FrontSide}}<hr id="answer">{{Back}}'
                '<div style="font-size:80%; color:#555; margin-top:6px;">{{Example_EN}}</div>',
    }],
)

# ------------------------------------------------------------------
# 3. UNIQUE DECK ID
# ------------------------------------------------------------------
def generate_deck_id(name: str) -> int:
    base = 2_147_483_647          # largest 32‑bit signed int
    return abs(hash(name)) % base

deck = Deck(generate_deck_id(DECK_NAME), DECK_NAME)

# ------------------------------------------------------------------
# 4. READ TSV AND CREATE NOTES
# ------------------------------------------------------------------
tsv_path = f"./input/{TSV_NAME}.tsv"
with open(tsv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        # Required columns in the TSV: Greek, Translit, English, Example_GR, Example_EN, Tags
        front       = html.escape(row['Greek'])
        back        = html.escape(row['English'])
        example_gr  = html.escape(row.get('Example_GR', ''))
        example_en  = html.escape(row.get('Example_EN', ''))

        note = Note(
            model=model,
            fields=[front, back, example_gr, example_en]
        )

        # Attach root‑family tag(s) if present, e.g. "root:γραφ"
        raw_tags = row.get('Tags', '')
        if raw_tags:
            note.tags = [t.strip() for t in raw_tags.split()]
        deck.add_note(note)

# ------------------------------------------------------------------
# 5. WRITE THE .APKG PACKAGE
# ------------------------------------------------------------------
out_dir = "./output"; os.makedirs(out_dir, exist_ok=True)
apkg_path = f"{out_dir}/{TSV_NAME}.apkg"
Package(deck, media_files=MEDIA_DIR).write_to_file(apkg_path)
print(f"Anki deck saved as {apkg_path}")
