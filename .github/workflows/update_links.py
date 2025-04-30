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
    return name.replace("_", " ").replace(".pdf", "").title()


def generate_links(json_data, variable_name):
    """
    Genera i link HTML per i file corrispondenti a una variabile.
    - Cerca tutte le chiavi nel JSON che contengono il nome della variabile.
    - Se ci sono più file, genera una lista di link.
    - Se c'è un solo file, genera un link singolo.
    """
    links = []

    # Cerca tutte le chiavi che contengono il nome della variabile
    for key, link in json_data.items():
        if variable_name in key:
            # Estrai il nome del file dalla chiave e formatta il nome
            file_name = key.split("/")[-1]
            links.append(
                f'<li><a href="{link.replace(" ", "%20")}" target="_blank">{format_name(file_name)}</a></li>'
            )

    if not links:
        return "<p>Nessun documento disponibile</p>"

    if len(links) == 1:
        # Rimuovi i tag <li> se c'è un solo link
        return links[0][4:-5]
    return f"<ul>{''.join(links)}</ul>"


def save_output(output_path, replacements):
    """
    Sostituisce le variabili nel file di output senza modificare il resto.
    """
    try:
        if not os.path.exists(output_path):
            print(f"Errore: Il file {output_path} non esiste.")
            return

        with open(output_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()

        updated_content = existing_content
        for variable, replacement in replacements.items():
            updated_content = updated_content.replace(f"{{{{{variable}}}}}", replacement)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"File aggiornato con successo: {output_path}")

    except Exception as e:
        print(f"Errore durante l'aggiornamento del file: {e}")


def main():
    # URL del file JSON aggiornato
    json_url = "https://teamcodealchemists.github.io/docs/index.json"

    # Percorso del file di output
    output_path = "index.html"

    # Scarica il JSON aggiornato
    json_data = download_json(json_url)

    # Specifica le variabili e genera i link corrispondenti
    replacements = {
        "rtb/AdR": generate_links(json_data, "rtb/AdR"),
        "rtb/NdP": generate_links(json_data, "rtb/NdP"),
        "rtb/PdQ": generate_links(json_data, "rtb/PdQ"),
        "rtb/Gls": generate_links(json_data, "glossario/Gls"),
        "rtb/verbali/verbali_interni": generate_links(json_data, "rtb/verbali/verbali_interni"),
        "rtb/verbali/verbali_esterni": generate_links(json_data, "rtb/verbali/verbali_esterni"),
        "candidatura/verbali/verbali_interni": generate_links(json_data, "candidatura/verbali/verbali_interni"),
        "candidatura/verbali/verbali_esterni": generate_links(json_data, "candidatura/verbali/verbali_esterni"),
        "candidatura/Valutazione": generate_links(json_data, "candidatura/Valutazione"),
        "candidatura/Lettera": generate_links(json_data, "candidatura/Lettera"),
        "candidatura/Dichiarazione": generate_links(json_data, "candidatura/Dichiarazione"),
        "presentazioni": generate_links(json_data, "presentazioni"),
    }

    # Salva il file aggiornato sostituendo le variabili
    save_output(output_path, replacements)


if __name__ == "__main__":
    main()