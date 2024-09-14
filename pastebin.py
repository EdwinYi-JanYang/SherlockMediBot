import requests

def create_paste(api_dev_key, api_paste_code, api_paste_name='', api_paste_format='python', api_paste_private=0, api_paste_expire_date='10M', image_url=''):
    # Include the image URL at the top of the paste content as a clickable link
    if image_url:
        api_paste_code = f"Image: {image_url}\n\n{api_paste_code}"

    # API endpoint
    url = 'https://pastebin.com/api/api_post.php'

    # Data to be sent
    data = {
        'api_dev_key': api_dev_key,
        'api_option': 'paste',
        'api_paste_code': api_paste_code,
        'api_paste_name': api_paste_name,
        'api_paste_format': api_paste_format,
        'api_paste_private': api_paste_private,
        'api_paste_expire_date': api_paste_expire_date
    }

    # Send POST request
    response = requests.post(url, data=data)

    # Check if paste was created successfully
    if response.status_code == 200:
        return response.text  # Returns the URL of the paste
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
api_dev_key = 'tYgiZroLZVqF94WQ5RXThj-B47xh7YTG'  # Replace with your actual API key
text_to_paste = final_msg
paste_name = "Sherlock MediBot Test"
image_url = "https://cdn.pixabay.com/photo/2013/07/12/13/46/sherlock-holmes-147255_1280.png"  # Replace with the actual image URL

result = create_paste(api_dev_key, text_to_paste, paste_name, image_url=image_url)
print(result)
