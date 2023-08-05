#!/usr/bin/python

#       Sgourakis Lab
#   Author: Santrupti Nerli
#   Date: June 20, 2018
#   Email: snerli@ucsc.edu
#

'''

A dictionary of supported chaperone sequences

'''
# import required libraries
from collections import defaultdict

chaperone_sequences = defaultdict(dict)
chaperone_sequences['tapasin']='MKSLSLLLAVALGLATAVSAGPAVIECWFVEDASGKGLAKRPGALLLRQGPGEPPPRPDLDPELYLSVHDPAGALQAAFRRYPRGAPAPHCEMSRFVPLPASAKWASGLTPAQNCPRALDGAWLMVSISSPVLSLSSLLRPQPEPQQEPVLITMATVVLTVLTHTPAPRVRLGQDALLDLSFAYMPPTSEAASSLAPGPPPFGLEWRRQHLGKGHLLLAATPGLNGQMPAAQEGAVAFAAWDDDEPWGPWTGNGTFWLPRVQPFQEGTYLATIHLPYLQGQVTLELAVYKPPKVSLMPATLARAAPGEAPPELLCLVSHFYPSGGLEVEWELRGGPGGRSQKAEGQRWLSALRHHSDGSVSLSGHLQPPPVTTEQHGARYACRIHHPSLPASGRSAEVTLEVAGLSGPSLEDSVGLFLSAFLLLGLFKALGWAAVYLSTCKDSKKKAE'
chaperone_sequences['tapbpr']='MGTQEGWCLLLCLALSGAAETKPHPAEGQWRAVDVVLDCFLAKDGAHRGALASSEDRARASLVLKQVPVLDDGSLEDFTDFQGGTLAQDDPPIIFEASVDLVQIPQAEALLHADCSGKEVTCEISRYFLQMTETTVKTAAWFMANMQVSGGGPSISLVMKTPRVTKNEALWHPTLNLPLSPQGTVRTAVEFQVMTQTQSLSFLLGSSASLDCGFSMAPGLDLISVEWRLQHKGRGQLVYSWTAGQGQAVRKGATLEPAQLGMARDASLTLPGLTIQDEGTYICQITTSLYRAQQIIQLNIQASPKVRLSLANEALLPTLICDIAGYYPLDVVVTWTREELGGSPAQVSGASFSSLRQSVAGTYSISSSLTAEPGSAGATYTCQVTHISLEEPLGASTQVVPPERRTALGVIFASSLFLLALMFLGLQRRQAPTGLGLLQAERWETTSCADTQSSHLHEDRTARVSQPS'
chaperone_sequences['none']=''
