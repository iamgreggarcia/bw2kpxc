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
    Process a vault item.

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
    ## If the item has additional fields, we add them to the `Notes` field. 
    ## IMPORTANT: If the additional field was of type "hidden", it will be shown in plain text inside the `Notes` field!
    ## TODO: Map to KeePassXC entry's 'Advanced' > 'Additional Attributes' field (with "protect" flag set to "true" for hidden fields)
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

def convert(bw_file):
    """
    Converts a Bitwarden export file to a KeePassXC-compatible CSV file.

    Args:
        bw_file (str): The file path of the exported bitwarden file.

    Returns:
        None
    """
    csv_path = bw_file.rsplit('.', 1)[0] + '_keepassxc.csv'

    with open(bw_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        folders = load_folders(data.get("folders", []))
        items = data.get("items", [])

        with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
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
    bw_file = sys.argv[1]
    convert(bw_file)
    print(f"Conversion complete. KeePassXC CSV file created at {bw_file.rsplit('.', 1)[0] + '_keepassxc.csv'}")