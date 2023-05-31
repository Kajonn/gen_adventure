from gen_adventure import prompt_manager

prompt_manager = prompt_manager.PromptManager()
user_prompt = ""

while user_prompt != "end":    
    prompt_result = prompt_manager.handle_prompt(user_prompt)
    print(prompt_result)
    user_prompt = input()
    