import csv
from genanki import Deck, Note, Package, Model

NAME = "flashcards"
MODEL = 1607392319




model_id = MODEL 
model = Model(
    model_id,
    'NP-Complete Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
)

#Anki deck
def generate_deck_id(name: str) -> int:
    base = 2147483647
    return abs(hash(name)) % base

deck_id = generate_deck_id(NAME)
deck = Deck(
    deck_id,
    NAME,
)

# Read the TSV file and add notes to the deck
tsv_file = "flashcards.tsv"  
with open(tsv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        if len(row) >= 2:  # check for front and back
            front, back = row[0], row[1]
            note = Note(
                model=model,
                fields=[front, back]
            )
            deck.add_note(note)

output_path = f"{NAME}.apkg"  # Output .apkg file
Package(deck).write_to_file(output_path)
print(f"Anki deck saved as {output_path}")
