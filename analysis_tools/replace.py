file_in = "/users/nwlodychak/Downloads/Notion.md"
cleaned_file = "/users/nwlodychak/Downloads/Notion1.md"

def clean_file(filename, cleaned_filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        content = file.read()
        cleaned = content.replace("\xa0", " ")

    with open(cleaned_filename, 'w', encoding = 'utf-8') as file:
        file.write(cleaned)

clean_file(file_in, cleaned_file)