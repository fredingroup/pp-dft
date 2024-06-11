import library.spectrum as spc

def main():
	import library.main_window as g
	inputs = g.main()
	spc.read_state_file(inputs['states'])


	if inputs['plots']['absorbance']:
		# plot individual spectra with sticks
		for state in inputs['states']:
			spc.plot_sticks(state, region=inputs['region'])

		# plot combined spectra
		spc.plot_spec(inputs)



	# plot combined dads
	if inputs['plots']['dads']:
		spc.plot_dads(inputs)



	# make Jablonski diagram
	# not yet implemented
	if inputs['plots']['jablonski']:
		pass


if __name__ == '__main__':
	main()