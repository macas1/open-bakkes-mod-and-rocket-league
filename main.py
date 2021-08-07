# Created by Bradley McInerney 2021
# https://github.com/macas1
#
# Add the correct `BAKKES_MOD_PATH` and `ROCKET_LEAGUE_PATH` constants for your setup.
# If this seems to slow you PC down at all, lower `ROCKET_LEAGUE_CLOSED_CHECK_DLEAY`
# If Bakkes Mod doesn't have time to open and get ready to inject before rocket league opens please raise `BAKKES_MOD_OPEN_BUFFER`
# If Bakkes Mod closes before Rocket League opens raise `ROCKET_LEAGUE_OPEN_BUFFER`

from subprocess import Popen, call, check_output
from time import sleep
from os.path import isfile

# ==========
# Constants
# ==========
BAKKES_MOD_PATH = "C:/Program Files/BakkesMod/BakkesMod.exe"
ROCKET_LEAGUE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/rocketleague/Binaries/Win64/RocketLeague.exe"
BAKKAS_MOD_PROCESS_NAME = "BakkesMod.exe"
ROCKET_LEAGUE_PROCESS_NAME = "RocketLeague.exe"
BAKKES_MOD_OPEN_BUFFER = 0
ROCKET_LEAGUE_OPEN_BUFFER = 120
ROCKET_LEAGUE_CLOSED_CHECK_DLEAY = 5
DEBUG_PRINT = False

# ==========
# Functions
# ==========
def main():
	if not preRunCheck():
		input("Press enter to continue. ")
		return

	bm = runBakkesMod()
	runRocketLeague()
	bm.kill()
	debugPrint("Bakkes Mod killed\nDone")
	
def preRunCheck():
	passed = True

	if not isfile(ROCKET_LEAGUE_PATH):
		print("Rocket League doesn't exist at given path.")
		passed = False

	if not isfile(BAKKES_MOD_PATH):
		print("Bakkes Mod doesn't exist at given path.")
		passed = False

	if process_exists(ROCKET_LEAGUE_PROCESS_NAME):
		print("Rocket League is already running.")
		passed = False

	return passed
	
def runBakkesMod():
	bm = Popen(BAKKES_MOD_PATH)
	debugPrint("Opening Bakkes Mod")
	sleep(BAKKES_MOD_OPEN_BUFFER)
	return bm

def runRocketLeague():
	# Open
	call(ROCKET_LEAGUE_PATH)
	debugPrint("Opening Rocket League")
	sleep(ROCKET_LEAGUE_OPEN_BUFFER)

	# Wait for it to close
	while(process_exists(ROCKET_LEAGUE_PROCESS_NAME)):
		debugPrint("Rocket League is open")
		sleep(ROCKET_LEAGUE_CLOSED_CHECK_DLEAY)
	debugPrint("Rocket League is closed")

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.upper().startswith(str(process_name).upper())

def debugPrint(message):
	if DEBUG_PRINT:
		print(message)

# ==========
# Run
# ==========
if __name__ == "__main__":
	main()
