import os

# glossario_convert.py

def convert_glossario_to_html(txt_file):
    try:
        # Leggi il contenuto del file di testo
        with open(txt_file, 'r', encoding='utf-8') as txt:
            glossario_content = txt.read()

        # Stampa il contenuto del file per il debug
        print("Contenuto del file glossario.txt:")
        print(glossario_content)

        # Converte il contenuto in HTML
        html_content = generate_html(glossario_content)

        # Leggi il file HTML esistente
        output_html_file = os.path.splitext(txt_file)[0] + ".html"
        with open(output_html_file, 'r', encoding='utf-8') as output_html:
            existing_html = output_html.read()

        # Sostituisci la variabile {{glossario}} con il contenuto generato
        updated_html = existing_html.replace("{{glossario}}", html_content)

        # Scrivi il risultato nel file HTML
        with open(output_html_file, 'w', encoding='utf-8') as output_html:
            output_html.write(updated_html)

        print(f"File HTML aggiornato con successo: {output_html_file}")

    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")


def generate_html(txt_content):
    # Crea un dizionario per organizzare le definizioni per lettera
    glossario = {letter: [] for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

    # Flag per identificare la sezione del glossario
    in_glossary_section = False
    current_term = None  # Per tracciare il termine corrente

    # Processa il contenuto del file di testo
    for line in txt_content.splitlines():
        line = line.strip()

        # Identifica l'inizio della sezione del glossario
        if line == "Glossario":
            in_glossary_section = True
            continue

        # Ignora le righe fuori dalla sezione del glossario
        if not in_glossary_section:
            continue

        # Ignora righe vuote o non pertinenti
        if not line or line.startswith(("Pagina", "Indice", "Registro")):
            continue

        # Identifica le definizioni (formato "• Term: Definizione")
        if line.startswith("•"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                current_term = parts[0].replace("•", "").strip()
                definition = parts[1].strip()
                letter = current_term[0].upper()
                if letter in glossario:
                    glossario[letter].append(f"<b class='parola'>{current_term}:</b> <p class='definizione'>{definition}</p>")
        elif current_term:
            # Aggiunge righe successive come parte della descrizione
            letter = current_term[0].upper()
            if letter in glossario and glossario[letter]:
                glossario[letter][-1] = glossario[letter][-1].rstrip('</p>') + f" {line}</p>"

    # Genera solo il contenuto del glossario
    html_output = ""

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        html_output += f'<h2>{letter}</h2>\n'
        if glossario[letter]:
            for definition in glossario[letter]:
                html_output += f'    <div>\n        {definition}\n    </div>\n'
        else:
            html_output += f'    <div><b class="parola">Nessuna definizione disponibile.</b></div>\n'
        html_output += f'    <hr>\n'

    return html_output


# Specifica il file di input
txt_file = 'glossario.txt'

# Esegui la conversione
convert_glossario_to_html(txt_file)