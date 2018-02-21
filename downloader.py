import os
from robobrowser import RoboBrowser
from string import capwords

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

    for song_link in song_link_list:

        song_name = capwords(song_link.text)
        filepath = save_path + song_name + "/"

        if os.path.isdir(filepath):
            print("SKIPPED: " + song_name)
            continue
        else:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

        browser.open(song_link.find("a")["href"])

        # Find the div containing the lead sheet
        song_img_divs = browser.find_all("div", {"class": "realbook_song_div"})

        multiple_pages = True if len(song_img_divs) > 1 else False
        counter = 1

        for song_img_div in song_img_divs:

            # Skip if it doesn't exist
            if not song_img_div:
                continue

            # Get the image src and its extension
            song_img_src = song_img_div.find("img")["src"]
            file_ext = song_img_src.split(".")[-1]

            page_num = " " + str(counter) if multiple_pages else ""
            filename = song_name + page_num + "." + file_ext

            counter = counter + 1;

            browser.open(song_img_src)

            # Check proper response
            if browser.response.status_code != 200:
                print("Server responded with code " + str(browser.response.status_code) + " for " + song_img_src)
                continue

            # Write the image onto disk
            with open(filepath + filename, "wb") as output:
                output.write(browser.response.content)
                print("SAVED: " + filename)
