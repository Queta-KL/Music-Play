import music
import numpy as np
import pydub

def main():
	scoreList=("Freude",
		"InTheSpring",
		"TheMoonOfLuzhou")
	inputFile=".\\MusicScore\\"
	outputFile=".\\output\\"
	for score in scoreList:
		haha=music.MusicalNotation(inputFile+score+r".txt")
		haha.nmn2MusicPlayer().write(outputFile+score+r".wav")
		sound=pydub.AudioSegment.from_wav(outputFile+score+r".wav")
		sound.export(outputFile+score+r".mp3", format="mp3")
		print(score,"OK")
	return

if __name__ == '__main__':
	main()
