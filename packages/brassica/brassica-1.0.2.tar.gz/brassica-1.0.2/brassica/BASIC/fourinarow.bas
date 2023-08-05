# FOUR IN A ROW
# By James L. Murphy.
# From David H. Ahl & Steve North, More BASIC Computer Games, Workman, 1980.

# An implementation of Howard Wexler and Ned Strongin's 'Connect 4' board game
# of 1974. The computer's artificial intelligence is pre-set; it does not learn.

# Changes:
# - Formatting of some printed output.
# - Appended author and year to title.
# - Modifed lines 180 and 310 (and removed lines 190 and 200), to allow 'Y',
#   'N', and blank responses, in addition to 'yes' and 'no' (only).
# - Added the DELAY 0 on line 420, to flush the terminal after each move.
# - Added lines 1580 onward, to allow rematches.

10 PRINT TAB(22);"FOUR IN A ROW"
20 PRINT TAB(20);"Creative Computing"
30 PRINT TAB(18);"Morristown, New Jersey"
40 PRINT
50 PRINT TAB(20);"by James L. Murphy"
60 PRINT TAB(3);"board game by Howard Wexler and Ned Strongin (1974)"
70 PRINT TAB(26);"c1978"
80 PRINT: PRINT: PRINT
100 DIM B$(8,8),L(8),S(4),F(4)
110 DIM V(16),N(4)
130 DATA 1,100,500,1E20,1,800,4000,1E20
140 DATA 1,75,900,1E18,1,450,3000,1E18
150 FOR Z1=1 TO 16:READ V(Z1):NEXT Z1
160 PRINT"The game of Four In A Row."
170 INPUT"Do you want instructions (y/n)";A$
180 IF LEFT$(A$,1)="N" THEN 270
# 190 IF A$="yes" THEN 210
# 200 PRINT"Yes or No":GOTO 170
210 PRINT"The game consists of stacking X's"
220 PRINT"and O's (the computer has O) until"
230 PRINT"one of the players gets four in a"
240 PRINT"row vertically, horizontally, or "
250 PRINT"diagonally."
260 PRINT:PRINT
270 X$="X":O$="O"
280 FOR I=1 TO 8:FOR J=1 TO 8:B$(I,J)="-":NEXT J:NEXT I
290 FOR Z1=1 TO 8:L(Z1)=0:NEXT Z1
300 INPUT"Do you want to go first";A$:PRINT
310 IF LEFT$(A$,1)="N" THEN 610
320 GOSUB 340
330 GOTO 450
340 FOR I=8 TO 1 STEP -1
350 FOR J=1 TO 8
360 PRINT"  ";B$(I,J);
370 NEXT J
380 PRINT
390 NEXT I
400 PRINT" ";
410 FOR I=1 TO 8:PRINT I;:NEXT I
420 PRINT:PRINT:DELAY 0
430 RETURN
440 PRINT"Illegal move. Try again."
450 INPUT"A column between 1 and 8";M
460 M=INT(M)
470 IF M<1 OR M>8 THEN 440
480 L=L(M)
490 IF L>7 THEN 440
500 L(M)=L+1:L=L+1
510 B$(L,M)=X$
520 PRINT
530 GOSUB 340
540 P$=X$
550 GOSUB 1240
560 FOR Z=1 TO 4
570 IF S(Z)<4 THEN 600
580 PRINT"Y O U   W I N !!!"
590 GOTO 1580
600 NEXT Z
610 M9=0:V1=0
620 N1=1
630 FOR M4=1 TO 8
640 L=L(M4)+1
650 IF L>8 THEN 1080
660 V=1
670 P$=O$:W=0
680 M=M4
690 GOSUB 1240
700 FOR Z1=1 TO 4:N(Z1)=0:NEXT Z1
710 FOR Z=1 TO 4
720 S=S(Z)
730 IF S-W>3 THEN 1130
740 T=S+F(Z)
750 IF T<4 THEN 780
760 V=V+4
770 N(S)=N(S)+1
780 NEXT Z
790 FOR I = 1 TO 4
800 N=N(I)-1
810 IF N=-1 THEN 840
820 I1=8*W+4*SGN(N)+I
830 V=V + V(I1) + N*V(8*W+I)
840 NEXT I
850 IF W=1 THEN 880
860 W=1:P$=X$
870 GOTO 690
880 L=L+1
920 IF L>8 THEN 1020
930 GOSUB 1240
940 FOR Z=1 TO 4
950 IF S(Z)>3 THEN V=2
960 NEXT Z
1020 IF V<V1 THEN 1080
1030 IF V>V1 THEN N1=1: GOTO 1060
1040 N1=N1 + 1
1050 IF RND(1)>1/N1 THEN 1080
1060 V1 = V
1070 M9=M4
1080 NEXT M4
1090 IF M9<>0 THEN 1120
1100 PRINT "T I E   G A M E ..."
1110 GOTO 1580
1120 M=M9
1130 PRINT "Computer picks column";STR$(M);":":PRINT
1140 L=L(M)+1:L(M)=L(M)+1
1150 B$(L,M)=O$
1160 P$=O$:GOSUB 340
1170 GOSUB 1240
1180 FOR Z = 1 TO 4
1190 IF S(Z)<4 THEN 1220
1200 PRINT"C O M P U T E R   W I N S !!!"
1210 GOTO 1580
1220 NEXT Z
1230 GOTO 450
1240 Q$=X$
1250 IF P$=X$ THEN Q$=O$
1260 D2=1:D1=0
1270 Z=0
1280 GOSUB 1360
1290 D1=1:D2=1
1300 GOSUB 1360
1310 D2=0:D1=1
1320 GOSUB 1360
1330 D2=-1:D1=1
1340 GOSUB 1360
1350 RETURN
1360 D=1:S=1
1370 T=0
1380 Z=Z+1
1390 C=0
1400 FOR K=1 TO 3
1410 M5=M+K*D1:L1=L+K*D2
1420 IF M5<1 OR L1<1 OR M5>8 OR L1>8 THEN 1510
1430 B$=B$(L1,M5)
1440 IF C=0 THEN 1480
1450 IF B$=Q$ THEN K=3: GOTO 1510
1460 T = T+1
1470 GOTO 1510
1480 IF B$=P$ THEN S=S+1:GOTO 1510
1490 C=1
1500 GOTO 1450
1510 NEXT K
1520 IF D=0 THEN 1550
1530 D=0:D1=-D1:D2=-D2
1540 GOTO 1390
1550 S(Z)=S
1560 F(Z)=T
1570 RETURN
1580 PRINT
1590 INPUT"Play again";A$
1600 IF LEFT$(A$,1)="N" THEN 1630
1610 FOR Z=1 TO 4:S(Z)=0:F(Z)=0:NEXT Z
1612 REM It matters that Z is the iterator. If we arrive at 1580 from 590 or
1613 REM 1210, then we're inside a loop over Z (560 or 1180). The Z loop at
1614 REM 1610 ends that prior loop. Otherwise, if the user elects not to have
1615 REM the first move at 300, the M4 loop at 630 will be nested under the Z
1616 REM loop, and hence terminated by the new Z loop at 710. This results in
1617 REM next without for at 1080.
1620 GOTO 280
1630 END

# END
