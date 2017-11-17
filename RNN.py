import read_data as rd
			

def main():
	path = '/home/jterstall/Documents/CI/CI_Project/train_data/'
	category_index_input, category_index_output, input_data, output_data = rd.read_data(path)
	

if __name__ == '__main__':
	main()