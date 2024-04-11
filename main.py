from keys import consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import schedule
import random
import tweepy
import time
import json
import os

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

# Select a random image from external folder
def select_random_image(folder):
    images = [f for f in os.listdir(folder) if f.endswith('.jpg')]
    return os.path.join(folder, random.choice(images))

# Select a random paragraph from json
with open('random_text.json', 'r') as file:
    paragraphs = json.load(file)

# Check the number of images in the folder
def count_images_in_folder(folder):
    images = [f for f in os.listdir(folder) if f.endswith('.jpg')]
    return len(images)

# Upload image to twitter and create tweet.
def upload_image_and_create_tweet():
    # Meme Folder path
    external_folder = 'O:/memes'

    # Check the number of images in the folder
    num_images = count_images_in_folder(external_folder)

    # Warn if there are less than x imgs
    if num_images < 24:
        print("WARNING: There are less than X imgs left in the folder")

    # Select a random image from the external folder
    image_path = select_random_image(external_folder)

    # Select a random text from JSON file and then remove it from the JSON
    with open('random_text.json', 'r+') as file:
        paragraphs = json.load(file)

        # Select a random paragraph
        selected_paragraph = random.choice(paragraphs)

        # Remove selected Paragraph
        paragraphs.remove(selected_paragraph)

        # Set the file cursor at the beginning
        file.seek(0)

        # Write the modified data back to JSON
        json.dump(paragraphs, file, indent=4)

        # Remove any remaining content after the newly written data
        file.truncate()

    # Upload image to Twitter
    media_id = api.media_upload(filename=image_path).media_id_string

    # Text for the tweet if not paragraph the tweet will have no text
    if selected_paragraph:
        text = selected_paragraph
    else:
        text = ""

    # Create tweet with text and img
    client.create_tweet(text=text, media_ids=[media_id])
    print("Tweeted: ", selected_paragraph + " IMGs: ", image_path)

    # Delete the image file after posting
    os.remove(image_path)
    print("Paragraph's Remaining: ", str(len(paragraphs)), " Img's Remaining: ", num_images)


posting_time = input("Enter the minute interval (00-59): ")

# Schedule the bot to run every hour on the hour
schedule.every().hour.at(f":{posting_time}").do(upload_image_and_create_tweet)

print("Bot started...")

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)





