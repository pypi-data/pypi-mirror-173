# HAMMURABI
# By David H. Ahl.
# From David H. Ahl & Steve North, BASIC Computer Games, Workman, 1978.

# A game of resource management. An awful lot hinges on random crop yields.

# Changes:
# - It was a tough call, but this version restores the long-lost m to Hammurabi.
# - Formatting of some printed output.
# - Appended authors and history to title.
# - Added line 120, to hold the history on-screen.
# - Changed < to <= on line 455 (10 acres per person).

10 PRINT TAB(24);"HAMMURABI"
20 PRINT TAB(20);"Creative Computing"
25 PRINT TAB(18);"Morristown, New Jersey"
30 PRINT
40 PRINT TAB(21);"by David H. Ahl"
45 PRINT TAB(7);"after King of Sumeria by Doug Dyment (1968)"
50 PRINT TAB(9);"itself inspired by The Sumerian Game by"
55 PRINT TAB(8);"Mabel Addis and William McKay (1964-1966)"
60 PRINT TAB(27);"1971"
70 PRINT:PRINT:PRINT
80 PRINT "Try your hand at governing ancient Sumeria"
90 PRINT "for a ten-year term of office.":PRINT
95 D1=0: P1=0
100 Z=0: P=95:S=2800: H=3000: E=H-S
110 Y=3: A=H/Y: I=5: Q=1
120 INPUT"[press enter when ready]",
210 D=0
215 PRINT:PRINT:PRINT "Hammurabi:  I beg to report to you.": Z=Z+1
217 PRINT "In year";STR$(Z);",";D;"people starved,";I;"came to the city."
218 P=P+I
227 IF Q>0 THEN 230
228 P=INT(P/2)
229 PRINT "A horrible plague struck!  Half the people died."
230 PRINT "The population is now";STR$(P);"."
232 PRINT "The city now owns";A;"acres."
235 PRINT "You harvested";Y;"bushels per acre."
250 PRINT "The rats ate";E;"bushels."
260 PRINT "You now have";S;"bushels in store.": PRINT
270 IF Z=11 THEN 860
310 C=INT(10*RND(1)): Y=C+17
312 PRINT "Land is trading at";Y;"bushels per acre."
320 PRINT "How many acres do you wish to buy";
321 INPUT Q: IF Q<0 THEN 850
322 IF Y*Q<=S THEN 330
323 GOSUB 710
324 GOTO 320
330 IF Q=0 THEN 340
331 A=A+Q: S=S-Y*Q: C=0
334 GOTO 400
340 PRINT "How many acres do you wish to sell";
341 INPUT Q: IF Q<0 THEN 850
342 IF Q<A THEN 350
343 GOSUB 720
344 GOTO 340
350 A=A-Q: S=S+Y*Q: C=0
400 PRINT
410 PRINT "How many bushels do you wish to feed your people";
411 INPUT Q
412 IF Q<0 THEN 850
418 REM *** TRYING TO USE MORE GRAIN THAN IS IN SILOS?
420 IF Q<=S THEN 430
421 GOSUB 710
422 GOTO 410
430 S=S-Q: C=1: PRINT
440 PRINT "How many acres do you wish to plant with seed";
441 INPUT D: IF D=0 THEN 511
442 IF D<0 THEN 850
444 REM *** TRYING TO PLANT MORE ACRES THAN YOU OWN?
445 IF D<=A THEN 450
446 GOSUB 720
447 GOTO 440
449 REM *** ENOUGH GRAIN FOR SEED?
450 IF INT(D/2)<=S THEN 455
452 GOSUB 710
453 GOTO 440
454 REM *** ENOUGH PEOPLE TO TEND THE CROPS?
455 IF D<=10*P THEN 510
460 PRINT "But you have only";P;"people to tend the fields!  Now then,"
470 GOTO 440
510 S=S-INT(D/2)
511 GOSUB 800
512 REM *** A BOUNTIFUL HARVEST!
515 Y=C: H=D*Y: E=0
521 GOSUB 800
522 IF INT(C/2)<>C/2 THEN 530
523 REM *** RATS ARE RUNNING WILD!!
525 E=INT(S/C)
530 S=S-E+H
531 GOSUB 800
532 REM *** LET'S HAVE SOME BABIES
533 I=INT(C*(20*A+S)/P/100+1)
539 REM *** HOW MANY PEOPLE HAD FULL TUMMIES?
540 C=INT(Q/20)
541 REM *** HORRORS, A 15% CHANCE OF PLAGUE
542 Q=INT(10*(2*RND(1)-.3))
550 IF P<C THEN 210
551 REM *** STARVE ENOUGH FOR IMPEACHMENT?
552 D=P-C: IF D>.45*P THEN 560
553 P1=((Z-1)*P1+D*100/P)/Z
555 P=C: D1=D1+D: GOTO 215
560 PRINT: PRINT "You starved";D;"people in one year!!!"
565 PRINT "Due to this extreme mismanagement you have not only"
566 PRINT "been impeached and thrown out of office, but you have"
567 PRINT "also been declared national fink!!!!": GOTO 990
710 PRINT "Hammurabi:  Think again.  You have only"
711 PRINT MID$(STR$(S),2);" bushels of grain.  Now then,"
712 RETURN
720 PRINT "Hammurabi:  Think again.  You own only";A;"acres.  Now then,"
730 RETURN
800 C=INT(RND(1)*5)+1
801 RETURN
850 PRINT: PRINT "Hammurabi:  I cannot do what you wish."
855 PRINT "Get yourself another steward!!!!!"
857 GOTO 990
860 PRINT "In your 10-year term of office,";P1;"percent of the"
862 PRINT "population starved per year on the average, i.e. a total of"
865 PRINT MID$(STR$(D1),2);" people died!!": L=A/P
870 PRINT "You started with 10 acres per person and ended with"
875 PRINT MID$(STR$(L),2);" acres per person.": PRINT
880 IF P1>33 THEN 565
885 IF L<7 THEN 565
890 IF P1>10 THEN 940
892 IF L<9 THEN 940
895 IF P1>3 THEN 960
896 IF L<10 THEN 960
900 PRINT "A fantastic performance!!!  Charlemagne, Disraeli, and"
905 PRINT "Jefferson combined could not have done better!":GOTO 990
940 PRINT "Your heavy-handed performance smacks of Nero and Ivan IV."
945 PRINT "The people (remaining) find you an unpleasant ruler, and,"
950 PRINT "frankly, hate your guts!!":GOTO 990
960 PRINT "Your performance could have been somewhat better, but"
965 PRINT "really wasn't too bad at all. ";INT(P*.8*RND(1));"people"
970 PRINT "would dearly like to see you assassinated, but we all have our"
975 PRINT "trivial problems."
990 PRINT: FOR N=1 TO 10: PRINT CHR$(7);: NEXT N
995 PRINT "So long for now.": PRINT
999 END

# END
