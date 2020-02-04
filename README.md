# Music-Play
It is used for play numbered musical notation.
But you need to provide a text file as the numbered musical notation, which could be not so convenient.


There are two examples:
* Freude.txt (*Ode to Joy* / *An die Freude*)
* InTheSpring.txt (A popular song in *Belief Flies in the Wind (2009)* by Wang Feng, a Chinese rock musician and composer)

You might need **ffmpeg** [link](https://ffmpeg.zeranoe.com/builds/) for packge of **pydub**.

## input
A numbered musical notation (like Freude.txt).

The first line includes two numbers that is the key and BPM (beats per minute).

* 1   -- C  (4)
* 1.5 -- C# (4)
* 2   -- B  (4)
* 2.5 -- B# (4)
* 3   -- D  (4)
* 4   -- E  (4)

The second line includes several numbers that beats per bar (metre). 

* ([3 1 2 1] -- [f p mf p] as 4-4 metre)
* ([3 1 1 2 1 1] -- [f p p mf p p] as 8-6 metre)

"Freude.txt":
```cmd
1 120
3 1 2 1

3 1
3 1
4 1
5 1
5 1
4 1
3 1
2 1
1 1
1 1
2 1
3 1
3 1.5
2 0.5
2 2
3 1
3 1
4 1
5 1
5 1
4 1
3 1
2 1
1 1
1 1
2 1
3 1
2 1.5
1 0.5
1 2
2 1
2 1
3 1
1 1
2 1
3 0.5
4 0.5
3 1
1 1
2 1
3 0.5
4 0.5
3 1
2 1
1 1
2 1
-5 1
3 2
3 1
4 1
5 1
5 1
4 1
3 1
4 0.5
2 0.5
1 1
1 1
2 1
3 1
2 1.5
1 0.5
1 2

```

## Output
a wav file.
