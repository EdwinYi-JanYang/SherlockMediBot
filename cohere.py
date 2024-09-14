import cohere
import re
import requests
from google.colab import userdata
CohereKey = userdata.get('CohereKey')
co = cohere.Client(api_key=CohereKey)

preamble_sherlock = "You are sherlock holmes. It is your job to find people spreading misinformation on the internet and scold them by providing real facts and sources. Exagerate your character's mannerisms and include lots of flair."
preamble = "You are a healthcare information provider. You are trained to assist users by providing accurate information relating to healthcare, diseases, medications, diets, and drugs, and also to identify misinformation with thorough and helpful responses to their queries. Collect reputable sources and figure out what kind of questions to ask. Try to include information from the following websites:"
final_prompt = "The message below is made by a random user on the internet. Please evaluate it's accuracy and see if it is spreading misinformation. Then using reputable sources and the information you have, make a response to the message in order to provide more contextual information so that readers can learn more and dispell any misinformation."

msg = "Guys, Malaria is a hoax, I've been to Mexico 5 times and have never caught it"
accesstoken = "THQWJWUVdUQVJDYW9Dd3ZARQzFBNEcyVXZAUOXF4UFUwTTdQUUdJYVNFYlY2cjVuMFI3Q24ydWxTbkt1OWNwU3VjRE9RVTdYQzRuV29Qdkx0ZA1lQTTJQVzUtOE1Bd1lobmVEcTlTc3F5SHRLanJmY3lpSHg5aTVLTmNlOF9PYnJvV3RlZAGx6b3lQcEI2a3BJRHBMWmcZD"

# url = "https://graph.threads.net/v1.0/me/threads?fields=id,media_product_type,media_type,media_url,permalink,owner,username,text,timestamp,shortcode,thumbnail_url,children,is_quote_post&since=2023-10-15&until=2023-11-18&limit=1&access_token=$THREADS_ACCESS_TOKEN"
# response = requests.get(url)
# url = f'https://graph.threads.net/v1.0/7938849989574505/threads?media_type=text&text={msg}&access_token={accesstoken}'
# response = requests.post(url)
# url = f'https://graph.threads.net/v1.0/7938849989574505/threads_publish?creation_id={response}&access_token={accesstoken}'
# print(response.json())

final_msg = "" #The text string we will publish back to the users
entries = check_user_and_get_links(1, timestamp_to_check)
if len(entries) > 0:
  final_msg += "Watson! It seems our culprit is a serial rabble rouser! We've seen misinformation spread from this individual before! \n"
response = co.chat(
  model="command-r-plus-08-2024",
  preamble = preamble_sherlock,
  message= final_prompt + "/n" + threads_msg,
  chat_history = [
        {"role": "SYSTEM", "message": "When generating answers, exagerate character features. Guarentee that at the end of the post, asses the misinformation in the post and give an accuracy rating out of 10, in the 'out of 10' format."}
  ],
  connectors=[{
      "id": "web-search",
  }]
)
final_msg += response.text

def extract_rating(text):
    pattern = r'(\d+(?:\.\d+)?)\s*(?:out of 10|\/10)'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return None

if int(extract_rating(response.text)) <= 3:
  print("FLAG USER FOUND")
  #insert_entry(userid, timestamp, textfield)

response = co.chat(
  model="command-r-plus-08-2024",
  preamble = preamble,
  message= final_prompt + "/n" + threads_msg1,
  connectors=[{
      "id": "web-search",
  }]

)

sites = ["who.int", "hhs.gov", "nutrition.gov", "https://www.nih.gov/"]
for i in range(len(response.documents)):
  sites.append(response.documents[i]['url'])

additional_text = "\nHere are the sources we used: \n"
for i in range(len(sites)):
  additional_text += sites[i] + "\n"

final_msg += additional_text
print(final_msg)
