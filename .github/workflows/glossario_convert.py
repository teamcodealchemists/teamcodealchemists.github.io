import os

# glossario_convert.py

def convert_glossario_to_html(txt_file):
    try:
        # Leggi il contenuto del file di testo
        with open(txt_file, 'r', encoding='utf-8') as txt:
            glossario_content = txt.read()

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
                term = parts[0].replace("•", "").strip()
                definition = parts[1].strip()
                letter = term[0].upper()
                if letter in glossario:
                    glossario[letter].append(f"<b class='parola'>{term}:</b> <p class='definizione'>{definition}</p>")
        elif glossario and any(glossario[letter] for letter in glossario):
            # Aggiunge righe successive come parte della descrizione
            last_letter = term[0].upper()
            if last_letter in glossario and glossario[last_letter]:
                glossario[last_letter][-1] = glossario[last_letter][-1].rstrip('</p>') + f" {line}</p>"

    # Genera l'HTML
    html_output = "<!DOCTYPE html>\n<html lang='it'>\n<head>\n"
    html_output += "    <meta charset='UTF-8'>\n"
    html_output += "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
    html_output += "    <title>Glossario</title>\n"
    html_output += "    <style>\n"
    html_output += "        .letter-section { margin-bottom: 20px; }\n"
    html_output += "        .parola { font-weight: bold; }\n"
    html_output += "        .definizione { margin-left: 10px; display: inline; }\n"
    html_output += "    </style>\n"
    html_output += "</head>\n<body>\n"
    html_output += "    <h1>Glossario</h1>\n"

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        html_output += f'<div id="letter-{letter}" class="letter-section">\n'
        html_output += f'    <h2>{letter}</h2>\n'
        if glossario[letter]:
            for definition in glossario[letter]:
                html_output += f'    <div>{definition}</div>\n'
        else:
            html_output += f'    <div><b class="parola">Nessuna definizione disponibile.</b></div>\n'
        html_output += f'    <hr>\n'
        html_output += f'</div>\n'

    html_output += "</body>\n</html>\n"

    return html_output


# Specifica il file di input
txt_file = 'glossario.txt'

# Esegui la conversione
convert_glossario_to_html(txt_file)