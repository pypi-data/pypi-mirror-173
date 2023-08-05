# ELIZA
# By Jeff Shrager.
# From David H. Ahl & Steve North, More BASIC Computer Games, Workman, 1980.

# An early natural language processing chatterbot program. The computer searches
# for keywords in your entries, and responds appropriately in the manner of a
# Rogerian psychotherapist (providing only the illusion of comprehension). This
# BASIC version is less sophisticated than Joseph's original, and you need to
# carry the conversation with longer, rather than succinct, responses.

# Changes:
# - Appended author and year to title.
# - Added the instructions on lines 20 through 22.

# As per Steve's notes, lines 120, 420, and 590 could be replaced with RESTORE
# 2500, 1200, and 1300, respectively, while the various substring search loops
# using MID$ could be replaced with INSTR.

1 PRINT TAB(26);"ELIZA"
2 PRINT TAB(20);"Creative Computing"
3 PRINT TAB(18);"Morristown, New Jersey"
4 PRINT
5 PRINT TAB(18);"by Jeff Shrager (1973)"
6 PRINT TAB(9);"after Joseph Weizenbaum's original (1966)"
7 PRINT TAB(12);"adapted to MS BASIC by Steve North"
8 PRINT TAB(27);"1977"
9 PRINT:PRINT:PRINT
20 PRINT "Responses with commas should be wrapped in double quotes."
21 PRINT "It is best to avoid punctuation altogether."
22 PRINT "'Shut up' quits.":PRINT
80 REM     -----INITIALIZATION-----
100 DIM S(36),R(36),N(36)
110 N1=36:N2=14:N3=112
120 FOR X=1 TO N1+N2+N3:READ Z$:NEXT X:REM SAME AS RESTORE 2500
130 FORX=1 TO N1
140 READ S(X),L:R(X)=S(X):N(X)=S(X)+L-1
150 NEXT X
160 PRINT "Hi!  I'm Eliza.  What's your problem?"
170 REM
180 REM     -----USER INPUT SECTION-----
190 REM
200 INPUT I$
201 I$=" "+I$+"  "
210 REM  GET RID OF APOSTROPHES
220 FOR L=1 TO LEN(I$)
230 IFMID$(I$,L,1)="'"THENI$=LEFT$(I$,L-1)+RIGHT$(I$,LEN(I$)-L):GOTO230
240 IFL+4<=LEN(I$)THENIFMID$(I$,L,4)="shut"THENPRINT"Shut up...":END
250 NEXT L
255 IF I$=P$ THEN PRINT "Please don't repeat yourself!":GOTO 170
260 REM
270 REM     -----FIND KEYWORD IN I$-----
280 REM
290 RESTORE
295 S=0
300 FOR K=1 TO N1
310 READ K$
315 IF S>0 THEN 360
320 FOR L=1 TO LEN(I$)-LEN(K$)+1
340 IF MID$(I$,L,LEN(K$))=K$THENS=K:T=L:F$=K$
350 NEXT L
360 NEXT K
365 IF S>0 THEN K=S:L=T:GOTO390
370 K=36:GOTO570:REM  WE DIDN'T FIND ANY KEYWORDS
380 REM
390 REM     TAKE RIGHT PART OF STRING AND CONJUGATE IT
400 REM     USING THE LIST OF STRINGS TO BE SWAPPED
410 REM
420 RESTORE:FORX=1 TO N1:READ Z$:NEXT X:REM SKIP OVER KEYWORDS
430 C$=" "+RIGHT$(I$,LEN(I$)-LEN(F$)-L+1)+" "
440 FOR X=1 TO N2/2
450 READ S$,R$
460 FOR L= 1 TO LEN(C$)
470 IF L+LEN(S$)>LEN(C$) THEN 510
480 IF MID$(C$,L,LEN(S$))<>S$ THEN 510
490 C$=LEFT$(C$,L-1)+R$+RIGHT$(C$,LEN(C$)-L-LEN(S$)+1)
495 L=L+LEN(R$)
500 GOTO 540
510 IF L+LEN(R$)>LEN(C$)THEN540
520 IF MID$(C$,L,LEN(R$))<>R$ THEN 540
530 C$=LEFT$(C$,L-1)+S$+RIGHT$(C$,LEN(C$)-L-LEN(R$)+1)
535 L=L+LEN(S$)
540 NEXT L
550 NEXT X
555 IF MID$(C$,2,1)=" "THENC$=RIGHT$(C$,LEN(C$)-1):REM ONLY 1 SPACE
556 FOR L=1 TO LEN(C$)
557 IF MID$(C$,L,1)="!" THEN C$=LEFT$(C$,L-1)+RIGHT$(C$,LEN(C$)-L):GOTO557
558 NEXT L
560 REM
570 REM     NOW USING THE KEYWORD NUMBER (K) GET REPLY
580 REM
590 RESTORE:FOR X= 1 TO N1+N2:READ Z$:NEXT X
600 FORX=1TOR(K):READF$:NEXT X:REM  READ RIGHT REPLY
610 R(K)=R(K)+1: IFR(K)>N(K) THEN R(K)=S(K)
620 IF RIGHT$(F$,1)<>"*" THEN PRINT F$:P$=I$:GOTO 170
630 PRINT LEFT$(F$,LEN(F$)-1);C$
640 P$=I$:GOTO 170
1000 REM
1010 REM     -----PROGRAM DATA FOLLOWS-----
1020 REM
1030 REM     KEYWORDS
1040 REM
1050 DATA "can you","can i","you are","youre","i dont","i feel"
1060 DATA "why dont you","why cant i","are you","i cant","i am","im "
1070 DATA "you ","i want","what","how","who","where","when","why"
1080 DATA "name","cause","sorry","dream","hello","hi ","maybe"
1090 DATA " no","your","always","think","alike","yes","friend"
1100 DATA "computer","nokeyfound"
1200 REM
1210 REM     STRING DATA FOR CONJUGATION
1220 REM
1230 DATA " are "," am ", "were ","was "," you "," i ","your ","my "
1235 DATA " ive "," youve "," im "," youre "
1240 DATA " me ", " !you "
1300 REM
1310 REM     REPLIES
1320 REM
1330 DATA "Don't you believe that I can*"
1340 DATA "Perhaps you would like to be able to*"
1350 DATA "You want me to be able to*"
1360 DATA "Perhaps you don't want to*"
1365 DATA "Do you want to be able to*"
1370 DATA "Do you want to be able to*"
1380 DATA "Does it please you to believe I am*"
1390 DATA "Perhaps you would like to be*"
1400 DATA "Do you sometimes wish you were*"
1410 DATA "Don't you really*"
1420 DATA "Why don't you*"
1430 DATA "Do you wish to be able to*"
1440 DATA "Does that trouble you?"
1450 DATA "Tell me more about such feelings."
1460 DATA "Do you often feel*"
1470 DATA "Do you enjoy feeling*"
1480 DATA "Do you really believe I don't*"
1490 DATA "Perhaps in good time I will*"
1500 DATA "Do you want me to*"
1510 DATA "Do you think you should be able to*"
1520 DATA "Why can't you*"
1530 DATA "Why are you interested in whether or not I am*"
1540 DATA "Would you prefer if I were not*"
1550 DATA "Perhaps in your fantasies I am*"
1560 DATA "How do you know you can't*"
1570 DATA "Have you tried?"
1580 DATA "Perhaps you can now*"
1590 DATA "Did you come to me because you are*"
1600 DATA "How long have you been*"
1610 DATA "Do you believe it is normal to be*"
1620 DATA "Do you enjoy being*"
1630 DATA "We were discussing you-- not me."
1640 DATA "Oh, I*"
1650 DATA "You're not really talking about me, are you?"
1660 DATA "What would it mean to you if I got*"
1670 DATA "Why do you want*"
1680 DATA "Suppose you soon got*"
1690 DATA "What if you never got*"
1700 DATA "I sometimes also want*"
1710 DATA "Why do you ask?"
1720 DATA "Does that question intertest you?"
1730 DATA "What answer would please you the most?"
1740 DATA "What do you think?"
1750 DATA "Are such questions on your mind often?"
1760 DATA "What is it that you really want to know?"
1770 DATA "Have you asked anyone else?"
1780 DATA "Have you asked such questions before?"
1790 DATA "What else comes to mind when you ask that?"
1800 DATA "Names don't interest me."
1810 DATA "I don't car about names-- please go on."
1820 DATA "Is that the real reason?"
1830 DATA "Don't any other reasons come to mind?"
1840 DATA "Does that reason explain anything else?"
1850 DATA "What other reasons might there be?"
1860 DATA "Please don't apologize!"
1870 DATA "Apologies are not necessary."
1880 DATA "What feelings do you have when you apologise?"
1890 DATA "Don't be so defensive!"
1900 DATA "What does that dream suggest to you?"
1910 DATA "Do you dream often?"
1920 DATA "What persons appear in your dreams?"
1930 DATA "Are you disturbed by your dreams?"
1940 DATA "How do you do ... Please state your problem."
1950 DATA "You don't seem quite certain."
1960 DATA "Why the uncertain tone?"
1970 DATA "Can't you be more positive?"
1980 DATA "You aren't sure?"
1990 DATA "Don't you know?"
2000 DATA "Are you saying 'no' just to be negative?"
2010 DATA "You are being a bit negative."
2020 DATA "Why not?"
2030 DATA "Are you sure?"
2040 DATA "Why no?"
2050 DATA "Are you concerned about my*"
2060 DATA "What about your own*"
2070 DATA "Can you think of a specific example?"
2080 DATA "When?"
2090 DATA "What are you thinking of?"
2100 DATA "Really, always?"
2110 DATA "Do you really think so?"
2120 DATA "But you are not sure you*"
2130 DATA "Do you doubt you*"
2140 DATA "In what way?"
2150 DATA "What resemblance do you see?"
2160 DATA "What does the similarity suggest to you?"
2170 DATA "What other connections do you see?"
2180 DATA "Could there really be some connection?"
2190 DATA "How?"
2200 DATA "You seem quite positive."
2210 DATA "Are you sure?"
2220 DATA "I see."
2230 DATA "I understand."
2240 DATA "Why do you bring up the topic of friends?"
2250 DATA "Do your friends worry you?"
2260 DATA "Do your friends pick on you?"
2270 DATA "Are you sure you have any friends?"
2280 DATA "Do you impose on your friends?"
2290 DATA "Perhaps your love for friends worries you?"
2300 DATA "Do computers worry you?"
2310 DATA "Are you talking about me in particular?"
2320 DATA "Are you frightened by machines?"
2330 DATA "Why do you mention computers?"
2340 DATA "What do you think machines have to do with your problem?"
2350 DATA "Don't you think computers can help people?"
2360 DATA "What is it about machines that worries you?"
2370 DATA "Say, do you have any psychological problems?"
2380 DATA "What does that suggest to you?"
2390 DATA "I see."
2400 DATA "I'm not sure I understand you fully."
2410 DATA "Come, come. Elucidate your thoughts."
2420 DATA "Can you elaborate on that?"
2430 DATA "That is quite interesting."
2500 REM
2510 REM     DATA FOR FINDING RIGHT REPLIES
2520 REM
2530 DATA 1,3,4,2,6,4,6,4,10,4,14,3,17,3,20,2,22,3,25,3
2540 DATA 28,4,28,4,32,3,35,5,40,9,40,9,40,9,40,9,40,9,40,9
2550 DATA 49,2,51,4,55,4,59,4,63,1,63,1,64,5,69,5,74,2,76,4
2560 DATA 80,3,83,7,90,3,93,6,99,7,106,6

# END
