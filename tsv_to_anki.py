import csv
from genanki import Deck, Note, Package, Model

# Define the Anki model
model_id = 1607392319
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

# Create an Anki deck
deck_id = 2059400110
deck = Deck(
    deck_id,
    'NP-Complete Problems',
)

# Read the TSV file and add notes to the deck
tsv_file = "flashcards.tsv"  # Update with your TSV file path
with open(tsv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        if len(row) >= 2:  # Ensure the row has at least Front and Back content
            front, back = row[0], row[1]
            note = Note(
                model=model,
                fields=[front, back]
            )
            deck.add_note(note)

# Save the deck to an Anki package file
output_path = "flashcards.apkg"  # Output .apkg file
Package(deck).write_to_file(output_path)
print(f"Anki deck saved as {output_path}")
