from bs4 import BeautifulSoup

def extract_main_text(html_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the main body of text
    main_text = soup.find('body').text

    return main_text


def main():
    # Provide the path to your HTML file
    html_file = 'D:/UC Irvine/01 - Academics/3_Spring 24/EECS232 Data Privacy/Project/data_privacy_readability_ws/policies/WA/Privacy Policy - Revisions - August 25, 2016.html'

    # Extract the main body of text
    main_text = extract_main_text(html_file)

    # Provide the path for the output text file
    output_file = 'D:/UC Irvine/01 - Academics/3_Spring 24/EECS232 Data Privacy/Project/data_privacy_readability_ws/output.txt'

     # Write the text to a text file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(main_text)

    # Print the extracted text
    print(main_text)


if __name__ == '__main__':
    main()