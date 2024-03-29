# Add papers below in chronological order :)

printf "HELLO! WELCOME TO METRINOME. PRESS THE CORRESPONDING NUMBER TO SEE THE BENCHMARKS FROM THAT PAPER.\n\
   1) ISSTA 2024 PAPER\n\
   2) ICSE 2024 POSTER\n\
   3) ICSE 2021 PAPER\n"

# Add valid papers to this list as we expand
paper_dict='{
   "0": "/app/code/chooseFile.txt",
   "1": "/app/code/tests/cFiles/C-master/CmasterFiles.txt",
   "2": "/app/code/experiments/function_calls/benchmark/benchmarkFiles.txt",
   "3": "/app/code/experiments/icse_experiment/files/files.txt"
   }'

while read paper_num; do
   # check if input in the list
   # if ([[ ${paper_dict[@]} =~ (^|[[:space:]])"$paper_num"($|[[:space:]]) ]]); then
   if [[ $paper_dict == *"$paper_num"* ]]; then
      break
   else
      echo "Not a valid paper! Try Again :)"
      continue
   fi
done

python3 /app/code/experiments/function_calls/tests/test_getrgf.py $paper_num "$paper_dict"
# must run this in order for mergeTestResult to work

# python3 /app/code/experiments/function_calls/tests/test_fcapc.py $paper_num

# python3 /app/code/experiments/function_calls/tests/test_rapc.py $paper_num

# python3 /app/code/experiments/function_calls/tests/test_npath.py $paper_num

# python3 /app/code/experiments/function_calls/tests/mergeData.py