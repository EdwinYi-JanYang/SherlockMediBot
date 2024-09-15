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
def add_br_after_sentences(text):
    # This pattern matches sentences ending with . ! or ?
    # It also accounts for sentences that end with quotation marks
    pattern = r'([.!?]"?)(\s+|\Z)'
    
    # Replace the matched pattern with the punctuation, followed by <br> and any whitespace
    result = re.sub(pattern, r'\1<br>\2', text)
    
    return result

final_msg += add_br_after_sentences(response.text)


entries = check_user_and_get_links(1, timestamp_to_check)
if len(entries) > 0:
    final_msg += "<br><br> Watson! It seems our culprit is a serial rabble rouser! We've seen misinformation spread from this individual before! <br>"

def extract_rating(text):
    pattern = r'(\d+(?:\.\d+)?)\s*(?:out of 10|\/10)'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return None

if int(extract_rating(response.text)) <= 3:
    print("FLAG USER FOUND")
    # insert_entry(userid, timestamp, textfield)

sites = ["https://www.who.int", "https://www.hhs.gov", "https://www.nutrition.gov", "https://www.nih.gov/", "https://www.nfid.org/infectious-diseases/", "https://www.niams.nih.gov/health-topics/all-diseases", "https://www.malacards.org/"]
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

additional_text = "<br><br> Here are the sources we used: <br>"
for i in range(len(sites)):
    additional_text += '<a href="' + sites[i] + '">' + sites[i] + '</a><br>'

final_msg += additional_text
print(final_msg)

# Function to update the message in index.html
additional_text = "<br><br> Here are the sources we used: <br>"
sites = ["https://www.who.int", "https://www.hhs.gov", "https://www.nutrition.gov", "https://www.nih.gov/", "https://www.nfid.org/infectious-diseases/", "https://www.niams.nih.gov/health-topics/all-diseases", "https://www.malacards.org/"]
for i in range(len(sites)):
    additional_text += '<a href="' + sites[i] + '">' + sites[i] + '</a><br>'

suspect_username = "someDeviousUser1"
msg = "Guys, Malaria is a hoax, I've been to Mexico 5 times and have never caught it"
final_msg = "My dear Watson, I must say, I am not surprised that you have brought this case to my attention.<br> It is clear that this individual is spreading misinformation and I shall do my utmost to correct them.<br> Malaria is a serious and sometimes fatal disease transmitted by mosquitoes.<br> It is not a hoax.<br> While the risk of malaria in Mexico is low, it is present intermittently throughout the year.<br> In recent years, the states of Campeche, Chiapas, Chihuahua, Durango, Nayarit, Oaxaca, Quintana Roo, Sinaloa and Tabasco have reported cases.<br> Malaria precautions are essential.<br> One must avoid mosquito bites by covering up with clothing such as long sleeves and long trousers, especially after sunset, using insect repellents on exposed skin and, when necessary, sleeping under a mosquito net.<br> I must also point out that this individual's experience is not a reliable indicator of the prevalence of malaria in Mexico.<br> Just because they have not caught malaria does not mean that it is a hoax.<br> It is possible that they have not been exposed to the disease or that they have been taking the necessary precautions to avoid it.<br> I would advise this individual to be more careful in the future and to refrain from spreading misinformation.<br> As for the accuracy of this post, I would give it a rating of 1 out of 10.<br> Yours sincerely, Sherlock Holmes<br><br> Watson! It seems our culprit is a serial rabble rouser! We've seen misinformation spread from this individual before! <br>"

def generate_sources_list(sources):
    """Generate HTML for the sources list."""
    temp = ''.join(f'<li><a href="{source}">{source}</a></li>' for source in sources)
    print("sources: " + temp)
    return temp

def generate_mystery_chamber(suspect_username, message, final_msg, additional_text):
    """
    Generate the HTML content for Sherlock's Mystery Chamber.
    
    :param suspect_username: The username of the suspect
    :param message: The message content
    :param final_msg: The final message about the investigation
    :param additional_text: A list of sources
    :return: The generated HTML content as a string
    """
    sources_list_html = generate_sources_list(sites)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sherlock's Mystery Chamber</title>
        <style>
            body {{
                background-color: #1a1a1a;
                font-family: 'Georgia', serif;
                color: #e0e0e0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-image: url('https://t3.ftcdn.net/jpg/03/20/02/22/360_F_320022201_iskWgYQZDICRWh64UPxwyV97EBOiQS3z.jpg');
                background-size: cover;
                background-position: center;
            }}
            #content {{
                background-color: rgba(0, 0, 0, 0.8);
                border: 2px solid #8B4513;
                border-radius: 15px;
                padding: 30px;
                width: 90%;
                max-width: 800px;
                box-shadow: 0 0 20px rgba(139, 69, 19, 0.5);
            }}
            h1 {{
                font-size: 2.8em;
                margin-bottom: 20px;
                color: #d4af37;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }}
            #case-file {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #8B4513;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                text-align: left;
            }}
            #update-message {{
                font-size: 1.2em;
                margin-top: 20px;
                line-height: 1.6;
            }}
            .image-container {{
                width: 200px;
                height: 200px;
                margin: 20px auto;
                border-radius: 50%;
                overflow: hidden;
                background-color: #FFA500;
                display: flex;
                justify-content: center;
                align-items: center;
                border: 3px solid #8B4513;
                box-shadow: 0 0 15px rgba(139, 69, 19, 0.7);
            }}
            .image-container img {{
                width: 180px;
                height: auto;
            }}
            .message {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid #8B4513;
                border-radius: 5px;
                padding: 10px;
                margin-top: 15px;
                font-style: italic;
            }}
            .button {{
                background-color: #d4af37;
                color: #1a1a1a;
                border: none;
                padding: 10px 20px;
                font-size: 1.2em;
                margin-top: 20px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-right: 10px;
            }}
            .button:hover {{
                background-color: #ffd700;
            }}
            #sources {{
                display: none;
                margin-top: 20px;
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #8B4513;
                border-radius: 10px;
                padding: 20px;
                text-align: left;
            }}
            .suspect {{
                font-weight: bold;
                color: #d4af37;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <script>
            function solveMystery() {{
                alert("Elementary, my dear Watson! The culprit has indeed been caught. Their spread of misinformation has been halted, thanks to our diligent investigation. The internet shall be a bit safer now.");
            }}

            function toggleSources() {{
                var sourcesDiv = document.getElementById("sources");
                var button = document.getElementById("toggle-sources");
                if (sourcesDiv.style.display === "none") {{
                    sourcesDiv.style.display = "block";
                    button.textContent = "Hide Sources";
                }} else {{
                    sourcesDiv.style.display = "none";
                    button.textContent = "Show Sources";
                }}
            }}
        </script>
        <div id="content">
            <h1>Sherlock's Mystery Chamber</h1>
            <div class="image-container">
                <img src="https://cdn.pixabay.com/photo/2013/07/12/13/46/sherlock-holmes-147255_1280.png" alt="Sherlock Holmes" />
            </div>
            <div id="case-file">
                <h2>Case File: The Misinformation Menace</h2>
                <p>A nefarious individual has been spreading misinformation across the internet. It's up to you, dear Watson, to assist in uncovering the truth.</p>
                <p class="suspect">Suspect: @{suspect_username}</p>
                <div class="message">
                    <p>{message}</p>
                </div>
            </div>
            <p id="update-message">{final_msg}</p>
            <button class="button" id="solve-button">Solve the Mystery</button>
            <button class="button" id="toggle-sources">Show Sources</button>
            <div id="sources" style="display: none;">
                <h3>Sources:</h3>
                <ul id="source-list">
                    {sources_list_html}
                </ul>
            </div>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                document.getElementById("solve-button").addEventListener("click", solveMystery);
                document.getElementById("toggle-sources").addEventListener("click", toggleSources);
            }});
        </script>
    </body>
    </html>
    """
    return html_content

def update_html_message(new_message):
    GITHUB_TOKEN = ''  # Your GitHub token
    REPO_OWNER = 'EdwinYi-JanYang'  # Your GitHub username
    REPO_NAME = 'SherlockMediBot'  # Your GitHub Pages repo name
    FILE_PATH = 'index.html'  # Path to the file you want to update

    # Generate the new content
    new_content = generate_mystery_chamber(suspect_username, msg, new_message, sites)

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


update_html_message(final_msg)