import argparse
import pandas as pd
import os

##            What's This?            ##
#
# Right now sets up arguments for calling the main program from the command line
# 
# might change it later so that it manages whichever type of input (args,gui,json)
#
# 


def get_args():
	parser = argparse.ArgumentParser(description='This will take output files from the Multiwfn program and convert the transition energies and oscillator strengths to theoretical UV-Vis spectra. ')
	parser.add_argument('filename')
	parser.add_argument('-s','--saved',action='store_true',dest='save',help='indicate that the spectra have already been computed and are can be read from a csv file (filename)')
	parser.add_argument('-r','--region',choices=['UVVIS','IR','LARGE'],default='LARGE',dest='reg',help='define the region of the spectrum')
	parser.add_argument('-n','--nstates',type=int,default=30,dest='n',help='define the the number of states run in the td (default: 30)')
	parser.add_argument('-o','--output',dest='outfile', default='spectra.csv', help='define an output file for the spectral data. Data can be read with subsequent call with the \'-s\' option. Not applicable concurrently with \'-s\' option. (default: spectra.csv)')
	parser.add_argument('-i','--image', nargs='?', const= 'spectra.png',default=None, dest='imgfile', help='Graph of spectra will be displayed and then saved as a file with the given name. (default name: spectra.png) Image will not be saved automatically without this option.')
	parser.add_argument('-t','--title', nargs='?', const= 'Absorbance Spectra',default=None, metavar='GRAPH_TITLE', dest='gtitle', help='Input the title to be displayed on the graph')
	parser.add_argument('-d','--dads',action='store_true',dest='dads',help='also create a graph of the dads, subtracting the ground state from each spectrum')
	return parser.parse_args()


def process_directory(directory):
	# Initialize an empty DataFrame to store the combined results
	combined_df = pd.DataFrame(index=region)
	combined_df.index.name = "Wavelength"

	# Walk through the directory, subdirectories, and files 
	for root, dirs, files in os.walk(directory):
			# Loop over each file
			state_df = pd.DataFrame()
			if len(files) > 0:
				(path,dirname)=os.path.split(root)
				n=int(dirname[-1])

			for filename in files:
				# Construct the full file path
				filepath = os.path.join(root, filename)
				print(filepath)
				try:
					# Read the file into a DataFrame
					data = pd.read_csv(filepath,delim_whitespace=all,header=3,skiprows=[nstates+7,nstates+8, nstates+9])
					data = data.groupby(data.i).get_group(n)
				except pd.errors.ParserError:
					print(f"Could not parse file: {filepath}")

				# compute the spectrum from the transition info
				spec = compute_spec(df=data)

				# Append the result to the combined DataFrame of the state
				state_df[filename]=spec

				# Sum the singlet and triplet spectra to get full spectra for states
				state_df['total'] = state_df.sum(axis=1)

			if len(files) > 0:
				(path,dirname)=os.path.split(root)
				combined_df[dirname] = state_df['total']

	combined_df.to_csv(args.outfile)
	return combined_df


# Call the function with your directory name
if __name__=="__main__":
	args = get_args()
	if(args.save): #if the data has already been computed, read it from the csv file
		print("reading from "+args.filename)
		df = pd.read_csv(args.filename,index_col=0)
	else: #else, compute from transition info
		print("computing from files in "+args.filename)
		df = process_directory(args.filename)

	if(args.dads): #if requested, also compute dads
		dads_df = pd.DataFrame(index=region)
		dads_df.index.name = "Wavelength"
		for column in df:
			dads_df[column] = df[column] - df['s0']
		dads_df.to_csv("dads.csv")
		
	# plot_spec(df)
	# plot_spec(dads_df)