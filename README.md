# LoLAutoRunes
Grab runes from popular sites and automatically set your rune page based on the game mode and champion.

## To Do

Startup:
- Get LCU port & password from running client process **DONE**
- Check client version and verify the downloaded json is up to update
- Add Mac/Unix support

Rune Selection:
- Add web scrape to determine necessary runes **DONE**
- Add more rune pages sources
- Map rune names to rune IDs **DONE**
- Check if current page is a default page (to determine if removable)

General:
- Add checking to see if in match
- Create cross-platform GUI to easily select rune source
- validate functionality with all champions
- Add summoner spell functionality

## Installation

1. Clone the repository
2. Run the following command in a terminal located in the cloned repo:
`pip install -r requirements.txt`
3. Run the following command to start the program:
`python runes.py`
