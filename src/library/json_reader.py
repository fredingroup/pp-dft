import pandas as pd
import json
from .region import Region
from . import spectrum as spc

# %%
##            What's This?            ##
#
# manages input via reading json files (see ../input_files/*.json)
# Computes Absorbance spectra for all states indicated in the json file
# Returns an object containing relevant information
# 
# The returned object is as follows:
#	output : {
# 		spectra: {
#			singets: df - spectra by name
#			triplets: df
#			all_spec: df - sum of singlets and triplets
#		},
#		DADS: {
#			same layout as spectra but difference spectra instead
#		},
#		transitions: {
#			name: df of transitions
#			name: ...
#			...
#		}
#	}

def loadjson(filename):
	# read json file listing parameters, states of interest, and datafile names
	with open(filename, 'r') as f:
		input = json.load(f)

	# prepare dataframes to contain data
	singlets = pd.DataFrame()
	triplets = pd.DataFrame()
	full_spec= pd.DataFrame()

	# Prepare an output object to store all the relevant information
	output={
		'molecule':input['molecule'],
		'spectra':{
			'singlet':singlets,
			'triplet':triplets,
			'full_spec':full_spec
		},
		'dads':{},
		'transitions':{}
	}

	# loop over multiwfn output files
	for file in input['files']:
		#read date from singlet and triplet transition files
		nstates=file['nstates']
		try:
			file['singlet_transitions'] = pd.read_csv(file['singlet'],delim_whitespace=all,header=3,skiprows=[nstates+7,nstates+8, nstates+9])
			file['triplet_transitions'] = pd.read_csv(file['triplet'],delim_whitespace=all,header=3,skiprows=[nstates+7,nstates+8, nstates+9])
		except pd.errors.ParserError:
			print(f"Could not parse file")

		# Add a column to transitions df with energy in (nm)
		file['singlet_transitions']['Diff.(nm)']=spc.eV_to_nm(file['singlet_transitions']['Diff.(eV)'])	
		file['triplet_transitions']['Diff.(nm)']=spc.eV_to_nm(file['triplet_transitions']['Diff.(eV)'])	
		
		# each pair of files has a list of states of interests
		# group transitions by starting state i
		sing_group = file['singlet_transitions'].groupby('i')
		trip_group = file['triplet_transitions'].groupby('i')

		# compute the spectra for each state and save to dataframe with name from JSON file
		for state in file['states']:
			name = "{}/{}".format(state['name'],file['name'])
			print(name)
			output['transitions'][name] = {
				'singlet':sing_group.get_group(state['n']),
				'triplet':trip_group.get_group(state['n'])}
			singlets[name] = spc.compute_spec(output['transitions'][name]['singlet'])
			triplets[name] = spc.compute_spec(output['transitions'][name]['triplet'])
			full_spec[name] = singlets[name] + triplets[name]

	# compute dads and store with object
	for name,df in output['spectra'].items():
		output['dads'][name] = pd.DataFrame()
		for column in df.columns:
			output['dads'][name][column] = df[column] - df[df.columns[0]]



	return output


# %%
if __name__ == "__main__":
	print('Reading Files...')
	# bod
	# data = jr.loadjson('C:/Users/gabri/LU Student Dropbox/Gabe Masso/Fredin Group/Gabe/pump_probe_TDDFT/scripts/thesis/input_files/bodipy_input.json')
	
	# rub
	# data = jr.loadjson('C:/Users/gabri/LU Student Dropbox/Gabe Masso/Fredin Group/Gabe/pump_probe_TDDFT/scripts/thesis/input_files/rubipy_input.json')
	
	# znp
	# data = jr.loadjson('C:/Users/gabri/LU Student Dropbox/Gabe Masso/Fredin Group/Gabe/pump_probe_TDDFT/scripts/thesis/input_files/znoep_input.json')
	
	# bod test
	data = loadjson('C:/Users/gabri/LU Student Dropbox/Gabe Masso/Fredin Group/Gabe/pump_probe_TDDFT/scripts/thesis/input_files/bodipy_temp.json')
	
	print("Plotting Spectra")
	spc.plot_sticks(data,data['molecule'],region=Region.MID)
	print("Plotting overlap")
	spc.plot_spec(data['spectra']['full_spec'],data['molecule'],region=Region.MID)

