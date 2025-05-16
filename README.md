# DH-decode-script

A Python script for decoding downlinked `.bin` telemetry log files from Argus. The script parses subsystem-specific binary Data Handler files, originally packed using `struct.pack` in the onboard flight software and converts them into human-readable `.csv` files for analysis. Useful for batch processing logs from long-duration DITL or TVAC tests.


## Usage

```bash
python main.py -i ./logs -o ./converted_logs
```

- `-i` / `--input`: Path to the top-level input folder containing subsystem folders (e.g., logs/adcs, logs/eps, etc.)
- `-o` / `--output`: Path to the top-level output folder where .csv files will be saved, preserving the directory structure

## Features

- Supports all key subsystems:
  - `adcs`, `cdh`, `cmd_logs`, `comms`, `eps`, `eps_warning`, `gps`, and `hal`
- Recursively scans a directory containing subsystem folders with `.bin` log files
- Decodes binary files using appropriate `struct` format for each subsystem
- Outputs `.csv` files with corresponding headers in a mirrored output directory structure.

## Functionality

1. Each subsystem has a known binary format (`STRUCT_FORMATS`) and field definitions (`FIELDS`).
2. The script uses Python's `struct` module to unpack binary records from `.bin` files.
3. It creates a matching `.csv` file for each `.bin` file, with a header row and data rows.
4. Output `.csv` files are written to a new directory that mirrors the structure of the input log directory.
