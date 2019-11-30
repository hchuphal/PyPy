#!/usr/bin/env python
#align.py : Post Processing of TT Logs

import re
import sys
import os

#Alignment of pattern in input dump
def InputAlignment(Filename):
        for file in os.listdir('./'):
                if Filename==file:
                        print "Input File for Processings %s "% Filename
                        os.rename(file, 'dump.txt')
        os.system("sed -e 's/:H-PID /\ H-PID:/g'  -e 's/:rnti /rnti:/g'  -e 's/:ndi/\ ndi/g'  -e 's/:cce_index /\ cce_index:/g' -e 's/:aggr_level /\ aggr_level:/g' -e 's/:TB0/\ TB0/g'  -e 's/lc_id /lc_id:/g' -e 's/:size /\ size:/g'  -e 's/:mcs /\ mcs:/g'  -e 's/:TB1/\ TB1/g' -e 's/:rb_coding /\ rb_coding:/g' -e 's/rb_coding /\ rb_coding:/g'  -e 's/:ce_bitmap /\ ce_bitmap:/g' -e 's/:wb_cqi/\ wb_cqi/g' -e 's/:ri /\ ri:/g' -e 's/:WMCS /\ WMCS:/g' -e 's/:HarqOff /\ HarqOff:/g' -e 's/cce_index /cce_index:/g' -e 's/aggr_level /aggr_level:/g' -e 's/rb_start /rb_start:/g' -e 's/num_rb /num_rb:/g' -e 's/mcs /mcs:/g' -e 's/ndi /ndi:/g' -e 's/dmrs_cs2 /dmrs_cs2:/g' -e 's/tpc /tpc:/g'  -e 's/: /\ :/g' -e 's/SNR /SNR:/g'  -e 's/target_snr /target_snr:/g'  -e 's/current_tx_nb /current_tx_nb:/g'  -e 's/max_num_tx /max_num_tx:/g'  -e 's/SfCnt /SfCnt:/g'  -e 's/RNTI /RNTI:/g'  -e 's/LCID /LCID:/g'  -e 's/QCI /QCI:/g'  -e 's/QCI /QCI:/g'  -e 's/Wt /Wt:/g'  -e 's/M /M:/g'  -e 's/TP /TP:/g'  -e 's/CurAlcn /CurAlcn:/g'  -e 's/PRBsAvlbl /PRBsAvlbl:/g'  -e 's/TotalPendingData /TotalPendingData:/g'  -e 's/lcg_id /lcg_id:/g'  -e 's/in_flight /in_flight:/g'  -e 's/received /received:/g'  -e 's/buffer_size /buffer_size:/g'  -e 's/lcg /lcg:/g'  -e 's/metric /metric:/g'  -e 's/W /W:/g'  -e 's/\#\*\#\* /DL_LC_STATS: /g'  -e 's/\[get_ulsch_list:/get_ulsch_list_ulmetric: /g' -e 's/rnti /rnti:/g' -e 's/:tpc /\ tpc/g'  dump.txt >>InputDump.txt")
        print "\n Logs Aligned for Post Processing \n"

if __name__ == '__main__':
        print "\n **** Aligning TTool Logs ******\n"
