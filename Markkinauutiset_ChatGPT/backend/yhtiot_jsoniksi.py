import json

# Path to your text file
text_file_path = r'C:\Users\Kingi\Ohjelmointi\OpiKoodia\Markkinauutiset_ChatGPT_tiedot\FirstNorthYhtiot.txt'
# Output JSON file path
json_file_path = r'C:\Users\Kingi\Ohjelmointi\OpiKoodia\Markkinauutiset_ChatGPT_tiedot\FirstNorthYhtiotJson.json'

# Initialize an empty list to hold the company data
companies = []

# Open and read the text file line by line
with open(text_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Assuming each line contains company details separated by commas
        name = line.strip()
        sector = 'Nasdaq Helsinki' 
        # Create a dictionary for the current company
        company = {
            'company': name,
            'sector': sector,
        }
        # Add the company dictionary to the list
        companies.append(company)

# Write the list of companies to a JSON file
# print(companies)
[print(i) for i in companies]
        
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(companies, json_file, ensure_ascii=False, indent=4)

print(f"Converted {len(companies)} companies to JSON format in '{json_file_path}'.")
