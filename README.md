# bw2kpxc: Bitwarden to KeePassXC Converter

This tool allows you to convert your Bitwarden vault data to a format that can be imported into KeePassXC.

## Prerequisites
* Python 3
* Your Bitwarden vault data exported as a JSON file

## Usage
1. Export your Bitwarden vault data to a JSON file. You can do this from the Bitwarden web vault by going to "Tools" > "Export Vault" > "File Format: .json".

1. Clone this repository to your local machine:

```bash
git clone https://github.com/iamgreggarcia/bw2kpxc.git
```

3. Move the exported Bitwarden JSON file to the root directory of the cloned repository.

4. Run the conversion script with the name of your exported vault file as an argument:

```py
python convert.py <name_of_exported_vault.json>
```

This will create a new CSV file in the same directory with the name <name_of_exported_vault>_keepassxc.csv.

5. Open KeePassXC and select "Database" > "Import" > "Import from CSV".

6. Navigate through the import options, set your master password, and on the "Import CSV Fields" screen, make sure to check the "First line has field names" option.

7. Click "OK" to complete the import process.

Now, your Bitwarden vault data should be successfully imported into KeePassXC.