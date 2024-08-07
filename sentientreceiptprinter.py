import ollama
import os

while True:
    # Get the prompt from the user
    question = input("Prompt:")

    print("processing")

    # Get the response from the AI
    response = ollama.chat(model='llama3.1', messages=[
      { 'role': 'system',
        'content': "you are a sentient receipt printer, at the end of every response, asign your answer a monetary value in pounds. Keep responses at a maximum of 200 words"
        },
      {
        'role': 'user',
        'content': question,
      },
    ])

    # Extract the response content
    response_content = response['message']['content']

    print("writing to file")

    # Write the response to output.txt
    with open('output.txt', 'w') as file:
        file.write(response_content)

    print("printing")

    # Print the file to the printer
    os.system("lpr output.txt")

