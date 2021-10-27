import requests
import sys
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Please install BeautifulSoup!\npip install beautifulsoup\npip install bs4")

def main():
    """Le script"""
    print(
        "Parses a (rec) room's RecNet page's metadata to acquire its title, description, image, creator and cheer count."
        +"\nEnter an empty room name to quit.\n"
    )  # Title

    while True:  # Inf loop
        room = input("Room > ")  # Ask for le room
        if not room:  # Exit if nothing input
            break

        # Get and parse RecNet room HTML
        parsed = parse_html(get_room_html(room))

        r_data = {
            "Title": parsed.find("meta",  {"property":"og:title"}),
            "Description": parsed.find("meta",  {"property":"og:description"}),
            "Image": parsed.find("meta", {"property": "og:image"}),
            "Creator": parsed.find("meta", {"name": "twitter:data1"}),
            "Cheers": parsed.find("meta", {"name": "twitter:data2"})
        }  # Unpack data

        if r_data['Title']['content'] == 'Rec Room':  # If it's the front page
            print(f"\n'^{room}' doesn't exist! Either it's an invalid room name, or the name isn't taken!\n")
            continue

        print()  # Empty space
        for data in r_data:  # Go through the data
            if data not in ("Creator", "Cheers"):  # If not twitter card
                print(f"{data}:", r_data[data]["content"] if r_data[data] else "Couldn't find.")
            else:  # Twitter stuff here
                if data == "Cheers":  # This is so I can put thousand separators to cheers!
                    print(f"{data}:", f"{int(r_data[data]['value']):,}" if r_data[data] else "Couldn't find.")
                else:  # Anything but cheers.
                    print(f"{data}:", r_data[data]["value"] if r_data[data] else "Couldn't find.")

        print()  # Empty space for next room

def get_room_html(room):
    """Get the room page's HTML"""
    r = requests.get("https://rec.net/room/" + room)
    return r.text

def parse_html(html):
    """Parses HTML with BeautifulSoup"""
    parsed_html = BeautifulSoup(html, features="html.parser")
    return parsed_html

if __name__ == "__main__":
    """Run le script"""
    main()
