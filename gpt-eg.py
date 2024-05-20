from openai import OpenAI
import csv  
import sys

# File path of your CSV file containing the questions
csv_file_path = 'GDPR_questions.csv'
# File path of your TXT file containing the privacy policy
txt_file_path = 'Text.txt'

# File path to write the CSV file containing questions and answers
output_csv_file_path = 'questions_with_answers.csv'

# List to store the questions
questions = []
#string to store the text information of the policy
privacy_policy_text = ''
# List to store the questions and their corresponding answers
question_answer_pairs = []

client = OpenAI()

def read_policy(txt_file_path):
    # Reading the content of the TXT file with UTF-8 encoding
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        privacy_policy_text = file.read()
    return privacy_policy_text

def read_questions():
  # Reading questions from the CSV file
  with open(csv_file_path, 'r') as file:
      reader = csv.reader(file)
      for row in reader:
          questions.append(row[0])


def ask_gpt():
  # Get answers for each question
  for question in questions:
    answer = get_response(question, privacy_policy_text)
    question_answer_pairs.append((question, answer))


def get_response(question, policy_text):
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.0001,
    messages=[
              {
                "role": "system",
                "content": "You are a privacy law expert specializing in GDPR compliance. You will be provided with a privacy policy and a question enclosed in XML tags. Based on the provided policy, determine the compliance with GDPR and respond with one of the following: 'compliant', 'not compliant'. Only respond with 'out of my scope to determine' if the policy does not provide enough information to make a determination. Be concise and ensure your response is based solely on the content of the policy."
              },
              {
                "role": "user",
                "content": f"Here is the privacy policy of a company: \n<privacy_policy>{policy_text}</privacy_policy> \n\nHere is the question: <question>{question}</question>"
              }
            ]
    )    
    return response.choices[0].message.content

def write_to_file():
  # Writing questions and answers to the CSV file
  with open(output_csv_file_path, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['Question', 'Answer'])  # Writing header
      writer.writerows(question_answer_pairs)

  print("Questions with answers have been saved to 'questions_with_answers.csv'")

def main():
  try:
      privacy_policy_text = read_policy(txt_file_path)
      print(f'Privacy Policy length : {len(privacy_policy_text)}')
      read_questions()
      print(f'questions read, total number of questions = {len(questions)}')
      print(f'asking gpt')
      ask_gpt()
      print(f'created question answer pairs of count = {len(question_answer_pairs)}')
      write_to_file()
  except Exception as e:
      print(f'error: {e}')
  finally:
     print(f'program ended successfully')
     sys.open('questions_with_answers.csv')

if __name__ == '__main__':
   main()   