import openai
from .gameworld import Place, World, environments
from .keys import api_key, organisation

openai.organisation = organisation
openai.api_key = api_key
model = "gpt-3.5-turbo"

class PromptManager:

    def __init__(self):
        self.world = World()
        print(str(self.world))
        self.current_place = self.world.root
        self.current_descr = None


    def _build_description(self, place : Place) -> str:
        prompt = "Give short realistic descriptions. The world setting is low fantasy. I am a traveller walking with green clothes and a pointy hat.\n"
        prompt +=  f"I am in a {place.environment}.\n"
        if len(place.exits) > 0:
            prompt += f"In the distance is {' and a '.join(place.get_exit_environments())}\n"
        if len(place.creatures) > 0:
            prompt += f"Here stands a {' and a '.join(place.creatures)}.\n"
        if len(place.things) > 0:
            prompt += f"On the ground lays a {' and a '.join(place.things)}.\n"
        prompt += f"The weather is {self.world.weather}.\n"
        prompt += f"The time is {self.world.time}.\n"
        return prompt

    def _prompt(self,description : str) -> str:
        result = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Describe the environment as seen for the first time"},
                {"role": "user", "content": description},
            ]
        )
        return result["choices"][0]["message"]["content"]

    def _interperet_use_prompt(self, user_prompt : str, context : str) -> str:
        result = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You interperet the user prompt"},
                {"role": "user", "content": context},
                {"role": "user", "content": "Give a summary of the next user prompt in max two words."},
                {"role": "user", "content": user_prompt},
            ]
        )
        return result["choices"][0]["message"]["content"]


    def _act_on_user_prompt(self,user_prompt, context) -> str:
        print("Act on user prompt: "+user_prompt + " with context: "+context)
        result = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You interperet the user prompt"},
                {"role": "assistant", "content": context},
                {"role": "user", "content": "Describe in a short sentence what happens after the next prompt."},
                {"role": "user", "content": user_prompt},
            ]
        )
        #return result["choices"][0]["message"]["content"]
        result2 = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You interperet the user prompt"},
                {"role": "assistant", "content": context},
                {"role": "user", "content": "Desribe in a short sentence what happens after the next prompt."},
                {"role": "user", "content": user_prompt},
                {"role":"assistant", "content": result["choices"][0]["message"]["content"]},
                {"role": "user", "content": "Did I go somewhere? If so answer only with one word: the name of the place, otherwise answer 'no'."},
            ]
        )
        go_to = result2["choices"][0]["message"]["content"] 
        if go_to.lower() != "no." :
            return go_to
        else:
            return result["choices"][0]["message"]["content"]

    
    def handle_prompt(self, user_prompt) -> str:
        if self.current_descr is None:
            self.current_descr = self._prompt(self._build_description(self.current_place)) 
            self.current_place.description = self.current_descr
            return self.current_descr
        else:
            #print(description)

            new_description = self._act_on_user_prompt(user_prompt,self.current_descr)

            possible_location = new_description.lower().removesuffix(".")
            if self.current_place.get_exit_environments().count( possible_location ) == 1:
                for e in self.current_place.exits:
                    if e.environment == possible_location:
                        print("Going to to "+e.environment+".")
                        self.current_place = e
                        self.current_place.build_exits()
                        if self.current_place.description == "":
                            print("Generating description for "+self.current_place.environment+".")
                            self.current_descr = self._prompt(self._build_description(self.current_place))
                            self.current_place.description = self.current_descr
                        else:
                            self.current_descr = self.current_place.description
                        return self.current_descr
            else:
                print(new_description)
                self.current_descr += new_description
                return new_description
        

#Generate a simple world with connected places
#promt to describe. 
#feed environment, places and things
#promt gpt for descriptions and generate conversations 
#store generated and reuse when going to place again or meeting the same people or creature

# import openai

# # Construct your chat messages
# messages = [
#     {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
#     {"role": "user", "content": (
#         "[Environment Details]\n"
#         "- Location: A medieval village\n"
#         "- Weather: Rainy and cold\n"
#         "- Time of day: Early morning\n\n"
#         "[Character Details]\n"
#         "- Character 1: Thalia, a tall female elf ranger with long, silver hair, carrying a longbow and a quiver of arrows\n"
#         "- Character 2: Gorn, a stout male dwarf warrior with a thick red beard, wearing heavy armor and wielding a battleaxe\n\n"
#         "Provide a detailed description of the scene based on the environment and character details provided in JSON format, with \"description\" and \"location\" as fields. location should only contain location name")}
# ]

# # Send the chat messages to the GPT API
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",  # You can use other models like "gpt-3.002" or "gpt-2.002"
#     messages=messages,
#     max_tokens=300,  # Adjust this value depending on the desired length of the response
#     n=1,
#     stop=None,
#     temperature=0.7,
# )

# # Extract the response text
# response_text = response.choices[0].message['content'].strip()

# print(response_text)
