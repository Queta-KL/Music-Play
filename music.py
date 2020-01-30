import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class MusicalNotation:
	C4HZ=440*2**(-9.0/12.0)
	RAT=(0,2,4,5,7,9,11)
	PIANO=tuple([i/150 for i in (113,11,10,10,17,26,14,2,5,0,0,1)])
	#PIANO=[]
	EPSTOL=1e-4
	NOTEPRECISION=8
	def __init__(self,arg):
		if type(arg) is str:
			self.read(arg)

	def read(self,filename):
		with open(filename, "r") as f:
			self.f0,self.bpm=np.fromstring(f.readline(),sep=' ')
			self.stress=np.fromstring(f.readline(),sep=' ')
			self.score=np.fromstring(f.read(),sep=' ').reshape((-1,2))
		self.f0Hz=self.C4HZ*2**(self.nmn2ratSingle(self.f0)/12)

	def checkNotePrecision(self,acc):
		if np.abs(acc*self.NOTEPRECISION-np.round(acc*self.NOTEPRECISION))<self.EPSTOL:
			acc=np.round(acc*self.NOTEPRECISION)/self.NOTEPRECISION
		return acc
	
	def __str__(self):
		return "Major: %s (%d)\n"\
			"BPM:   %d beats/min\n"\
			"Meter: %d beats/bar %s"%(
				chr(int((np.abs(self.f0)+1)%7)+65)+("#" if np.floor(self.f0)!=self.f0 else ""),
				4+int(self.f0)//7-int(self.f0>0 and self.f0//7==self.f0/7),
				self.bpm,
				len(self.stress),str(self.stress))

	def __repr__(self):
		ans=str(self)
		num=acc=0
		ans+="\nScore:\n"+'-'*16+' (%d)'%num+'\n'
		for k,t in self.score:
			if acc >= len(self.stress):
				num+=1
				ans+='-'*16+' (%d)'%num+'\n'
				acc%=len(self.stress)
			ans+='('+str(k)+', '+str(t)+') '
			accLst=acc
			acc=self.checkNotePrecision(acc+t)
			if np.floor(accLst)!=np.floor(acc):
				ans+='\n'
		return ans

	def nmn2ratSingle(self,x):
		t=np.floor(np.abs(x)-1)
		return self.RAT[int(t%7)]+((int(x>0)<<1)-1)*12*(np.floor(t/7)+int(x<0))+2*(np.abs(x)-1-t)

	def nmn2rat(self):
		return [np.NINF if x==0 else self.nmn2ratSingle(x) for x in self.score[:,0]]

	def nmn2wav(self,fs=44100):
		ans=np.zeros(int(np.ceil(60*fs*(self.score[:,1].sum()+len(self.stress))/self.bpm)))
		acc=0
		for k,t in np.vstack((self.nmn2rat(),self.score[:,1])).T:
			temp=self.wavSingle(k,t,fs,self.stress[int(acc%len(self.stress))])
			bgn=int(np.ceil(60*fs*acc/self.bpm))
			ans[bgn:bgn+len(temp)]+=temp
			acc=self.checkNotePrecision(acc+t)
		ans/=np.abs(ans).max()
		#plt.figure()
		#plt.plot(ans)
		#plt.show()
		return ans

	def nmn2MusicPlayer(self,fs=44100):
		return MusicPlayer(self.nmn2wav(fs))

	def envelope(self,k,t,fs,a):
		ans=np.zeros(int(np.ceil(fs*((60*t)/self.bpm+0.3))))
		if 60*t/self.bpm>0.2:
			# arise
			arise=0.02
			overload=1.4
			bgn=0
			n=int(np.round(arise*fs))
			ans[bgn:n]=overload*np.exp(-np.square((1-np.arange(n)/n)*3))
			bgn+=n
			# keep 1
			keep1=0.01
			height1=0.999
			end=np.sqrt(1/(-np.log(1-height1)))
			n=int(np.round(keep1*fs))
			ans[bgn:bgn+n]=overload*(1-np.exp(-1/np.square(np.arange(n)/n*end+1e-4)))
			bgn+=n
			# drop
			drop1=0.3
			n=int(np.round(drop1*fs))
			ans[bgn:bgn+n]=1+(height1*overload-1)*np.exp(-np.square(np.arange(n)/n*3))
			bgn+=n
			# keep 2
			keep2=0.02
			height2=0.999
			end=np.sqrt(1/(-np.log(1-height2)))
			n=int(np.round(keep2*fs))
			ans[bgn:bgn+n]=1-np.exp(-1/np.square(np.arange(n)/n*end+1e-4))
			bgn+=n
			# decay
			fall=0.4
			n=len(ans)-bgn-int(np.round(fall*fs))
			ans[bgn:bgn+n]=height2*np.exp(-np.arange(n)/n*1.2)
			end=ans[bgn+n-1]
			bgn+=n
			# fall
			n=len(ans)-bgn
			ans[bgn:]=end*np.exp(-np.square(np.arange(n)/n*3))
		else:
			# arise
			arise=0.015
			overload=1.4
			bgn=0
			n=int(np.round(arise*fs))
			ans[bgn:n]=overload*np.exp(-np.square((1-np.arange(n)/n)*3))
			bgn+=n
			# keep 1
			keep1=0.01
			height1=0.999
			end=np.sqrt(1/(-np.log(1-height1)))
			n=int(np.round(keep1*fs))
			ans[bgn:bgn+n]=overload*(1-np.exp(-1/np.square(np.arange(n)/n*end+1e-4)))
			bgn+=n
			# drop
			drop1=0.15
			n=int(np.round(drop1*fs))
			ans[bgn:bgn+n]=1+(height1*overload-1)*np.exp(-np.square(np.arange(n)/n*3))
			bgn+=n
			# keep 2
			keep2=0.02
			height2=0.999
			end=np.sqrt(1/(-np.log(1-height2)))
			n=int(np.round(keep2*fs))
			ans[bgn:bgn+n]=1-np.exp(-1/np.square(np.arange(n)/n*end+1e-4))
			bgn+=n
			# decay
			fall=0.3
			n=len(ans)-bgn-int(np.round(fall*fs))
			ans[bgn:bgn+n]=height2*np.exp(-np.arange(n)/n*1.2)
			end=ans[bgn+n-1]
			bgn+=n
			# fall
			n=len(ans)-bgn
			ans[bgn:]=end*np.exp(-np.square(np.arange(n)/n*2.2))
		ans*=a
		#plt.cla()
		#plt.plot(ans)
		return ans

	def wavSingle(self,k,t,fs,a):
		omg=np.pi*self.f0Hz*(2**(1+k/12))/fs
		x=np.arange(int(np.ceil(fs*((60*t)/self.bpm+0.3))))
		y=np.sin(omg*x)
		for i,amp in enumerate(self.PIANO):
			y+=amp*np.sin((i+2)*omg*x)
		y*=self.envelope(k,t,fs,a)
		
		#plt.cla()
		#plt.plot(y)
		return y



class MusicPlayer:
	def __init__(self,arg):
		if type(arg) is str:
			self.read(arg)
		else:
			self.fs=44100
			self.wav=np.array(arg,dtype='float32')

	def read(self,filename):
		self.fs,self.wav=wavfile.read(filename)
		self.wav=np.array(self.wav,dtype='float')
		self.wav/=np.abs(self.wav).max()

	def write(self,filename):
		wavfile.write(filename,self.fs,np.array(self.wav,dtype='float32'))

	def display(self,end=-1):
		fig=plt.figure()
		if end==-1:
			end=len(self.wav)
		plt.plot([i/self.fs for i in range(end)],self.wav[:end])
		plt.xlabel(r'time $t/\mathrm{s}$')
		plt.ylabel(r'normalized frame $A$')
		plt.title('Wave frames')
		fig.tight_layout()

	def displayFFT(self,end=-1):
		fig=plt.figure()
		if end==-1:
			end=len(self.wav)
		plt.plot(np.linspace(0,self.fs,num=len(self.wav[:end]),endpoint=False),abs(np.fft.fft(self.wav)))
		plt.xlabel(r'frequency $f/\mathrm{Hz}$')
		plt.ylabel(r'magnitude $\|F(f)\|$')
		plt.title('Frequency Domain of the Wave')
		fig.tight_layout()

	def __str__(self):
		length=len(self.wav)/self.fs
		return "Sampling freq: %d Hz\n"\
			"Channel(s):    %d\n"\
			"Length:        %d min %.3f sec"%(
				self.fs,self.wav.ndim,
				length//60,
				length%60)

def main():
	print("class MusicalNotation")
	print("class MusicPlayer")

if __name__ == '__main__':
	main()
