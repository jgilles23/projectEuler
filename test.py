from bs4 import BeautifulSoup

# Read HTML content from the file
with open("testtext.txt", "r", encoding="utf-8") as file:
    html_input = file.read()

# Parse the HTML
soup = BeautifulSoup(html_input, "html.parser")

# Find all <li> elements
list_items = soup.find_all("li")

# Extract and print the main visible name from each list item
for li in list_items:
    # Find the first <div> inside the <li>
    main_div = li.find("div")
    if main_div and main_div.text:
        # Get the direct text of the outer div, excluding nested divs
        name = main_div.get_text(separator="|").split("|")[0].strip()
        print(name)
