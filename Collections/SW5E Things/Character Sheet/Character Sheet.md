# v2.1
## Top Information
### Main Header A2:R5
```scala
=if(C174="",if(isnumber(find("Han",C6)),image("https://i.imgur.com/T5OD9a5.png",2),if(and(AV16<>"",countif(AQ155:AQ180,AV16)),image(vlookup(AV16,AQ155:AS180,2,false),2),image(AR156,2))),image(vlookup(C174,AQ155:AS180,2,false),2))
```
### Theming image S3
```scala
=if(C174="Magic",IMAGE("http://i.imgur.com/2jwsXWa.png",2),"")
```
### Help text line 1T2:AM2
```scala
=if(and(name="",classAndLevel="",race="",level="",C16=0,C21=0,C26=0,C31=0,C36=0,C41=0),"Click [File] then [Make a copy...] to use the sheet for yourself.",if(and(sum(AT6:AT15)<>level,classAndLevel<>""),"Total class levels must equal character level",""))
```
### Help text line 2 T3:AM3
```scala
=if(and(name="",classAndLevel="",race="",level="",C16=0,C21=0,C26=0,C31=0,C36=0,C41=0),"Check [?] for help.  And read all the notes!",if(and(sum(AT6:AT15)<>level,classAndLevel<>""),"If you are using a homebrew class, enter its details on the Class Info page.",""))																			
```
### Name top border S4:AN4
```scala
=IMAGE("http://i.imgur.com/OlUFGxq.png",2)
```
### Name right side border A04:A08
```scala
=IMAGE("http://i.imgur.com/nWCUyCa.png",2)
```
### Level top border AL5:AM5
```scala
=if(AL6="",IMAGE(Additional!AX9,2),if(AL6<5,IMAGE(Additional!AX10,2),if(AL6<11,IMAGE(Additional!AX11,2),if(AL6<17,IMAGE(Additional!AX12,2),IMAGE(Additional!AX13,2)))))
```
### Level left border AK5:AK8
```scala
=if(AL6="",IMAGE(Additional!AV9,2),if(AL6<5,IMAGE(Additional!AV10,2),if(AL6<11,IMAGE(Additional!AV11,2),if(AL6<17,IMAGE(Additional!AV12,2),IMAGE(Additional!AV13,2)))))
```
### Level right border AN5:AN8
```scala
=if(AL6="",IMAGE(Additional!AW9,2),if(AL6<5,IMAGE(Additional!AW10,2),if(AL6<11,IMAGE(Additional!AW11,2),if(AL6<17,IMAGE(Additional!AW12,2),IMAGE(Additional!AW13,2)))))
```
### AL6:AM7
```scala
=if(AE7<>"",if(AE7<300,1,if(AE7<900,2,if(AE7<2700,3,if(AE7<6500,4,if(AE7<14000,5,if(AE7<23000,6,if(AE7<34000,7,if(AE7<48000,8,if(AE7<64000,9,if(AE7<85000,10,if(AE7<100000,11,if(AE7<120000,12,if(AE7<140000,13,if(AE7<165000,14,if(AE7<195000,15,if(AE7<225000,16,if(AE7<265000,17,if(AE7<305000,18,if(AE7<355000,19,20))))))))))))))))))),"")
```
### Level A6:A7
```scala
=IMAGE("https://imgur.com/ABQY3Ko.png",2)
```
### Character name left border B6:B7
```scala
=IMAGE("https://imgur.com/mswZvmb.png",2)
```
### Next Level AH7:AJ7
```scala
=if(AE7<>"",choose(AL6,300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000,0),"")
```
### Character name bottom border A8:R9
```scala
=if(C174="",if(isnumber(find("Han",C6)),image("https://i.imgur.com/zOBptnJ.png",2),if( and(AV16<>"",countif(AQ155:AQ180,AV16)),image("https://i.imgur.com/zOBptnJ.png",2),image(AS156,2))),image(vlookup(C174,AQ155:AS180,3,false),2))
```
### Race label T8:AD8
```scala
=if(and(T7<>"",AQ5=""),"To use a custom race, add it on the 'Race Info' tab.","RACE")
```
### Header bottom oborder S9:AN9
```scala
=IMAGE("http://i.imgur.com/6avJSbK.png",2)
```
## Stats
### Stats top border B10:E10
```scala
=IMAGE("http://i.imgur.com/u3YeDks.png",2)
```
### Stats right border E11:E41
```scala
=IMAGE("http://i.imgur.com/u9a6TBA.png",2)
```

### Strength mod C13:D14
```scala
=if(C15="-","-",INT((C15-10)/2))
```
### Strength score C15:D15
```scala
=if(C16,min(30,max(
iferror(int(trim(right(regexextract(Additional!$AR$79,lower(C12)&"[a-z]+? score is [0-9]+"),2))),0),
iferror(int(trim(right(regexextract(Additional!$AR$79,lower(C12)&"[a-z]+? score changes to [0-9]+"),2))),0),
min(iferror(int(trim(right(regexextract(Additional!$AR$79,lower(C12)&"[a-z]+? [a-z ]+maximum of [0-9]+?"),2))),20),
C16+
iferror(if(find(regexextract($AR$5,lower(C12)&" \+[0-9]"),$AR$5)<iferror(find("choose",lower($AR$5)),len($AR$5)),int(right(regexextract($AR$5,lower(C12)&" \+[0-9]"),1)),0),0)-
iferror(if(find(regexextract($AR$5,lower(C12)&" \-[0-9]"),$AR$5)<iferror(find("choose",lower($AR$5)),len($AR$5)),int(right(regexextract($AR$5,lower(C12)&" \-[0-9]"),1)),0),0)
+D16))
+sum(arrayformula(int(iferror(trim(right(regexextract(lower(filter({BA$32:BA$56;Additional!$BA$3:$BA$24},regexmatch(lower({BA$32:BA$56;Additional!$BA$3:$BA$24}),lower(C12)&"[a-z]+? score increases by [0-9]+"))),lower(C12)&"[a-z]+? score increases by [0-9]+"),2)),0))))),"-")
```
### Dexterity mod C18:D19
```scala
=if(C20="-","-",INT((C20-10)/2))
```
### Dexterity score C20:D20
```scala
=if(C21,min(30,max(
iferror(int(trim(right(regexextract(Additional!$AR$79,lower(C17)&"[a-z]+? score is [0-9]+"),2))),0),
iferror(int(trim(right(regexextract(Additional!$AR$79,lower(C17)&"[a-z]+? score changes to [0-9]+"),2))),0),
min(iferror(int(trim(right(regexextract(Additional!$AR$79,lower(C17)&"[a-z]+? [a-z ]+maximum of [0-9]+?"),2))),20),
C21+
iferror(if(find(regexextract($AR$5,lower(C17)&" \+[0-9]"),$AR$5)<iferror(find("choose",lower($AR$5)),len($AR$5)),int(right(regexextract($AR$5,lower(C17)&" \+[0-9]"),1)),0),0)-
iferror(if(find(regexextract($AR$5,lower(C17)&" \-[0-9]"),$AR$5)<iferror(find("choose",lower($AR$5)),len($AR$5)),int(right(regexextract($AR$5,lower(C17)&" \-[0-9]"),1)),0),0)
+D21))
+sum(arrayformula(int(iferror(trim(right(regexextract(lower(filter({BA$32:BA$56;Additional!$BA$3:$BA$24},regexmatch(lower({BA$32:BA$56;Additional!$BA$3:$BA$24}),lower(C17)&"[a-z]+? score increases by [0-9]+"))),lower(C17)&"[a-z]+? score increases by [0-9]+"),2)),0))))),"-")
```
## Saves
## Skills
## Player Information
