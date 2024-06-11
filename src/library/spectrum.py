import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from library.region import Region

#plot size
w=9
h=6.5

##            What's This?            ##
#
# Manage all the math and plotting
# (might split math and plotting into 2 modules)
# Want as simple as possible, input df/array return df/plot
#
#


# given a dataframe from a multiwfn output file, group to select specific state, and compute specrum for that state

# computes the spectrum
def compute_spec(df):
	output_eps=[]
	for wavelength in Region.ALL:
		const = (1.3062974*(10**8))/((10**7)/3099.6)

		epsilon_df = const*(df["Oscil.str"]) \
		*np.exp(-1*(((1/wavelength)-(1/(1239.84198/df['Diff.(eV)'])))/(1/3099.6))**(2))
		epsilon_df = epsilon_df.sum()
		output_eps.append(float(epsilon_df))
	return output_eps

# converts a Series of energies in eV to wavelength in (nm)
def eV_to_nm(ev):
	h = 4.135667696*(10**-15) # eV s
	c = 2.99792458*(10**17) # nm/s
	return (h*c)/ev

# Plots all spectra of listed in the provided dictionary in one figure
def plot_spec(input):

	title = input['title']
	region = Region[input['region']]
	fig, ax = plt.subplots()
	fig.set_size_inches(w,h)
	plt.xlim(region[0],region[-1])
	for state in input['states']:
		ax.plot(state.data['spectrum'],label=state.getText(style='a'))
	ax.legend()
	ax.set_ylabel('\u03B5')
	ax.set_xlabel("Wavelength (nm)")
	plt.title(title)
	# if(args.imgfile is not None):
	# 	plt.savefig(args.imgfile)
	plt.show(block=True)


# Plots all spectra of listed in the provided dictionary in one figure
def plot_dads(input):

	title = input['title']
	region = Region[input['region']]
	fig, ax = plt.subplots()
	fig.set_size_inches(w,h)
	# for i,geom in enumerate(df):
	# 	ax.plot(df,label='$S_%d$'%i)
	plt.xlim(region[0],region[-1])

	ground = input['states'][0]
	for state in input['states']:
		dads = [state.data['spectrum'][i]-ground.data['spectrum'][i] for i in range(len(ground.data['spectrum']))]
		ax.plot(dads,label=f'{state.getText()}-{ground.getText()}')
	ax.legend()
	ax.set_ylabel('\u03B5')
	ax.set_xlabel("Wavelength (nm)")
	plt.title(title)
	# if(args.gtitle is not None):
	# 	plt.title(args.gtitle)
	# if(args.imgfile is not None):
	# 	plt.savefig(args.imgfile)
	plt.show(block=True)



# Plots individual spectra in the data object 
# includes sticks for singlet and triplet transitions
# sticks can be turned off 

def plot_sticks(state, region='LARGE', sticks=True):
	plt.style.use('seaborn-v0_8-poster')

	region = Region[region]
	fig, ax1 = plt.subplots()
	fig.set_size_inches(w,h)

	plt.xlim(region[0],region[-1])
	ax1.plot(state.data['spectrum'])
	# ax1.legend(name)	
	ax1.set_ylabel('\u03B5')
	ax1.set_xlabel("Wavelength (nm)")
	plt.title(f"{state.getText(style='a')}")

	if(sticks):
		ax2 = ax1.twinx()

		# singlet transition data for sticks
		stick_x=state.data['transitions']['Diff.(nm)']
		stick_y=state.data['transitions']['Oscil.str']
		zeros = [0] * len(stick_y)
		ax2.errorbar(stick_x,stick_y,yerr=[stick_y,zeros],fmt=',') 

		ax2.set_ylabel("Oscillator Strength")


	plt.show(block=True)


# reads a multiwfn output file and computes absobance spectra
def read_state_file(input):
	# input should be shaped like:
	# input = [
	# 	{ path: <filepath>,
   	# 	  nstates: <number of states in td-dft computation>,
	# 	  ...
	#   },
	# 	...
	# ]
	for state in input:
		nstates = state.nstates
		# print(state.spin)
		try:
			data = pd.read_csv(state.path,delim_whitespace=all,header=3,skiprows=[nstates+7,nstates+8, nstates+9])
		except pd.errors.ParserError:
			print(f"Could not parse file")

		# print(data)
		group = data.groupby('i') 
		state.data['transitions'] = group.get_group(state.state)
		state.data['transitions']['Diff.(nm)']=eV_to_nm(data['Diff.(eV)'])
		state.data['spectrum'] = compute_spec(state.data['transitions'])