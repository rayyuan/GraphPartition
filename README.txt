These are the instructions for how to run the code.

    solver_rewrite.py #threads #thread_num

for an example, if I am running on on 1 thread, then I will run as follows:

    python solver_rewrite.py 1 0

if I am running on 4 threads, then I will run as follows:

    python solver_rewrite.py 4 0
    python solver_rewrite.py 4 1
    python solver_rewrite.py 4 2
    python solver_rewrite.py 4 3

There is also a start.rewrite_32.sh that will run solver_rewrite.py on 32 threads

    in a linux OS, run by: ./start.rewrie_32.sh (you may have to run chmod +x start.rewrite_32.sh first to make it executable)

We also included tools for combining the best of 2 solution sets (this will combine the best in output1 and output2 and save them in output3):

    python output_combiner.py output1 output2 output3