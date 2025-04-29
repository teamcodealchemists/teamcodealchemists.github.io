import json
import requests
import os


def download_json(url):
    """
    Scarica un file JSON da un URL e lo restituisce come dizionario.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Errore durante il download del JSON: {e}")
        return {}


def format_name(name):
    """
    Rende il nome più leggibile rimuovendo caratteri speciali, formattandolo e sostituendo sigle con descrizioni.
    """
    replacements = {
        "VI": "Verbale Interno",
        "VE": "Verbale Esterno",
        "PdP": "Piano di Progetto",
        "AdR": "Analisi dei Requisiti",
        "PdQ": "Piano di Qualifica",
        "NdP": "Norme di Progetto",
        "Gls": "Glossario",
        "DdB": "Diario di Bordo",
        "signed": "Firmato"
    }
    for sigla, descrizione in replacements.items():
        name = name.replace(sigla, descrizione)
    return name.replace("_", " ").replace(".pdf", " ").title()


def resolve_files_or_folder(path):
    """
    Risolve un percorso che può essere una cartella o un file.
    Se è una cartella, restituisce tutti i file al suo interno.
    Se è un file, restituisce solo quel file.
    """
    if os.path.isdir(path):
        files = [
            {"name": file, "link": os.path.join(path, file)}
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
        ]
    elif os.path.isfile(path):
        files = [{"name": os.path.basename(path), "link": path}]
    else:
        files = []
    return files


def resolve_verbali(json_data, path):
    """
    Risolve i nodi per variabili che contengono la parola 'verbali'.
    Cerca tutti i nodi corrispondenti, li ordina per nome e genera i link HTML.
    """
    node = get_json_value(json_data, path)
    if isinstance(node, list):
        all_files = []
        for item in node:
            resolved_files = resolve_files_or_folder(item["path"])
            all_files.extend(resolved_files)

        sorted_files = sorted(all_files, key=lambda x: x["name"], reverse=True)
        links = [
            f'<li><a href="{file["link"]}" target="_blank">{format_name(file["name"])}</a></li>'
            for file in sorted_files
        ]
        return "".join(links)
    return f"<li>{path}</li>"


def get_json_value(json_data, path):
    """
    Ottiene un valore da un dizionario JSON seguendo un percorso specifico.
    """
    keys = path.split(".")
    value = json_data
    try:
        for key in keys:
            if "[" in key and "]" in key:
                array_key, index = key[:-1].split("[")
                value = value[array_key][int(index)]
            else:
                value = value[key]
        return value
    except (KeyError, IndexError, TypeError):
        return None


def generate_html(json_data):
    """
    Genera il contenuto HTML dinamicamente senza utilizzare un template esterno.
    """
    html = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documenti</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 5px 0; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Documenti</h1>
        <ul>
    """

    # Aggiungi i link dinamici per i verbali
    verbali_links = resolve_verbali(json_data, "verbali")
    html += verbali_links

    html += """
        </ul>
    </body>
    </html>
    """
    return html


def save_output(output_path, content):
    """
    Salva il contenuto generato in un file index.html.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"File generato: {output_path}")


def main():
    # URL del file JSON
    json_url = "https://teamcodealchemists.github.io/docs/index.json"

    # Percorso del file di output
    output_path = "index.html"

    # Scarica il JSON
    json_data = download_json(json_url)

    # Genera il contenuto HTML
    html_content = generate_html(json_data)

    # Salva il file generato
    save_output(output_path, html_content)


if __name__ == "__main__":
    main()