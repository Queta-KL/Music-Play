# Music-Play
It is used for play numbered musical notation.
But you need to provide a text file as the numbered musical notation, which could be not so convenient.


There are two examples:
* Freude.txt (Ode to Joy / An die Freude)
* InTheSpring.txt (A popular song by Feng Wang)


## input
A numbered musical notation (like Freude.txt).

The first line includes two numbers that is the key (1 -- C4, 2 -- B4, 3-- E4) and BPM (beats per minute).

The second line includes several numbers that beats per bar (metre). 

([3 1 2 1] -- [f p mf p] as 4-4 metre)
([3 1 1 2 1 1] -- [f p p mf p p] as 8-6 metre)

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
