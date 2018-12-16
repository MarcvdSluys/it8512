'''
Open Source Initiative OSI - The MIT License:Licensing
Tue, 2006-10-31 04:56 nelson

The MIT License

Copyright (c) 2018 Ceriel Jacobs

Precise Solar Panel Maximum Power Point Tracker (mppt) and module sorter 
for custom set operating level conversion.
Custom irridiation level because it makes no sense to current sort modules
at STC when average power generation is at 470 W/m2 in the South East of
The Netherlands), 

Using: 
- Itech IT8512A+ e-load with E-133 USB (ID 067b:2303) set to 38400 8N1
- Zes Zimmer LMG95 power analyser to improve tracking and power accuracy
- Fraunhofer ISE WPVS reference cell attached to a 2nd LMG95
- Barcode scanner to grab serial numbers && end measurements

Meas. accuracy		IT8512A+		FS		LMG95			FS
 Voltage: 			0.025%+0.025%FS	18|120	0.02%+0.06%FS	6|12.5|25|60
 Current: 			0.05%+0.05%FS	3|30	0.02%+0.06%FS	0.15|.3|.6|1.2
 Power:				0.1%+0.1%FS				0.03%+0.06%FS
'''
set_volts_delta_low = .32 #lowest voltage change that makes sense for IT8512A+ current measurement accuracy to speed up
                          #was .02 during testing

import sys, math, random, os.path, dcload, time
err = sys.stderr.write
start_time = time.time()

def TalkToLoad(load, port, baudrate):
	def test(cmd, results):
		if results:
			print cmd, "failed:"
			print "  ", results
			exit(1)
		else:
			print cmd
	def round_down(n, decimals=0):
		multiplier = 10 ** decimals
		return math.floor(n * multiplier) / multiplier

	load.Initialize(port, baudrate) # Open a serial connection
	test("Set to remote control", load.SetRemoteControl())
	#load.TurnLoadOff()	# make sure that Voc is measured
	#time.sleep(0.5) # wait 0.5s

	while True: # Loop and wait for module to be connected
		values = load.GetInputValues().split("\t") # ask V voltage
		volts = float(values[0])
		amps = float(values[1])

		if volts > 4: 				# Start tracking when Voc > ...
			print "Vset ", "voltsN", "ampsN", "voltsP", "deltaV", "sVoD", "deltaW", "watts"
			print "     ", "{0:06.3f}".format(volts), "{0:05.3f}".format(amps) , ' 0.000', ' 0.000', '    ', ' 0.000', ' 0.000'
			Vset = round_down(volts * 0.75, 2) 	# value depends on set_volts_delta initial value: 25% of Voc = 1V > set_volts_delta
			load.SetMode('cv') #cv set=2 decimal digits
			#print 'Set CV to ' + str(Vset) + ' volts'
			load.SetCVVoltage(Vset)
			direction_prev = -1
			load.TurnLoadOn()
			# find mpp using modified incremental-conductance (IC) algorithm
			volts_prev = 0
			amps_prev = 0		# first measurement is Voc
			watts_prev = 0
			volts_prev = volts

			if volts > 20.48:
				set_volts_delta = 5.12
			elif volts > 10.28:
				set_volts_delta = 2.56
			elif volts > 5.12:
				set_volts_delta = 1.28
			else:
				set_volts_delta = 0.64

			while True:
				values = load.GetInputValues().split("\t")
				while abs(float(values[0]) - Vset) > 0.015: # match measured voltage to set voltage within 15 mV = variable wait time to speed up searching and increase precision
					#time.sleep(.012)
					#GetInputValues() takes 0.0148s at 38400 8N1
					#start_time2 = time.time()
					values = load.GetInputValues().split("\t")
					#print "Read time = %s" % (time.time() - start_time2)
				volts_new = float(values[0])
				amps_new = float(values[1])
				watts_new = float(values[2])
				#ask Illumination = illu_new
				delta_volts = volts_new - volts_prev
				delta_amps = amps_new - amps_prev
				delta_watts = watts_new - watts_prev
				print "{0:05.2f}".format(Vset), "{0:06.3f}".format(volts_new), "{0:05.3f}".format(amps_new), "{0:06.3f}".format(volts_prev), "{0:+6.3f}".format(delta_volts), set_volts_delta, "{:+6.3f}".format(delta_watts), "{0:6.3f}".format(watts_new)

				if delta_watts == 0 or delta_volts == 0:
					# occurs in low light/power, randomly choose a direction?
					direction_new = random.choice([-1,1])
					Vset = Vset + (direction_new * set_volts_delta)
				elif delta_watts/delta_volts < 0:
					# we are at a higher voltage level then Vmp
					Vset = Vset - set_volts_delta
					direction_new = -1
				elif delta_watts/delta_volts > 0:
					# we are at a lower voltage level then Vmp
					Vset = Vset + set_volts_delta
					direction_new = 1

				load.SetCVVoltage(Vset)
				
				volts_prev = volts_new
				amps_prev = amps_new
				watts_prev = watts_new

				if direction_prev == 0:
					# first loop
					direction_prev = direction_new
				elif direction_new != direction_prev:
					if set_volts_delta < set_volts_delta_low:
						print "MPPT found in %s seconds" % round(time.time() - start_time, 2)
						load.TurnLoadOff()
						load.SetLocalControl()
						return
					else:
						set_volts_delta = set_volts_delta / 2
						direction_prev = direction_new

		else: # Voc < 4V
			time.sleep(.2) # poll 5 times a second

if __name__ == '__main__':
	try:
		if os.path.exists('/dev/ttyUSB-IT8512A'):
			port = 'ttyUSB-IT8512A'
		elif os.path.exists('/dev/ttyUSB0'):
	  		port = '/dev/ttyUSB0'
		elif os.path.exists('/dev/ttyUSB1'):
			port = '/dev/ttyUSB1'
		load = dcload.DCLoad()
		TalkToLoad(load, port, 38400)
	except KeyboardInterrupt:
		print('interrupted')
		load.TurnLoadOff()
		load.SetLocalControl()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
