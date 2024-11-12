import json
from fpdf import FPDF

# Load card data from JSON file
with open('cards.json', 'r') as file:
    data = json.load("C:\Users\alano\OneDrive\Documents\GitHub\cloud-nine\Data_cycle_cards_POC\data_cycle_cards.json")

# Create PDF document
pdf = FPDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=15)

# Card dimensions
card_width = 100
card_height = 140

# Function to add a card to the PDF
def add_card(card, x, y):
    # Front of the card
    pdf.set_xy(x, y)
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(card_width, 10, card['front'], border=1, align='C')

    # Back of the card
    pdf.set_xy(x, y + card_height + 5)
    pdf.set_font('Arial', '', 10)
    back_content = f"Example: {card['back']['example']}\nVariations: {', '.join(card['back']['variations'])}"
    pdf.multi_cell(card_width, 10, back_content, border=1, align='L')

# Add cards to the PDF
x, y = 10, 10
for card in data['cards']:
    if y + card_height * 2 + 10 > pdf.h - 10:
        pdf.add_page()
        y = 10
    add_card(card, x, y)
    y += card_height * 2 + 10

# Save the PDF to a file
pdf.output('data_cycle_cards.pdf')
