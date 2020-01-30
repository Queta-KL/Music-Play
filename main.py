import music

def main():
	haha=music.MusicalNotation(r"InTheSpring.txt")
	haha.nmn2MusicPlayer().write(r"InTheSpring.wav")

if __name__ == '__main__':
	main()
