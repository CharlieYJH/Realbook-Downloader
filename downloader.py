import os
from robobrowser import RoboBrowser
from string import capwords

def check_filename(directory, name):
    for f in os.listdir(os.path.dirname(directory)):
        if os.path.splitext(f)[0] == name:
            return True
    return False

url = "http://www.guitarcats.com/realbook-jazz-standards/A"

# Open up HTML
browser = RoboBrowser(parser="html.parser", history=True)
browser.open(url)

if browser.response.status_code != 200:
    print("Server responded with code " + str(browser.response.status_code) + " for " + url)
    print("Exiting...")
    quit()

links = browser.find_all("a", {"class": "realbook_letter_link"})

for link in links:

    # Open A-Z categories 1 by 1
    browser.open(link["href"])

    # Check proper response
    if browser.response.status_code != 200:
        print("Server responded with code " + str(browser.response.status_code) + " for " + link["href"])
        continue

    # Get current category and find all its songs
    letter = link["href"][-1]
    save_path = "./Lead Sheets/" + letter + "/"
    song_link_list = browser.find_all("li", {"class": "realbooks_song_li"})

    # Make a folder for the current category
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    for song_link in song_link_list:

        song_name = capwords(song_link.text)

        # Check if this song is already saved
        if (check_filename(save_path, song_name)):
            print("SKIPPED: " + song_name)
            continue

        browser.open(song_link.find("a")["href"])

        # Find the div containing the lead sheet
        song_img_div = browser.find("div", {"class": "realbook_song_div"})

        # Skip if it doesn't exist
        if not song_img_div:
            continue

        # Get the image src and its extension
        song_img_src = song_img_div.find("img")["src"]
        file_ext = song_img_src.split(".")[-1]

        filename = save_path + song_name + "." + file_ext

        #  if os.path.isfile(filename):
            #  print("SKIPPED: " + song_name)
            #  continue

        browser.open(song_img_src)

        # Check proper response
        if browser.response.status_code != 200:
            print("Server responded with code " + str(browser.response.status_code) + " for " + song_img_src)
            continue

        # Write the image onto disk
        with open(save_path + song_name + "." + file_ext, "wb") as output:
            output.write(browser.response.content)
            print("SAVED: " + song_name)
