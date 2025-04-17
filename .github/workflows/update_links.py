import json
import requests
import os
import re


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

def load_template(template_path):
    """
    Carica il contenuto del file template_index.html.
    """
    if not os.path.exists(template_path):
        print(f"Il file template {template_path} non esiste.")
        return ""
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_json_value(json_data, path):
    """
    Ottiene un valore da un dizionario JSON seguendo un percorso specifico.
    Il percorso è definito come una stringa, ad esempio: "glossario[0].link".
    """
    keys = path.split(".")
    value = json_data
    try:
        for key in keys:
            if "[" in key and "]" in key:  # Gestisce gli indici degli array
                array_key, index = key[:-1].split("[")
                value = value[array_key][int(index)]
            else:
                value = value[key]
        return value
    except (KeyError, IndexError, TypeError):
        return None

def find_node_by_name(data_list, keyword):
    """
    Cerca un elemento in una lista di dizionari in cui il campo 'name' contiene una parola chiave.
    """
    for item in data_list:
        if "name" in item and keyword in item["name"]:
            return item
    return None

def format_name(name):
    """
    Rende il nome più leggibile rimuovendo caratteri speciali, formattandolo e sostituendo sigle con descrizioni.
    """
    # Dizionario di sostituzioni per le sigle
    replacements = {
        "VI": "Verbale Interno",
        "VE": "Verbale Esterno",
        "PdP": "Piano di Progetto",
        "AdR": "Analisi dei Requisiti",
        "PdQ": "Piano di Qualifica",
        "NdP": "Norme di Progetto",
        "Gls": "Glossario",
        "signed": "Firmato"
    }
    
    # Esegui le sostituzioni per le sigle
    for sigla, descrizione in replacements.items():
        name = name.replace(sigla, descrizione)
    
    # Rimuovi underscore, sostituisci con spazi e formatta
    return name.replace("_", " ").replace(".pdf", " ").title()

def resolve_path_and_name(json_data, path_with_name):
    """
    Risolve un percorso del tipo X/Y/Z/NOME.
    Cerca il nodo X/Y/Z e poi cerca un elemento con 'name' che contiene NOME.
    """
    *path_parts, name_keyword = path_with_name.split("/")
    path = "/".join(path_parts)
    node = get_json_value(json_data, path.replace("/", "."))
    if isinstance(node, list):
        found_node = find_node_by_name(node, name_keyword)
        if found_node:
            formatted_name = format_name(found_node["name"])
            return f'<a href="{found_node["link"]}" target="_blank">{formatted_name}</a>'
    # Se non trovato, restituisci un <a> senza link
    return f'<a>{path_with_name}</a>'

def resolve_verbali(json_data, path):
    """
    Risolve i nodi per variabili che contengono la parola 'verbali'.
    Cerca tutti i nodi corrispondenti, li ordina per nome e genera i link HTML.
    """
    node = get_json_value(json_data, path)
    if isinstance(node, list):
        # Ordina i nodi per nome
        sorted_node = sorted(node, key=lambda x: x["name"], reverse=True)
        links = [
            f'<a href="{item["link"]}" target="_blank">{format_name(item["name"])}</a>\n'
            for item in sorted_node
        ]
        return "".join(links)
    # Se non trovato, restituisci un <a> senza link
    return f'<a>{path}</a>'

def replace_variables(template, variables):
    """
    Sostituisce le variabili nel template con i valori dal dizionario.
    Se una variabile non è presente, la lascia invariata.
    """
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"  # Formato delle variabili nel template: {{qualcosa}}
        template = template.replace(placeholder, str(value))
    return template

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

    # Percorsi dei file
    template_path = "Assets/templates/template_index.html"
    output_path = "index.html"

    # Scarica il JSON
    json_data = download_json(json_url)

    # Genera dinamicamente le variabili
    variables = {}

    # Carica il template
    template = load_template(template_path)

    # Sostituisci le variabili
    for placeholder in re.findall(r"\{\{(.*?)\}\}", template):
        if "verbali" in placeholder:  # Gestione speciale per variabili che contengono 'verbali'
            variables[placeholder] = resolve_verbali(json_data, placeholder)
        elif "/" in placeholder:  # Gestione speciale per percorsi del tipo X/Y/Z/NOME
            variables[placeholder] = resolve_path_and_name(json_data, placeholder)

    output_content = replace_variables(template, variables)

    # Salva il file generato
    save_output(output_path, output_content)

if __name__ == "__main__":
    main()