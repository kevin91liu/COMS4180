#Kevin Liu

Programming assignment 2.

##Instructions to execute

- Run the ngram program from the command line with:

``python problem1.py <n> <s> <file name> <output file>``, where ``<n>`` is the length of the ngrams (n=1, 2, 3), ``<s>`` is the length of the slide (s <= n), ``<file name>`` is the name of the file to analyze, and ``<output file>`` is the output filename

Example:
``python problem1.py 3 1 prog1 prog1.output``

- For problem 2b, run the program with sudo, because scapy requires root privileges in order to send packets:

``sudo python problem2.py``

- For problem 2c, run the program with:

``sudo python problem2c.py <source port> <destination port>``, where ``<source_port>`` and ``<destination_port>`` are both integers.

Example:
``sudo python problem2c.py 2099 2552``

##Output

The program outputs (both to the console, and to the output file) the top-20 ngrams, the unique number of ngrams, and the time it took to execute. For the largest of the files, prog1, running ``python problem1.py 3 1 prog1 prog1.output`` takes 0.18 seconds. 