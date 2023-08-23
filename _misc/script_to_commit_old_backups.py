from pathlib import Path
import re
import subprocess
from datetime import datetime
import sys
import shutil

START_CONDITION = len(sys.argv) > 1

def sort_key(folder_name):
    match = re.search(r'_(\d+)_', str(folder_name))
    if match:
        return int(match.group(1))
    else:
        return 0

def do_copiar_file(folder_item, destino):
	shutil.copyfile(folder_item, destino)

def do_commit_changes(message, destino):
	subprocess.run(["git", "add", "*"], cwd=destino)
	subprocess.run(["git", "commit", "-m", message])
	
	
def get_commit_message(folder):
	def get_datetime(folder):
		checkdatetime = folder / "map.ini"
		if checkdatetime.exists():
			commit_datetime = datetime.fromtimestamp(checkdatetime.stat().st_mtime)
		else:
			for item in folder.iterdir():
				commit_datetime = datetime.fromtimestamp(item.stat().st_mtime)
				break
		return commit_datetime
	if match1 := re.search(r'_(\d+)_(.+)', folder.name):
		commit_version = float(match1.group(1))
		original_comment = match1.group(2)
		return f"Python generated commit {commit_version}\n   BosPrimigeniusTaurus: The TW \n   Version: {commit_version} \n   Date: {get_datetime(folder)} \n   Message: {original_comment}"
	
def start_copy_and_commit(the_source, the_git_destine):
	source_folder = sorted((folder for folder in the_source.iterdir()),  key=sort_key)
	for folder in source_folder:
		commit_message = get_commit_message(folder)
		for folder_item in folder.iterdir():
			dst = the_git_destine / folder_item.name
			if folder_item.suffix not in {".BfME2Replay", ".jpg"} and folder_item.name not in {"solo.ini"}:
				do_copiar_file(folder_item, dst)
		do_commit_changes(commit_message, the_git_destine)
		
		
if START_CONDITION:
	print("Enough parameters suplied. Operation will begin now")
	SOURCES = Path.cwd() / "Cowmap"
	DESTINO_GIT = SOURCES.parent / "CowlandsTowerDefense3p"
	
	start_copy_and_commit(SOURCES, DESTINO_GIT)
else:
	print("Not enough parameters suplied. Operation won't start")
 



