# PandaSearch

PandaSearch is a command-line tool written in Python that searches through multiple public Google Sheets for a specific text input by the user. It fetches the live web versions of the sheets, and for each match, it outputs the cell value where the text was found and the link to the sheet.

## Features

- Search multiple Google Sheets simultaneously using asynchronous requests for efficiency.
- Improved search functionality: case-insensitive search, and handles plurals (e.g., searching for "dunk" will also match "dunks").
- Nicely formatted console output using the `rich` library.
- Reads the list of websites from a file, making it easy to manage the sheets you want to search.
- Included example website list with **45+ spreadsheets**

## Requirements

- Python 3.7+
- Terminal that supports hyperlinks (GNOME terminal, iTerm2, xterm, and many more)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/sheetsearch.git
cd sheetsearch
```

2. Install the required libraries:

```bash
pip3 install -r requirements.txt
```

## Usage

1. Add or remove the URLs of the Google Sheets you want to search in the `websites.txt` file, one URL per line.

2. Run the script:

```bash
python3 sheetsearch.py
```

3. Enter your search term at the prompt.

The script will search all the sheets and display the results in the console. For each match, it will output the cell value where the text was found, and the link to the sheet.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

Remember to replace `https://github.com/yourusername/sheetsearch.git` with your actual repository URL.
