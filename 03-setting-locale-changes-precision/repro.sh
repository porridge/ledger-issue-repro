#!/bin/bash
for arg in never at_start after_query
do
	./repro.py $arg > out-${arg}.txt
	cat out-${arg}.txt
done
