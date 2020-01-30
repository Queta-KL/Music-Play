import music

def main():
	haha=music.MusicalNotation(r"Freude.txt")
	haha.nmn2MusicPlayer().write(r"Freude.wav")

if __name__ == '__main__':
	main()
