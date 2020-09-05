import os
from user import Sub
import re
import subprocess

SUB_STATE_EMPTY=0
SUB_STATE_GOT_NUMBER=1
SUB_STATE_GOT_TIME=2
SUB_STATE_GOT_SOME_TEXT=3
SUB_STATE_FINISHED=4

def decompileSubs(id):
	f = open("/home/mikhail_kozyrev_nn/bot/service/download/BQACAgIAAxkBAAIBFV9P0pq7pcovOT5fleDoVeM548GXAAJyCQACr_1hSp8UN2DXfHqyGwQ", "r", encoding="latin-1")
	textArr = f.readlines()
	subsArr = []
	tmpSub = None
	for i,line in enumerate(textArr):
		if re.match("\d+$", line) != None:
			tmpSub = Sub(line.rstrip('\n'), "?????", "!!!!!")

			if re.match("\d{2}:\d{2}:\d{2}.* --> \d{2}:\d{2}:\d{2}.*", textArr[i+1]) != None:
				tmpSub.time =  textArr[i+1].rstrip('\n')
#				print("line: " + str(i) + " - " +  textArr[i+1])
				for nLine in textArr[i+2:]:
#					if re.match("\w+ && !(\d+$) && !(\d{2}:\d{2}:\d{2}.* --> \d{2}:\d{2}:\d{2}.*)", nLine) != None:
					if re.match("\w+", nLine) != None:
						tmpSub.text += nLine
#						print("line: " + str(i) + " - " + nLine)
					else:
#						print("=================================================")
						break
			subsArr.append(tmpSub)

	for s in subsArr:
		s.dump()

	f.close()

def main():
	#decompileSubs(0)
	#path = "/home/mikhail_kozyrev_nn/bot/service/download/BQACAgIAAxkBAAIBel9RHazcHGMdckWmS4VVoDyUZpIrAAJxBwACk_iRSufPFh492uzIGwQ"
	#returned_output = subprocess.check_output('/usr/bin/file -i ' + path + '| awk \'{print $3}\' | sed "s|charset=||g"', shell=True)
	print('Current date is:', returned_output.decode("utf-8"))

if __name__ == '__main__':
	main()