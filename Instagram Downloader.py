# Importing the necessary packages
import os
import re
import json
import requests
import urllib.request
from bs4 import BeautifulSoup

# Defining the i_DOWNLOADER() with the base_d as the argument
def i_DOWNLOADER(base_d):
    # Storing the path where to download the instagram posts in the download_path variable
    download_path = "YOUR DOWNLOAD PATH"

    # Fetching the __typename of the POST from base_d dictionary and storing them in typename
    typename = base_d['__typename']

    # Checking if the typename is GraphImage meaning INSTAGRAM POST is a single image
    if typename == "GraphImage":
        # Fetching the Instagram Image URL from display_url of base_d dictionary
        display_url = base_d['display_url']
        # Fetching the taken_at_timestamp value from base_d dictionary and storing in filename
        file_name = base_d['taken_at_timestamp']
        # Concatenating the download_path with the filename and .jpg extension
        download_path += str(file_name)+".jpg"

        # Checking if the file already exists using the os.path.exists() method
        if not os.path.exists(download_path):
            # If not present then download the file using the urlretrieve() of the urlib.request
            # module which takes the url and download_path as the arguments
            urllib.request.urlretrieve(display_url, download_path)
            print(str(file_name) + ".jpg HAS BEEN DOWNLOADED SUCCESSFULLY")
        else:
            # If the file is already present then printing the appropriate message
            print(str(file_name) + ".jpg HAS ALREADY BEEN DOWNLOADED")

    # Checking if the typename is GraphVideo meaning INSTAGRAM POST is a video
    if typename == "GraphVideo":
        # Fetching the Instagram Video URL from video_url of base_d dictionary
        video_url = base_d['video_url']
        # Fetching the taken_at_timestamp value from base_d dictionary and storing in filename
        file_name = base_d['taken_at_timestamp']
        # Concatenating the download_path with the filename and .mp4 extension
        download_path += str(file_name)+".mp4"

        # Checking if the file already exists using the os.path.exists() method
        if not os.path.exists(download_path):
            # If not present then download the file using the urlretrieve() of the urlib.request
            # module which takes the url and download_path as the arguments
            urllib.request.urlretrieve(video_url, download_path)
            print(str(file_name) + ".mp4 HAS BEEN DOWNLOADED SUCCESSFULLY")
        else:
            # If the file is already present then printing the appropriate message
            print(str(file_name) + ".mp4 HAS ALREADY BEEN DOWNLOADED")

    # Checking if typename is GraphSidecar meaning single POST consists of many images & videos
    elif typename == "GraphSidecar":
        # Fetching the value from shortcode of base_d dictionary
        shortcode = base_d['shortcode']
        # Sending request to INSTAGRAM URL with shortcode & converting the response to json
        # storing the response in response
        response = requests.get(f"https://www.instagram.com/p/"+shortcode+"/?__a=1").json()

        # Declaring a variable named post_n and setting it to 1
        post_n = 1

        # Interating through the edges present in the following location of response dictionary
        for edge in response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            # Fetching the taken_at_timestamp value from base_d dictionary and storing in filename
            file_name = response['graphql']['shortcode_media']['taken_at_timestamp']
            # Concatenating download_path with the filename & post_n value & storing in download_p
            download_p = download_path+str(file_name)+"-"+str(post_n)

            # Checking the value of is_video which will be either True or False
            is_video = edge['node']['is_video']

            # If is_video is False meaning single Instagram Post consists of only multiple Images
            if not is_video:
                # Fetching the Image URL from display_url of edge dictionary
                display_url = edge['node']['display_url']
                # Concatenating the download_p value with .jpg extension
                download_p += ".jpg"
                # Checking if the file already exists using the os.path.exists() method
                if not os.path.exists(download_p):
                    # If not present then download the file using the urlretrieve() of the
                    # urlib.request module which takes the url and download_path as the arguments
                    urllib.request.urlretrieve(display_url, download_p)
                    print(str(file_name)+"-"+str(post_n)+".jpg HAS BEEN DOWNLOADED SUCCESSFULLY")
                else:
                    # If the file is already present then printing the appropriate message
                    print(str(file_name)+"-"+str(post_n)+".jpg HAS ALREADY BEEN DOWNLOADED")

            # If is_video is True meaning Instagram Post consists of VIDEO along with the image
            else:
                # Fetching the Video URL from video_url of edge dictionary
                video_url = edge['node']['video_url']
                # Concatenating the download_p value with .mp4 extension
                download_p += ".mp4"

                if not os.path.exists(download_p):
                    urllib.request.urlretrieve(video_url, download_p)
                    print(str(file_name)+"-"+str(post_n)+".mp4 HAS BEEN DOWNLOADED SUCCESSFULLY")
                else:
                    print(str(file_name)+"-"+str(post_n)+".mp4 HAS ALREADY BEEN DOWNLOADED")

            # Incrementing the post_n value by 1
            post_n += 1

# Driver Code
if __name__ == '__main__':
    # Prompting the user to enter the INSTAGRAM POST URL
    insta_url = input("\nENTER THE URL OF THE INSTAGRAM POST : ")
    # Sending request to the insta_url URL & storing the response in insta_Posts
    insta_Posts = requests.get(insta_url)

    # Specifying the desired format of the insta_Comments using html.parser
    # html.parser allows Python to read the components of the insta_Page rather than treating
    # it as a string
    soup = BeautifulSoup(insta_Posts.text, 'html.parser')

    # Finding <script> whose text matches with 'window._sharedData' using re.compile()
    script = soup.find('script', text=re.compile('window._sharedData'))

    # Splitting the text of <script>, 1 time at '=' and fetching the item at index 1
    # followed by removing the ';' from the string and storing the resulting string in page_json
    page_json = script.text.split(' = ', 1)[1].rstrip(';')

    # Parsing the above json page_json string using json_loads() and storing the resulting
    # dictionary in data variable
    # The data dictionary is a very long dictionary consisting of 19 items
    data = json.loads(page_json)

    # Storing the necessary part of the data dictionary in base_data
    base_data = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    # Calling the i_DOWNLOADER() with the base_data as the argument
    i_DOWNLOADER(base_data)

# ---