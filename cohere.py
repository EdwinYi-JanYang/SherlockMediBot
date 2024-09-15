import cohere
import re
import requests
from google.colab import userdata
import base64
import json

CohereKey = userdata.get('CohereKey')
co = cohere.Client(api_key=CohereKey)

preamble_sherlock = "You are Sherlock Holmes. It is your job to find people spreading misinformation on the internet and scold them by providing real facts and sources. Exaggerate your character's mannerisms and include lots of flair."
preamble = "You are a healthcare information provider. You are trained to assist users by providing accurate information relating to healthcare, diseases, medications, diets, and drugs, and also to identify misinformation with thorough and helpful responses to their queries. Collect reputable sources and figure out what kind of questions to ask. Try to include information from the following websites:"
final_prompt = "The message below is made by a random user on the internet. Please evaluate its accuracy and see if it is spreading misinformation. Then using reputable sources and the information you have, make a response to the message in order to provide more contextual information so that readers can learn more and dispel any misinformation."

msg = "Guys, Malaria is a hoax, I've been to Mexico 5 times and have never caught it"
accesstoken = "YOUR_ACCESS_TOKEN"

final_msg = ""  # The text string we will publish back to the users

response = co.chat(
    model="command-r-plus-08-2024",
    preamble=preamble_sherlock,
    message=final_prompt + "\n" + msg,
    chat_history=[
        {"role": "SYSTEM", "message": "When generating answers, exaggerate character features. Guarantee that at the end of the post, assess the misinformation in the post and give an accuracy rating out of 10, in the 'out of 10' format."}
    ],
    connectors=[{
        "id": "web-search",
    }]
)
final_msg += response.text


entries = check_user_and_get_links(1, timestamp_to_check)
if len(entries) > 0:
    final_msg += "\nWatson! It seems our culprit is a serial rabble rouser! We've seen misinformation spread from this individual before! \n"

def extract_rating(text):
    pattern = r'(\d+(?:\.\d+)?)\s*(?:out of 10|\/10)'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return None

if int(extract_rating(response.text)) <= 3:
    print("FLAG USER FOUND")
    # insert_entry(userid, timestamp, textfield)

sites = ["who.int", "hhs.gov", "nutrition.gov", "https://www.nih.gov/", "https://www.nfid.org/infectious-diseases/", "https://www.niams.nih.gov/health-topics/all-diseases", "https://www.malacards.org/"]
response = co.chat(
    model="command-r-plus-08-2024",
    preamble=preamble,
    message=final_prompt + "\n" + msg,
    connectors=[{
        "id": "web-search",
        "sites": sites
    }]
)
for i in range(len(response.documents)):
    sites.append(response.documents[i]['url'])

additional_text = "\nHere are the sources we used: \n"
for i in range(len(sites)):
    additional_text += sites[i] + "\n"

final_msg += additional_text
print(final_msg)

# Function to update the message in index.html
def update_html_message(new_message):
    GITHUB_TOKEN = ''
    REPO_OWNER = 'EdwinYi-JanYang'  # Your GitHub username
    REPO_NAME = 'SherlockMediBot'  # Your GitHub Pages repo name
    FILE_PATH = 'index.html'  # Path to the file you want to update

    # New content for the file
    new_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sherlock Misinformation Search</title>
        <style>
            body {{
                background-color: #f5f5dc; /* Light beige background */
                font-family: 'Georgia', serif; /* Classic font for a vintage feel */
                color: #333; /* Dark text color for readability */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
                margin: 0;
            }}
            #content {{
                border: 2px solid #8B4513; /* Brown border */
                border-radius: 10px;
                padding: 20px;
                width: 80%;
                max-width: 600px;
                background-color: #fff; /* White background for content */
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            }}
            h1 {{
                font-size: 2.5em; /* Larger heading */
                margin-bottom: 10px;
            }}
            #update-message {{
                font-size: 1.2em; /* Slightly larger text for the update message */
                margin-top: 15px; /* Spacing above the message */
            }}
            img {{
                width: 150px; /* Resize the image to be smaller */
                height: auto; /* Maintain aspect ratio */
                margin-top: 20px; /* Space above the image */
                border: 2px solid #8B4513; /* Brown border around the image */
                border-radius: 5px; /* Rounded corners for the image */
            }}
        </style>
    </head>
    <body>
        <div id="content">
            <h1>You've been caught!</h1>
            <p>Sherlock has determined you've been spreading misinformation on the internet.</p>
            <p id="update-message">{final_msg}</p>
            <img src="https://cdn.pixabay.com/photo/2013/07/12/13/46/sherlock-holmes-147255_1280.png" alt="Sherlock Holmes" />
        </div>
    </body>
    </html>
    """

    # Get the current file's SHA to update it
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get the current file info
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha']  # Get the SHA of the current file

        # Prepare the new content
        encoded_content = base64.b64encode(new_content.encode()).decode()

        # Prepare the data for the update
        data = {
            'message': 'Update index.html via API',
            'content': encoded_content,
            'sha': sha
        }

        # Update the file
        update_response = requests.put(url, headers=headers, data=json.dumps(data))
        if update_response.status_code == 200:
            print("File updated successfully!")
        else:
            print(f"Error updating file: {update_response.status_code}, {update_response.text}")
    else:
        print(f"Error fetching file info: {response.status_code}, {response.text}")

# Call the update function with the final message
update_html_message(final_msg)