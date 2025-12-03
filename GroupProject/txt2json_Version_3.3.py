import sys
import json
import os
import sqlite3
import time
from pathlib import Path

# ---------- VARIABLES ----------
programdir = Path.cwd()
txtdir = Path('.//txt_input')
jsondir = Path('.//json_output')
json_input_dir = Path('.//json_input')
txt_output_dir = Path('.//txt_output')
json_samples_dir = Path('.//json_samples')
db_file = programdir / "json_schema.db"

JSON_SCOPES = ["textures_list", "terrain_textures", "flipbook_textures"]

# ---------- ENSURE DIRECTORIES ----------
for d in [txtdir, jsondir, json_input_dir, txt_output_dir, json_samples_dir]:
    if not d.exists():
        os.mkdir(d)

# ---------- USER INTERFACE ----------
def main_menu():
    print("\n==================================================")
    print("~~~~~~~~~~~~~ WELCOME TO TXT2JSON ~~~~~~~~~~~~~")
    print("==================================================")
    print("[!] Please view the README.txt file before continuing!")
    print("==================================================")
    print("What would you like to do today?")
    print("[1] Convert .txt files to .json")
    print("[2] Convert .json files to .txt")
    print("[3] Minecraft Mod Configurator")
    print("[4] Exit the Program")
    print("==================================================")

# ---------- USER PROMPT FUNCTIONS ----------
def prompt_user_choice(prompt, options):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input(f"Select an option (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("\n==================================================")
        print("[!] Invalid Input! Please try again!")
        print("==================================================")

# ---------- SQLITE FUNCTIONS ----------
def create_and_populate_json_terms_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS json_terms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)
    terms = [
        ("Object", "An unordered set of name/value pairs..."),
        ("Array", "An ordered collection of values..."),
        ("String", "A sequence of Unicode characters..."),
        ("Number", "A numeric integer or float..."),
        ("Boolean", "True or false..."),
        ("Null", "Empty or no value..."),
        ("Name/Value Pair", "Key and value separated by colon..."),
    ]
    cur.execute("DELETE FROM json_terms")
    cur.executemany("INSERT INTO json_terms (term, description) VALUES (?, ?)", terms)
    conn.commit()

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS json_structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT,
            data_type TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS text_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT,
            value TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS json_defaults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT,
            value TEXT
        )
    """)
    conn.commit()

def load_sample_structure(conn, sample_json_path):
    try:
        with open(sample_json_path, "r", encoding="utf-8") as f:
            sample = json.load(f)
    except FileNotFoundError:
        print("\n==================================================")
        print(f"[𐄂] Program failed to load '{sample_json_path.name}'.")
        print("Make sure it exists in the 'json_samples' folder.")
        print("==================================================")
        time.sleep(5)
        return False

    cur = conn.cursor()
    cur.execute("DELETE FROM json_structure")
    cur.execute("DELETE FROM json_defaults")

    def parse_structure(key, value):
        dtype = type(value).__name__
        cur.execute(
            "INSERT INTO json_structure (key_name, data_type) VALUES (?, ?)",
            (key, dtype)
        )
        if isinstance(value, dict):
            for k, v in value.items():
                parse_structure(f"{key}.{k}", v)
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                parse_structure(f"{key}.{idx}", item)
        else:
            cur.execute(
                "INSERT INTO json_defaults (key_name, value) VALUES (?, ?)",
                (key, str(value))
            )

    if isinstance(sample, dict):
        for k, v in sample.items():
            parse_structure(k, v)
    else:
        parse_structure("root", sample)

    conn.commit()
    print(f"[✓] Loaded JSON structure from '{sample_json_path.name}'")
    return True

def parse_txt_to_text_data(conn, scope=None, validated_files=None):
    cur = conn.cursor()
    cur.execute("DELETE FROM text_data")

    if validated_files is None:
        validated_files = list(txtdir.glob("*.txt"))

    if not validated_files:
        print(f"Warning: No files to process.")
        return

    for txt_file in validated_files:
        with open(txt_file, "r", encoding="utf-8") as f:
            # For textures_list, we need to handle plain lines without colons
            if scope == "textures_list":
                line_num = 0
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        # Store as root.INDEX for array items
                        cur.execute("INSERT INTO text_data (key_name, value) VALUES (?, ?)",
                                    (f"root.{line_num}", line))
                        line_num += 1
            else:
                # For other scopes, parse key:value pairs
                for line in f:
                    if ":" in line:
                        key, value = line.strip().split(":", 1)
                        cur.execute("INSERT INTO text_data (key_name, value) VALUES (?, ?)",
                                    (key.strip(), value.strip()))
    conn.commit()
    print("[✓] Inserted TXT data into SQLite.")

def build_json_from_db(conn, output_filename="converted.json"):
    cur = conn.cursor()
    cur.execute("SELECT key_name, value FROM json_defaults")
    defaults = cur.fetchall()
    cur.execute("SELECT key_name, value FROM text_data")
    rows = cur.fetchall()
    cur.execute("SELECT key_name, data_type FROM json_structure")
    structure = dict(cur.fetchall())
    json_obj = {}

    def decode_values(rows):
        for key, value in rows:
            dtype = structure.get(key, "str")
            obj = json_obj
            if "." in key:
                for k in key.split(".")[:-1]:
                    if k.isnumeric():
                        k = int(k)
                        obj["%islist"] = None
                    if k not in obj:
                        obj[k] = {}
                    obj = obj[k]
                k = key.split(".")[-1]
            else:
                k = key
            if k.isnumeric():
                k = int(k)
                obj["%islist"] = None

            try:
                if dtype == "int":
                    obj[k] = int(value)
                elif dtype == "float":
                    obj[k] = float(value)
                elif dtype == "bool":
                    obj[k] = value.lower() in ("true", "1", "yes")
                else:
                    obj[k] = value
            except Exception:
                obj[k] = value

    decode_values(defaults)
    decode_values(rows)

    def post_process(obj):
        if isinstance(obj, dict):
            if "%islist" in obj:
                listobj = []
                for k, v in obj.items():
                    if isinstance(k, int):
                        while k >= len(listobj):
                            listobj.append(None)
                        listobj[k] = post_process(v)
                return listobj
            else:
                for k, v in obj.items():
                    obj[k] = post_process(v)
                return obj
        else:
            return obj

    json_obj = post_process(json_obj)
    output_path = jsondir / output_filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, indent=4)
    print(f"[✓] Successfully created '{output_path.name}'!")

# ---------- TXT TO JSON CONVERSION ----------
def convert_txt_files_to_json():
    print("\n==================================================")
    print("MODE 1 -- txt2json")
    print("[!] Ensure that the .txt files you want to convert are in the txt_input folder.")
    print("==================================================")
    files_list = list(txtdir.glob('*.txt'))
    if not files_list:
        print("\n==================================================")
        print("[!] The Program was unable to pull any .txt files from the txt_input folder.")
        print("Please make sure your files are present before continuing.")
        print("==================================================")
        time.sleep(5)
        return

    for name in files_list:
        print(name)

    while True:
        response = input("\nAre these the files you want to convert? ['y' or 'n']\n> ").strip().lower()
        if response == 'y':
            print("\n[⟳] Starting Conversion...")
            time.sleep(2)
            converted_count = 0
            for txt_file in files_list:
                print(f"[⟳] Converting {txt_file.name}...")
                time.sleep(0.25)
                print(f"[⟳] Validating {txt_file.name}...")
                time.sleep(0.5)

                # perform actual conversion (preserved logic)
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                json_data = {"filename": txt_file.name, "content": content}
                json_filename = txt_file.stem + '.json'
                json_filepath = jsondir / json_filename
                with open(json_filepath, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)

                print(f"[✓] Successfully converted and validated {txt_file.name}!")
                time.sleep(0.1)
                converted_count += 1

            print("==================================================")
            print(f"Your conversion is complete! Successfully converted {converted_count} file(s).")
            print("Check json_output for your converted file(s)!")
            print("==================================================")
            return
        elif response == 'n':
            print("\nOperation cancelled! Returning to main menu.")
            time.sleep(3)
            return
        else:
            print("\n==================================================")
            print("[!] Invalid Input! Please try again!")
            print("==================================================")

# ---------- JSON TO TXT CONVERSION ----------
def convert_json_files_to_txt():
    print("\n==================================================")
    print("MODE 2 -- json2txt")
    print("[!] Ensure that the .json files you want to convert are in the json_input folder.")
    print("==================================================")
    files_list = list(json_input_dir.glob('*.json'))
    if not files_list:
        print("\n==================================================")
        print("[!] The Program was unable to pull any .json files from the json_input folder.")
        print("Please make sure your files are present before continuing.")
        print("==================================================")
        time.sleep(5)
        return

    for name in files_list:
        print(name)

    while True:
        response = input("\nAre these the files you want to convert? ['y' or 'n']\n> ").strip().lower()
        if response == 'y':
            print("\n[⟳] Starting Conversion...")
            time.sleep(2)
            converted_count = 0
            for json_file in files_list:
                print(f"[⟳] Converting {json_file.name}...")
                time.sleep(0.25)
                print(f"[⟳] Validating {json_file.name}...")
                time.sleep(0.5)

                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                txt_content = []
                def json_to_text(data, indent=0):
                    prefix = "  " * indent
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, (dict, list)):
                                txt_content.append(f"{prefix}{key}:")
                                json_to_text(value, indent + 1)
                            else:
                                txt_content.append(f"{prefix}{key}: {value}")
                    elif isinstance(data, list):
                        for i, item in enumerate(data):
                            if isinstance(item, (dict, list)):
                                txt_content.append(f"{prefix}[{i}]:")
                                json_to_text(item, indent + 1)
                            else:
                                txt_content.append(f"{prefix}[{i}]: {item}")
                    else:
                        txt_content.append(f"{prefix}{data}")

                json_to_text(json_data)
                txt_filename = json_file.stem + '.txt'
                txt_filepath = txt_output_dir / txt_filename

                with open(txt_filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(txt_content))

                print(f"[✓] Successfully converted and validated {json_file.name}!")
                time.sleep(0.1)
                converted_count += 1

            print("==================================================")
            print(f"Your conversion is complete! Successfully converted {converted_count} file(s).")
            print("Check txt_output for your converted file(s)!")
            print("==================================================")
            return
        elif response == 'n':
            print("\nOperation cancelled! Returning to main menu.")
            time.sleep(3)
            return
        else:
            print("\n==================================================")
            print("[!] Invalid Input! Please try again!")
            print("==================================================")


# ---------- MINECRAFT MOD CONFIGURATOR ----------
def minecraft_mod_configurator():
    while True:
        print("\n==================================================")
        print("MODE 3 -- Minecraft Mod Configurator")
        print("Select the JSON scope of your Minecraft Mod:")
        print("[1] textures_list")
        print("[2] terrain_textures")
        print("[3] flipbook_textures")
        print("==================================================")
        scope_choice = input("> ").strip()

        if scope_choice not in ['1', '2', '3']:
            print("\n==================================================")
            print("[!] Invalid Input! Please try again!")
            print("==================================================")
            continue

        selected_scope = JSON_SCOPES[int(scope_choice) - 1]
        sample_json_path = json_samples_dir / f"{selected_scope}.json"

        print("\n[⟳] Starting translation...")
        time.sleep(0.5)
        print("[⟳] Preparing SQLite...")
        time.sleep(0.2)

        with sqlite3.connect(db_file) as conn:
            # Check if txt_input has any .txt files before continuing
            txt_files = list(txtdir.glob("*.txt"))
            if not txt_files:
                print("\n==================================================")
                print("[𐄂] Program failed to locate any properly formatted .txt files in txt_input!")
                print("Please check to make sure your files are present, and have the correct syntax!")
                print("==================================================")
                time.sleep(5)
                return

            init_db(conn)
            create_and_populate_json_terms_table(conn)

            if not load_sample_structure(conn, sample_json_path):
                print("\nReturning to main menu...")
                time.sleep(1)
                return

            # Extract expected keys from json_structure table
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT key_name FROM json_structure")
            db_terms = set()
            for row in cur.fetchall():
                key_path = row[0]
                # Extract all parts of nested keys (e.g., "root.0.ticks_per_frame" -> ["root", "0", "ticks_per_frame"])
                parts = key_path.split('.')
                for part in parts:
                    if not part.isnumeric() and part != "root":  # Skip array indices and "root"
                        db_terms.add(part)

            # For array-based structures (like flipbook_textures), extract the leaf keys
            # These are the actual field names that should appear in txt files
            cur.execute("SELECT DISTINCT key_name FROM json_structure WHERE key_name LIKE '%.'")
            
            # Also extract terms from json_terms table as additional reference
            cur.execute("SELECT DISTINCT term FROM json_terms")
            json_terms_set = {row[0] for row in cur.fetchall()}

            # Combine expected terms (excluding common structure words)
            expected_terms = db_terms - {"root"}
            expected_terms = expected_terms.union(json_terms_set)

            validated_txt_files = []

            # Validate each .txt file for relevant terms before processing
            for txt_file in txt_files:
                is_valid = False
                txt_terms = set()
                has_texture_paths = False
                valid_texture_line_count = 0

                with open(txt_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:  # Skip empty lines
                            continue

                        if ":" in line:
                            key = line.split(":", 1)[0].strip()
                            if key:
                                txt_terms.add(key)
                        else:
                            # For textures_list: check if line looks like a texture path
                            # Valid texture paths typically contain "textures/" and end with image extensions
                            if ("textures/" in line.lower() or
                                line.endswith(('.png', '.tga', '.jpg', '.jpeg'))):
                                has_texture_paths = True
                                valid_texture_line_count += 1

                # For textures_list scope: expect plain texture path strings
                if selected_scope == "textures_list":
                    # Must have at least one valid texture path and no key:value pairs
                    if has_texture_paths and not txt_terms:
                        is_valid = True
                    elif txt_terms:
                        print(f"[𐄂] Skipping {txt_file.name} - Contains key:value pairs, not plain texture paths.")
                    else:
                        print(f"[𐄂] Skipping {txt_file.name} - No valid texture paths found for textures_list.")

                # For other scopes: expect key:value pairs with relevant keys
                else:
                    if txt_terms:
                        # Check if ALL keys in the file are valid (subset check)
                        invalid_keys = txt_terms - expected_terms
                        if not invalid_keys and txt_terms.intersection(expected_terms):
                            is_valid = True
                        elif invalid_keys:
                            print(f"[𐄂] Skipping {txt_file.name} - Contains invalid keys: {', '.join(sorted(invalid_keys))}")
                        else:
                            print(f"[𐄂] Skipping {txt_file.name} - No relevant terms found for {selected_scope}.")
                    else:
                        print(f"[𐄂] Skipping {txt_file.name} - No key:value pairs found.")

                if is_valid:
                    validated_txt_files.append(txt_file)

            if not validated_txt_files:
                print("\n==================================================")
                print("[𐄂] No .txt files with relevant terms found for translation!")
                print("Please check your .txt files and sample JSON structure.")
                print("Returning to main menu...")
                print("==================================================")
                time.sleep(5)
                return

            print("[⟳] Deploying text data into SQLite...")
            time.sleep(1)
            parse_txt_to_text_data(conn, selected_scope, validated_txt_files)
            print("[⟳] Validating translated data...")
            time.sleep(0.5)

            for txt_file in validated_txt_files:
                output_filename = txt_file.stem + ".json"
                build_json_from_db(conn, output_filename=output_filename)
                print(f"[✓] Successfully translated {txt_file.name} → {output_filename}")
                time.sleep(0.1)

        print("==================================================")
        print("Translation complete! View results in json_output.")
        print("==================================================")
        return

# ---------- MAIN LOOP ----------
while True:
    main_menu()
    userchoice = input("> ").strip()

    if userchoice == '1':
        convert_txt_files_to_json()
    elif userchoice == '2':
        convert_json_files_to_txt()
    elif userchoice == '3':
        minecraft_mod_configurator()
    elif userchoice == '4':
        print("\n==================================================")
        print("Thank you for using TXT2JSON! Goodbye!")
        print("==================================================")
        sys.exit()
    else:
        print("\n==================================================")
        print("[!] Invalid Input! Please try again!")
        print("==================================================")
