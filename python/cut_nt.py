def Cut_nt(file_name):
	fp1 = open(file_name, 'r')
	fp2 = open(file_name.split('.')[0]+'_nthash'+'.txt', 'w+')

	while 1:
		s_hash = fp1.readline()
		if not s_hash:
			break
		nt_hash = s_hash.split(':')[3]
		fp2.write(nt_hash + '\n')
	fp2.close()
	fp1.close()

if __name__ == '__main__':
	Cut_nt('aiusahash.txt')