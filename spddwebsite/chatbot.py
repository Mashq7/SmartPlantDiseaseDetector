import openai

openai.api_key = "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"

class_name="Tomato__Target_Spot"

# def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": str(prompt)}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=1,  # this is the degree of randomness of the model's output
#     )
#     print( response.choices[0].message["content"])



def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    print(response.choices[0].message["content"])



def collect_messages():
    print("Welcome to the Plant Pathologist Chatbot!")
    print("You can ask questions about plant diseases, including Tomato Target Spot.")
    
    context = [{'role': 'system', 'content': f"""
        act as a Plant Pathologist and tell me more about {class_name}
        ***********************************************
        output: the output should take into consideration the following
        - make the output 100 words at most
        - use easy words to understand
    """}]
    
    response = get_completion_from_messages(context)
    print("Chatbot:", response)  # Display initial response
    
    while True:
        prompt = input("You: ")
        
        if prompt.lower() in ["quit", "exit", "stop"]:
            print("Chatbot: Conversation ended. Goodbye!")
            break
        
        context.append({'role': 'user', 'content': prompt})
        response = get_completion_from_messages(context)
        print("Chatbot:", response)
        
    print("Chatbot session ended.")

# Call the function to start the chatbot
collect_messages()



# context = [ {'role':'system', 'content':f"""

#             act as a Plant Pathologist and tell me more about {class_name}
#               ***********************************************
#             output: the output should take in consideration the following
#             - make the output 100 word at most
#             - use easy words to understand


# """} ]  # accumulate messages


# def collect_messages():
#     response = get_completion_from_messages(context)
#     #crate a loop to keep the chatbot running
#     while True:
#         #enter the user input
#         prompt = input("Enter your input: ")
#         #inp.value = ''
#         context.append({'role':'user', 'content':f"{prompt}"})
#         response = get_completion_from_messages(context)
#         context.append({'role':'assistant', 'content':f"{response}"})
#         flag=input("Do you want to continue? (y/n)")
#         if flag=='n':
#             break
#         else:
#             collect_messages()
#     return response

        
        