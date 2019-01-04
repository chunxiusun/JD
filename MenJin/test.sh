#!/bin/bash

for ((i=1;i<12;i++))
do
   nohup python -u algoTest_$i.py > nohup_$i.out &
done
