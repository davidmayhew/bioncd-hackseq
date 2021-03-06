import sys, lzma, getopt
from sklearn.cluster import AgglomerativeClustering

#given 2 sequence strings, returns sequences + concatenation as an object of bytes
def return_byte(sequence1, sequence2):
	seq1 = bytes(sequence1, 'utf-8')
	seq2 = bytes(sequence2, 'utf-8')
	seqconcat = concat(seq1, seq2)
	return(seq1, seq2, seqconcat)

#compresses input sequence using lempel-ziv markov algorithm
def compress_lzma(sequence):
	#lzma requires Python 3.
    lz = lzma.compress(sequence)
    return lz

#input
def compressed_size(sequences):
	compressed_seq1 = compress_lzma(sequences[0])
	compressed_seq1_size = sys.getsizeof(compressed_seq1)
	compressed_seq2 = compress_lzma(sequences[1])
	compressed_seq2_size = sys.getsizeof(compressed_seq2)
	compressed_seqconcat = compress_lzma(sequences[2])
	compressed_seqconcat_size = sys.getsizeof(compressed_seqconcat)
	return(compressed_seq1_size, compressed_seq2_size, compressed_seqconcat_size)

#calculates NCD for 2 sequence sizes and their concatenation size	
def compute_distance(x,y,cxy):
    if x > y :
        distance = ((cxy - y) / x)
    elif y > x :
        distance = ((cxy - x) / y)
    else:
        distance = ((cxy - x) / x)
    return distance

#concatenates two input sequences together
def concat(sequence1, sequence2):
	concat_genome = sequence1 + sequence2
	return concat_genome


def main(argv):
	#parse command line arguments
	inputfile1=''
	inputfile2=''
	outputfile=''

	try:
		opts, args = getopt.getopt(argv, "hx:y:",["ifile1=","ifile2="])
	except getopt.GetoptError:
		print('compress.py -x <inputfile1> -y <inputfile2>')
		sys.exit(3)

	for opt, arg in opts:
		if opt == '-h':
			print('compress.py -x <inputfile1> -y <inputfile2>')
			sys.exit()
		elif opt in ("-x", "--ifile1"):
			inputfile1 = arg
		elif opt in ("-y", "--ifile2"):
			inputfile2 = arg

	#error conditions: missing input and confliciting command line arguments
	if inputfile1=='' or inputfile2=='':
		print("Error: Missing input")
		sys.exit(3)

	#open input sequences, exits if file not found
	try:
		with open (inputfile1, "r") as myfile:
			seq1 = myfile.read()
	except:
		print('Error reading sequence 1')
		sys.exit(3)
	
	try:
		with open (inputfile2, "r") as myfile:
			seq2 = myfile.read()
	except:
		print('Error reading sequence 2')
		sys.exit(3)

	#convert input sequences into bytes
	sequences = return_byte(seq1, seq2)
	
	#compress input sequences
	sizes = compressed_size(sequences)

	#compute ncd values
	ncd = compute_distance(sizes[0], sizes[1], sizes[2])
	print(ncd)

if __name__== "__main__":
	main(sys.argv[1:])
