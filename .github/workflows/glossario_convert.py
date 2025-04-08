import os

# glossario_convert.py

def convert_glossario_to_html(txt_file, html_template_file, output_html_file):
    try:
        # Leggi il contenuto del file di testo
        with open(txt_file, 'r', encoding='utf-8') as txt:
            glossario_content = txt.read()

        # Leggi il template HTML
        with open(html_template_file, 'r', encoding='utf-8') as html_template:
            html_content = html_template.read()

        # Sostituisci il segnaposto {{contenuto}} con il contenuto del glossario
        html_content = html_content.replace('{{glossario}}', convert_txt_to_html(glossario_content))

        # Scrivi il risultato in un nuovo file HTML
        with open(output_html_file, 'w', encoding='utf-8') as output_html:
            output_html.write(html_content)

        print(f"File HTML generato con successo: {output_html_file}")

    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")


def convert_txt_to_html(txt_content):
    # Crea un dizionario per organizzare le definizioni per lettera
    glossario = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        glossario[letter] = []

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
        if not line or line.startswith("Pagina") or line.startswith("Indice") or line.startswith("Registro"):
            continue

        # Identifica le definizioni (formato "• Term: Definizione")
        if line.startswith("•"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                term = parts[0].replace("•", "").strip()
                definition = parts[1].strip()
                letter = term[0].upper()
                if letter in glossario:
                    glossario[letter].append(f"<b class='parola'>{term}:</b> <p class='definizione'> {definition} </p>")
        elif not line or not line.startswith("Code Alchemists") and not len(line) < 2:
            # Aggiunge righe successive come parte della descrizione
            if glossario and any(glossario[letter] for letter in glossario):
                last_letter = term[0].upper()
                if last_letter in glossario and glossario[last_letter]:
                    glossario[last_letter][-1] = glossario[last_letter][-1].rstrip('</p>') + f" {line}</p>"

    # Genera l'HTML
    html_output = ""
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        html_output += f'<div id="letter-{letter}" class="letter-section">\n'
        html_output += f'    <h2>{letter}</h2>\n'
        if glossario[letter]:
            for definition in glossario[letter]:
                html_output += f'    <div>\n'
                html_output += f'        {definition}\n'
                html_output += f'    </div>\n'
        else:
            html_output += f'    <div>\n'
            html_output += f'        <b class="parola">Nessuna definizione disponibile.</b>\n'
            html_output += f'    </div>\n'
        html_output += f'    <hr>\n'
        html_output += f'</div>\n'

    return html_output

# Specifica i file di input e output
txt_file = 'glossario.txt'
html_template_file = 'Assets/templates/template_glossario.html'
output_html_file = 'glossario.html'

# Esegui la conversione
convert_glossario_to_html(txt_file, html_template_file, output_html_file)