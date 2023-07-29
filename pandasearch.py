import re
import asyncio
import aiohttp
import os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

# Create a custom theme that sets the 'default' style for all elements.
custom_theme = Theme({
    "repr.number": "default",
    "repr.str": "default",
    "log.time": "default",
    "log.level": "default",
    "log.message": "default"
})

# Pass the custom theme to the Console constructor.
console = Console(theme=custom_theme)

def is_link(text):
    # Regular expression to check if the text is a URL or link.
    pattern = r'https?://\S+'
    return bool(re.match(pattern, text))

def is_price(text):
    # Regular expression to check if the text contains currency symbols.
    pattern = r'[\$¥€£]'
    return bool(re.search(pattern, text))

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def search_website(session, url, target_text):
    try:
        response = await fetch(session, url)
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table')
        title = soup.title.text if soup.title else url

        search_results = []

        if table:
            from pandas import read_html
            df = read_html(str(table), flavor='bs4')[0]
            for _, row in df.iterrows():
                for col in df.columns:
                    cell_text = str(row[col])
                    if re.search(r'\b{}\b'.format(target_text), cell_text, re.IGNORECASE) and not is_link(cell_text) and not is_price(cell_text):
                        search_results.append((cell_text, title, url))
                        console.print(f"[bold]{cell_text}[/bold] found on [link={url}]{title}[/link].")
                        console.print("-" * os.get_terminal_size().columns)

        # Check if no items were found
        if not search_results:
            console.print(f"No items found on [link={url}]{title}[/link].")
            console.print("-" * os.get_terminal_size().columns)

        return search_results
    except Exception as e:
        console.print(f"Error while searching website: [link={url}]{title}[/link]\nError: {e}")

    return None

console = Console(theme=custom_theme)
ascii_console = Console()
async def main():
    # ASCII Art
    ascii_art = """
      ___              _      ___                  _    
     | _ \\__ _ _ _  __| |__ _/ __| ___ __ _ _ _ __| |_  
     |  _/ _` | ' \\/ _` / _` \\__ \\/ -_) _` | '_/ _| ' \\ 
     |_| \\__,_|_||_\\__,_\\__,_|___/\\___\\__,_|_| \\__|_||_|
    """
    ascii_console.print(ascii_art, style="green")

    target_text = input("Enter search: ")

    # Read the websites from a file
    with open("websites.txt", "r") as f:
        websites = [line.strip() for line in f.readlines()]

    all_search_results = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for website in websites:
            tasks.append(search_website(session, website, target_text))
        search_results = await asyncio.gather(*tasks)

    for results in search_results:
        if results:
            all_search_results.extend(results)

    if not all_search_results:
        console.print("No matching results found.")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('Cell Value')
    table.add_column('Website Link')

    for cell_value, title, url in all_search_results:
        table.add_row(cell_value, f"[link={url}]{title}[/link]")

    console.print(table)

if __name__ == "__main__":
    asyncio.run(main())

