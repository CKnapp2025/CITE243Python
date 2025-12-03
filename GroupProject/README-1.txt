=========================================================
 Program Name : txt2json File Converter
 Version      : 3.3.2
 Description  : A dual-direction TXT ↔ JSON file converter with 
                Minecraft schema support, using SQLite validation.
 Authors      : John C. // Ryley D. // Luke S. // Cameron K.
 Last Updated : December 2nd, 2025
=========================================================

Overview:
txt2json allows you to convert TXT files to JSON and JSON files
to TXT while keeping structured formatting. It also includes a 
Minecraft Mod Configurator that uses JSON schema templates to 
generate validated configuration files (textures, flipbooks, etc).

---------------------------------------------------------
 USAGE
---------------------------------------------------------

Run the program as the txt2json.exe file.

If Windows Defender warns you about running the file, don't
worry! This is normal, and the program is safe. 

Click on "More Info", and then click "Run Anyway".

---------------------------------------------------------
 FOLDER EXPECTATIONS
---------------------------------------------------------
When the program is run for the first time, it will automatically
generate the required folders if they do not exist:

  txt_input       → Place TXT files to convert to JSON
  json_input      → Place JSON files to convert to TXT
  json_output     → Converted JSON files will appear here
  txt_output      → Converted TXT files will appear here
  json_samples    → Required Minecraft schema files
                    (Do NOT modify or remove these)
  
---------------------------------------------------------
 MAIN PROGRAM FUNCTIONS
---------------------------------------------------------
[1] TXT ➜ JSON Conversion
    • Converts every TXT file in txt_input.
    • Preserves filename (example: example.txt → example.json).
    • Original TXT files are not modified.

[2] JSON ➜ TXT Conversion
    • Converts every JSON file in json_input.
    • Preserves filename structure.
    • Outputs readable text format.

[3] Minecraft Mod Configurator
    • Select from included Minecraft JSON schemas:
        - textures_list
        - terrain_textures
        - flipbook_textures
    • Program validates formatting based on Minecraft syntax
      (key:value pairs, hierarchy, and structure).
    • Invalid files are safely skipped.

---------------------------------------------------------
 IMPORTANT NOTES
---------------------------------------------------------
• All input folders must contain valid files before running.
• Invalid Minecraft TXT files do not stop the program,
  but they will be skipped automatically.
• The json_samples folder must remain untouched—these files
  are required for correct schema loading and validation.

---------------------------------------------------------
 OUTPUT LOCATIONS
---------------------------------------------------------
• TXT ➜ JSON conversions output to: json_output
• JSON ➜ TXT conversions output to: txt_output
• Minecraft Mod Configurator outputs validated JSON files
  to: json_output

=========================================================
 Thank you for using txt2json! --- CITE-243's Team 4!
=========================================================
