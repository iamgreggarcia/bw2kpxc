from unittest.mock import patch, mock_open
import json
import convert

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
    "folders": [{"id": "1", "name": "Folder1"}],
    "items": [{"name": "Item1", "folderId": "1", "type": 1, "login": {"username": "user1", "password": "pass1", "uris": [{"uri": "http://example.com"}]}, "notes": "Note1"}]
}))
def test_convert_bitwarden_to_keepassxc(mock_file):
    convert.convert_bitwarden_to_keepassxc("dummy_path.json")
    mock_file.assert_any_call("dummy_path.json", "r", encoding="utf-8")
    mock_file.assert_any_call("dummy_path_keepassxc.csv", "w", newline="", encoding="utf-8")
    mock_file().write.assert_called_with('Folder1,Item1,user1,pass1,http://example.com,Note1\r\n')

def test_load_folders():
    folders = convert.load_folders([{"id": "1", "name": "Folder1"}])
    assert folders == {"1": "Folder1", None: "No Folder"}

def test_process_item():
    item = {"name": "Item1", "folderId": "1", "type": 1, "login": {"username": "user1", "password": "pass1", "uris": [{"uri": "http://example.com"}]}, "notes": "Note1"}
    folders = {"1": "Folder1", None: "No Folder"}
    processed_item = convert.process_item(item, folders)
    assert processed_item == ["Folder1", "Item1", "user1", "pass1", "http://example.com", "Note1"]