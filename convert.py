import json
import csv
import sys

def load_folders(folder_data):
    """
    Load folders from folder_data and return a dictionary mapping folder IDs to folder names.
    
    Args:
        folder_data (list): A list of dictionaries containing folder information.
        
    Returns:
        dict: A dictionary mapping folder IDs to folder names.
    """
    folders = {folder["id"]: folder["name"] for folder in folder_data}
    folders[None] = "No Folder"
    return folders

def process_item(item, folders):
    """
    Process an item and extract relevant information.

    Args:
        item (dict): The item to process.
        folders (dict): A dictionary mapping folder IDs to folder names.

    Returns:
        list: A list containing the extracted information in the following order:
            - group: The name of the group the item belongs to.
            - title: The title of the item.
            - username: The username associated with the item (empty string if not applicable).
            - password: The password associated with the item (empty string if not applicable).
            - url: The URL associated with the item (empty string if not applicable).
            - notes: Additional notes associated with the item.
    """
    group = folders.get(item.get("folderId"), "Imported")
    title = item.get("name", "")
    username = (
        item.get("login", {}).get("username", "") if item.get("type") == 1 else ""
    )
    password = (
        item.get("login", {}).get("password", "") if item.get("type") == 1 else ""
    )
    url = (
        item.get("login", {}).get("uris", [{}])[0].get("uri", "")
        if item.get("type") == 1 and item.get("login", {}).get("uris")
        else ""
    )
    notes = item.get("notes", "") or ""
    if item.get("fields"):
        for field in item["fields"]:
            notes += f"\n{field['name']}: {field.get('value', '')}"
    if item.get("type") == 2:
        notes += "\nSecure Note"
    if item.get("type") == 3:
        card = item.get("card", {})
        notes += f"\nCard Number: {card.get('number', '')}\nExpiry: {card.get('expMonth', '')}/{card.get('expYear', '')}"

    return [group, title, username, password, url, notes]

def convert_bitwarden_to_keepassxc(bitwarden_export_path):
    """
    Converts a Bitwarden export file to a KeePassXC-compatible CSV file.

    Args:
        bitwarden_export_path (str): The file path of the Bitwarden export file.

    Returns:
        None
    """
    keepassxc_csv_path = bitwarden_export_path.rsplit('.', 1)[0] + '_keepassxc.csv'

    with open(bitwarden_export_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        folders = load_folders(data.get("folders", []))
        items = data.get("items", [])

        with open(keepassxc_csv_path, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                ["Group", "Title", "Username", "Password", "URL", "Notes"]
            )
            for item in items:
                csv_writer.writerow(process_item(item, folders))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json2csv.py bitwarden_exported_json_file.json")
        sys.exit(1)
    bitwarden_export_path = sys.argv[1]
    convert_bitwarden_to_keepassxc(bitwarden_export_path)
    print(f"Conversion complete. KeePassXC CSV file created at {bitwarden_export_path.rsplit('.', 1)[0] + '_keepassxc.csv'}")