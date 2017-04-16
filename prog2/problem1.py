#author kevin liu
#programming assignment 2
import sys
import time
import binascii

time1 = time.time()

if(len(sys.argv) != 5):
  print "Invalid number of arguments. Invoke program using: python problem1.py <n> <s> <file name> <output file>, where <n> is the length of the ngrams (n=1, 2, 3), <s> is the length of the slide (s <= n), <file name> is the name of the file to analyze, and <output file> is the output filename"
  exit()

#get the arguments. i assume here that proper arguments will be given, since the instructors said on courseworks that we
#don't have to handle bad inputs
n = int(sys.argv[1])
s = int(sys.argv[2])
filename = sys.argv[3]
output_filename = sys.argv[4]

#open the input and output files
try:
  f_input = open(filename, 'rb')
  f_output = open(output_filename, 'wb')
except IOError as e:
  print e
  sys.exit()

#this is where i record ngram counts
ngrams = {}

one_byte_ago = None
two_bytes_ago = None


current_byte = f_input.read(1)
while current_byte != '':
  if n==1 or (n==2 and one_byte_ago == None) or (n==3 and two_bytes_ago == None and one_byte_ago == None):
    if not current_byte in ngrams:
      ngrams[current_byte] = 0
    ngrams[current_byte] += 1
  elif n==2 or (n==3 and two_bytes_ago == None):
    if not (one_byte_ago+current_byte) in ngrams:
      ngrams[(one_byte_ago+current_byte)] = 0
    ngrams[(one_byte_ago + current_byte)] += 1
  elif n==3:
    if not (two_bytes_ago+one_byte_ago+current_byte) in ngrams:
      ngrams[two_bytes_ago+one_byte_ago+current_byte] = 0
    ngrams[two_bytes_ago+one_byte_ago+current_byte] += 1

  #get the next ngram
  for i in range(0, s):
    two_bytes_ago = one_byte_ago
    one_byte_ago = current_byte
    current_byte = f_input.read(1)


f_input.close()


def tuple_comparison(x, y):
  if x[1] > y[1]:
    return 1
  if x[1] < y[1]:
    return -1
  if x[0] < y[0]:
    return 1
  if x[0] > y[0]:
    return -1
  return 0
#now, iterate over the ngrams dictionary
list_ngrams_tuples = ngrams.items()
list_ngrams_tuples_sorted = sorted(list_ngrams_tuples, cmp = tuple_comparison, key = lambda x: (x[0], x[1]), reverse=True)

top_20_ngrams = list_ngrams_tuples_sorted[0:20]
for i in range(0, len(top_20_ngrams)):
  output = binascii.hexlify(top_20_ngrams[i][0]) + " " + str(top_20_ngrams[i][1])
  print output
  f_output.write(output + '\n')

# ngrams_sorted = sorted(ngrams, key=ngrams.get, reverse=True) #this results in a list, not a dictionary
# top_20_ngrams = ngrams_sorted[0:20]
# for i in range(0, len(top_20_ngrams)):
#   output = binascii.hexlify(ngrams_sorted[i]) + " " + str(ngrams[ngrams_sorted[i]])
  # print output
  # f_output.write(output + '\n')

output = "Unique number of ngrams: " + str(len(ngrams))
print output
f_output.write(output + '\n')

time2 = time.time()
output = "Execution time: %.2f seconds" % (time2 - time1)
print output
f_output.write(output + '\n')

f_output.close()






 #record the current ngram into our tabulation. this is a janky way of doing it, as clearly it is not sustainable
    #to keep writing code like this for higher values of n, but since the assignment says n will only be 1, 2, or 3, 
    #this is fine. if n could be arbitrarily large then i would come up with a more elegant solution
    # if n==1:
    #   if not current_byte in ngrams:
    #     ngrams[current_byte] = 0
      
    #   ngrams[current_byte] += 1

    # if n==2:
    #   if not one_byte_ago in ngrams:
    #     ngrams[one_byte_ago] = {}

    #   if not current_byte in ngrams[one_byte_ago]:
    #     ngrams[one_byte_ago][current_byte] = 0
      
    #   ngrams[one_byte_ago][current_byte] += 1

    # if n==3:
    #   if not two_bytes_ago in ngrams:
    #     ngrams[two_bytes_ago] = {}

    #   if not one_byte_ago in ngrams[two_bytes_ago]:
    #     ngrams[two_byte_ago][one_byte_ago] = {}

    #   if not current_byte in ngrams[two_bytes_ago][one_byte_ago]:
    #     ngrams[two_bytes_ago][one_byte_ago][current_byte] = 0

    #   ngrams[two_bytes_ago][one_byte_ago][current_byte] += 1

