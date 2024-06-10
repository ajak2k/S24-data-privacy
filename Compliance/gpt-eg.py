from openai import OpenAI
import csv  
from tokenizer import tokenize_text

# File path of your CSV file containing the questions
csv_file_path = 'GDPR_questions.csv'
# File path of your TXT file containing the privacy policy
txt_file_path = 'Text.txt'

# File path to write the CSV file containing questions and answers
output_csv_file_path = 'questionsV2_with_answersV3.csv'

gpt_model = 'gpt-4o' # what model to use, 'gpt-3.5-turbo'(faster and cheaper but less number of input tokens) or 'gpt-4o'(more number of input tokens, slower and expensive)

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
        #privacy_policy_text = tokenize_text(privacy_policy_text)
    return privacy_policy_text

def read_questions():
  # Reading questions from the CSV file
  with open(csv_file_path, 'r') as file:
      reader = csv.reader(file)
      for row in reader:
          questions.append(row[0])


def ask_gpt(policy_text, model):
  # Get answers for each question
  for question in questions:
    answer = get_response(question, policy_text, model)
    question_answer_pairs.append((question, answer))


def get_response(batch_question, policy_text, model):
    
    system_prompt = """
                    You are a privacy law expert specializing in GDPR compliance.
                    You will be given a privacy policy and a question enclosed in XML tags.
                    Based on the policy, determine GDPR compliance and respond with 1 for 'compliant', 0 for 'not compliant'.
                    Be concise and base your response solely on the policy content.
                    """

    user_prompt = f"""
                    <privacy_policy>{policy_text}</privacy_policy>
                    <question>{batch_question}</question>
                  """                

    response = client.chat.completions.create(
    model= model,
    temperature=0.1, #it is a measure of randomness that the model uses when generating text. A lower temperature value will result in more deterministic responses.
    top_p = 0.001, #it is a measure of the model's diversity. A lower value will result in the model sampling from a smaller set of likely tokens.
    messages=[
              {
                "role": "system",
                "content": f"{system_prompt}"
              },
              {
                "role": "user",
                "content": f"{user_prompt}"
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

  print(f"Questions with answers have been saved to '{output_csv_file_path}'")

def main():
  try:
      privacy_policy_text = read_policy(txt_file_path)
      print(f'Privacy Policy length : {len(privacy_policy_text)}')
      #print(f'{privacy_policy_text}')
      read_questions()
      print(f'questions read, total number of questions = {len(questions)}')
      print(f'asking gpt')
      ask_gpt(privacy_policy_text, gpt_model)
      print(f'created question answer pairs of count = {len(question_answer_pairs)}')
      write_to_file()
  except Exception as e:
      print(f'error: {e}')
  finally:
     print(f'program ended successfully')

if __name__ == '__main__':
   main()   