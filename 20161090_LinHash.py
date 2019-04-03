import sys,os
i , p , S, b , b_new, bucket_count, total_block_count = 0 , 0 , 0 , 2 , 4 , 2 , 2
linHash = {}
block_count = {}
block_count[0] = 1
block_count[1] = 1

output_buffer = []
input_buffer = []

def hash_table_too_full():

	temp = B * total_block_count
	density = ( S * 400.0 ) / temp
	if density > 75:
		return 1
	else:
		return 0
	return 0

def insertion (num):
	global S, total_block_count, output_buffer
	flag = 0

	hash_val = num % b
	if hash_val < p:
		hash_val = num % b_new
	if hash_val not in linHash:
		linHash[hash_val] = [[]]

	for i in range(block_count[hash_val]):
		if num in linHash[hash_val][i]:
			flag = 1
	
	if not flag:
		S += 1
		temp = block_count[hash_val] - 1
		l = []

		if len(linHash[hash_val][temp]) >= ((B * 1.0) / 4.0):
			total_block_count += 1
			temp += 1
			block_count[hash_val] += 1
			linHash[hash_val].append(l)
		linHash[hash_val][temp].append(num)
		output_buffer.append(num)

		# Buffer overflow
		if len(output_buffer) >= (B  / 4.0):
			for val in output_buffer:
				print(str(val))
			# Empty output_buffer
			output_buffer = []

	if hash_table_too_full() == 1:
		create_new_bucket()
	else:
		return


def create_new_bucket():
	global bucket_count, p, b, b_new, total_block_count

	replace_array = []
	bucket_count += 1

	pBlockCount = block_count[p]
	for i in range(pBlockCount):
		for value in linHash[p][i]:
			replace_array.append(value)

	total_block_count = total_block_count-pBlockCount

	linHash[p] = [[]]
	block_count[p] = 1
	total_block_count += 1

	linHash[bucket_count - 1] = [[]]
	block_count[bucket_count - 1] = 1
	total_block_count += 1

	for value in replace_array:
		hash_val = value % b_new

		if hash_val not in linHash:
			linHash[hash_val] = [[]]
			block_count[hash_val] = 1
			total_block_count += 1

		flag = 0
		for j in range(block_count[hash_val]):
			if value in linHash[hash_val][j]:
				flag = 1

		if not flag:
			temp = block_count[hash_val] - 1
			if len(linHash[hash_val][temp]) >= (B * 0.25):
				temp += 1
				block_count[hash_val] += 1
				total_block_count += 1
				l = []
				linHash[hash_val].append(l)
			linHash[hash_val][temp].append(value)
	p += 1

	if bucket_count == b_new:
		b_new = 4 * b
		b *= 2
		p = 0

	return 1


filename = sys.argv[1]
B = int(sys.argv[3])
M = int(sys.argv[2])

if os.path.isfile(filename):
	# Start reading file
	with open(filename) as fh:
		for line in fh:
			num = int(line.strip())
			input_buffer.append(num)
			if len(input_buffer) >= (((M-1) * B * 1.0) / 4.0) :
				for val in input_buffer:
					insertion(val)
				input_buffer = []
	fh.close()

	for val in input_buffer:
		insertion(val)

	for val in output_buffer:
		print(str(val))

# If file does not exist
else:
	print("Invalid File")
	exit(-1)

