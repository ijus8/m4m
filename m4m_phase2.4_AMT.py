import json
import datetime
import csv

with open("meal4monsters-export_v3.1.json", "r") as read_file:
    data = json.load(read_file)  
    ## Note that I took out one data entry from the JSON file bc the one with Korean in it is not ascii and was
    ## throwing errors. So that one Korean entry (userID that includes Korean) will have to added manually.



def readTimestamp(timestamp):
	return datetime.datetime.strptime(timestamp, '%m %d %Y_%H %M %S %p') 
	### how we are (if at all) mediating for the fact that time is recorded
	### in the time zone the device is set to. Therefore, we have GMT, EST, CDT, etc.
	### Since we are only recording the time difference we do NOT have to worry about this issue. 

def getRoundTime(user,whichRound):
	ts = data["M4M_Phase2_AMT"][user]["timestamps"]
	rnd = data["M4M_Phase2_AMT"][user]
	startTime = ""
	endTime = ""
	total_Dur=""
	#timestamps are keys, events are values
	for key in sorted(ts):
		#if (not startTime == "") and (endTime == "") and (ts[key].endswith("begins\"") or ts[key]=="\"Game Result\""): 
		if (not startTime == "") and (endTime == "") and (ts[key]=="\"Game Result\""): 
			endTime = key
			print ("Start Time: " + startTime) 
		if ts[key] == "\"round "+whichRound+" begins\"":
			startTime = key
			print ("End Time: " + endTime) 
	if (not startTime == "") and (not endTime == ""):
		total_Dur = (str(readTimestamp(endTime) - readTimestamp(startTime)))
		print ("First Rnd to Game Result Duration: " + str(readTimestamp(endTime) - readTimestamp(startTime)))
	

	### this is where I will start the duration the users spent on the community board page in each round
	### so there is (if collected properly), five duration instances (each one for each round) per user
	## so from "reason submit button click" to "comm submit button click" per each round OR after the first round up to "round # result screen"

	for key in sorted(ts):
		if ts[key] == "\"reason submit button click\"":
			startTime = key
			break #break here

	for key in sorted(ts):
		if ts[key] == "\"round 1 result screen\"":
			rnd1_result = key
		if ts[key] == "\"round 2 result screen\"":
			rnd2_result = key
		if ts[key] == "\"round 3 result screen\"":
			rnd3_result = key
		if ts[key] == "\"round 4 result screen\"":
			rnd4_result = key
		if ts[key] == "\"round 5 result screen\"":
			rnd5_result = key

	counter=0
	count_array = []

	
	for key in sorted(ts):
		counter +=1
		if ts[key] == "\"reason submit button click\"":
			counter = 0 	
		if ts[key] == "\"comm submit button click\"":
			count_array.append(counter)
	#print (count_array)
	freq_clicks_array = count_array
	# print ("Community Board Round A Clicks: " + str(count_array[0]))	
	# print ("Community Board Round B Clicks: " + str(count_array[1]))	
	# print ("Community Board Round C Clicks: " + str(count_array[2]))	
	# print ("Community Board Round D Clicks: " + str(count_array[3]))	
	# print ("Community Board Round E Clicks: " + str(count_array[4]))
	
	cb_1_clicks = str(count_array[0])
	cb_2_clicks = str(count_array[1])
	cb_3_clicks = str(count_array[2])
	cb_4_clicks = str(count_array[3])
	cb_5_clicks = str(count_array[4])

	rnd1_d = readTimestamp(rnd1_result) - readTimestamp(startTime) 
	rnd2_d = readTimestamp(rnd2_result) - readTimestamp(rnd1_result) 
	rnd3_d = readTimestamp(rnd3_result) - readTimestamp(rnd2_result) 
	rnd4_d = readTimestamp(rnd4_result) - readTimestamp(rnd3_result) 
	rnd5_d = readTimestamp(rnd5_result) - readTimestamp(rnd4_result) 

	# print("Round A Duration: " + str(rnd1_d))
	# print("Round B Duration: " + str(rnd2_d))
	# print("Round C Duration: " + str(rnd3_d))
	# print("Round D Duration: " + str(rnd4_d))
	# print("Round E Duration: " + str(rnd5_d))
	rnd1_dur = str(rnd1_d)
	rnd2_dur = str(rnd2_d)
	rnd3_dur = str(rnd3_d)
	rnd4_dur = str(rnd4_d)
	rnd5_dur = str(rnd5_d)


	init_choice = {} 
	comm_choice = {} 
	## initialize them as an empty dictionary and then read them when I am done with the loop

	#round_L-#_choice/reason : keys
	#numbers (specifically #-#) and reasonings in text: values
	initial_choices = [ ]
	initial_reasons = [ ]
	community_choices = [ ]
	community_reasons = [ ]
	for key in sorted(rnd):	
		mealShown = key[8]
		reason = rnd[key]


		if (key.endswith("t_choice")):
			init_choice[str(mealShown)] = rnd[key][1]
			#print ("Round " + mealShown + " Initial Choice: " + reason[1])
			initial_choices.append(reason[1])

		if (key.endswith("t_reason")):
			#print ("Round " + mealShown + " Initial Reason: " + reason) 	
			initial_reasons.append(reason)

		if (key.endswith("m_choice")):
			comm_choice[str(mealShown)] = rnd[key]		
			#print ("Round " + mealShown + " Post-Community Choice: " + reason)
			community_choices.append(reason)

		if (key.endswith("m_reason")):
			#print ("Round " + mealShown + " Post-Comm Reason: " + reason) 
			#print (mealShown)
			community_reasons.append(reason)

	answer_changes = [ ]
	#answer_not_change = [ ]
	for x in xrange(1,6):
		if (init_choice[str(x)] == comm_choice[str(x)]):
			#print ("Round " + str(x) + " Answer Change: 1") ## meal choice REMAINED THE SAME
			answer_changes.append(1) 

		else:
			#print ("Round " + str(x) + " Answer Change: 0") ## meal choice changed after community board
			answer_changes.append(0)
	
	return {"total duration": total_Dur, "frequency clicks all": freq_clicks_array, "community 1 clicks": cb_1_clicks, "community 2 clicks": cb_2_clicks,
			"community 3 clicks": cb_3_clicks, "community 4 clicks": cb_4_clicks, "community 5 clicks": cb_5_clicks, "round 1 duration": rnd1_dur, 
			"round 2 duration": rnd2_dur, "round 3 duration": rnd3_dur, "round 4 duration": rnd4_dur, "round 5 duration": rnd5_dur, "initial choices": initial_choices,
			"initial reasons": initial_reasons, "comm choices": community_choices, "comm reasons": community_reasons, "answer change": answer_changes 
			}

def firstLetter(ts):
	for t in sorted(ts):
		if ( ts[t].startswith("\"round ") and ts[t].endswith("begins\"")  ) : 
			return ts[t][6]

for user in data["M4M_Phase2_AMT"]: 
	#print (user)

	try:
		print ("Monster Choice: " + data["M4M_Phase2_AMT"][user]["monster choice"])
		data["M4M_Phase2_AMT"][user]["results"] = getRoundTime(user,firstLetter(data["M4M_Phase2_AMT"][user]["timestamps"])) 
		print ("")
	except Exception as e:
		print (e)
		print ("")




 ##calling the function firstLetter



# for ts in data["M4M_Phase2_AMT"][user]["timestamps"]: 
# 	#print (user)	
# 	try:
# 		#print ("Monster Choice: " + data["M4M_Phase2_AMT"][user]["monster choice"])
# 		#ts = data["M4M_Phase2_AMT"][user]["timestamps"]
# 		data["M4M_Phase2_AMT"][user]["results"] = getRoundTime(user,ts[6]) 
# 		## getRoundTime's function second argument is WHATEVER STRING (A, B, C, D, E) appears first, 
# 		print ("")
# 	except Exception as e:
# 		print (e)
# 		print ("")

with open('m4m_AMT.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["userID","Monster_Number","First Rnd to Game Result Duration","Community Board Freq Clicks Array","CB Clicks A",
    	"CB Clicks B","CB Clicks C","CB Clicks D","CB Clicks E","RndA Duration","RndB Duration","RndC Duration","RndD Duration","RndE Duration",
    	"Init Choice","Init Reason","Community Choice","Community Reason","Init Choice","Init Reason","Community Choice","Community Reason","Init Choice","Init Reason","Community Choice","Community Reason","Init Choice","Init Reason","Community Choice","Community Reason","Init Choice","Init Reason","Community Choice","Community Reason",
    	"Rnd1 Answer Change","Rnd2 Answer Change","Rnd3 Answer Change","Rnd4 Answer Change","Rnd5 Answer Change" ])
    for row in data["M4M_Phase2_AMT"]:
    	try:
    		writer.writerow([ row, data["M4M_Phase2_AMT"][row]["monster choice"],data["M4M_Phase2_AMT"][row]["results"]["total duration"],data["M4M_Phase2_AMT"][row]["results"]["frequency clicks all"],
    		
    		
    		## community board clicks to see "engagement" in order of rounds
    		data["M4M_Phase2_AMT"][row]["results"]["community 1 clicks"],data["M4M_Phase2_AMT"][row]["results"]["community 2 clicks"],data["M4M_Phase2_AMT"][row]["results"]["community 3 clicks"],
    		data["M4M_Phase2_AMT"][row]["results"]["community 4 clicks"],data["M4M_Phase2_AMT"][row]["results"]["community 5 clicks"],

    		## durations in order of rounds 
    		data["M4M_Phase2_AMT"][row]["results"]["round 1 duration"],data["M4M_Phase2_AMT"][row]["results"]["round 2 duration"],data["M4M_Phase2_AMT"][row]["results"]["round 3 duration"],
    		data["M4M_Phase2_AMT"][row]["results"]["round 4 duration"],data["M4M_Phase2_AMT"][row]["results"]["round 5 duration"],
    		
    		#round 1 -- choices and reasons
    		data["M4M_Phase2_AMT"][row]["results"]["initial choices"][0],data["M4M_Phase2_AMT"][row]["results"]["initial reasons"][0],
    		data["M4M_Phase2_AMT"][row]["results"]["comm choices"][0],data["M4M_Phase2_AMT"][row]["results"]["comm reasons"][0],

    		#round 2 -- choices and reasons
    		data["M4M_Phase2_AMT"][row]["results"]["initial choices"][1],data["M4M_Phase2_AMT"][row]["results"]["initial reasons"][1],
    		data["M4M_Phase2_AMT"][row]["results"]["comm choices"][1],data["M4M_Phase2_AMT"][row]["results"]["comm reasons"][1],

    		#round 3 -- choices and reasons
    		data["M4M_Phase2_AMT"][row]["results"]["initial choices"][2],data["M4M_Phase2_AMT"][row]["results"]["initial reasons"][2],
    		data["M4M_Phase2_AMT"][row]["results"]["comm choices"][2],data["M4M_Phase2_AMT"][row]["results"]["comm reasons"][2],

    		#round 4 -- choices and reasons
    		data["M4M_Phase2_AMT"][row]["results"]["initial choices"][3],data["M4M_Phase2_AMT"][row]["results"]["initial reasons"][3],
    		data["M4M_Phase2_AMT"][row]["results"]["comm choices"][3],data["M4M_Phase2_AMT"][row]["results"]["comm reasons"][3],

    		#round 5 -- choices and reasons
    		data["M4M_Phase2_AMT"][row]["results"]["initial choices"][4],data["M4M_Phase2_AMT"][row]["results"]["initial reasons"][4],
    		data["M4M_Phase2_AMT"][row]["results"]["comm choices"][4],data["M4M_Phase2_AMT"][row]["results"]["comm reasons"][4],

    		data["M4M_Phase2_AMT"][row]["results"]["answer change"][0],data["M4M_Phase2_AMT"][row]["results"]["answer change"][1], data["M4M_Phase2_AMT"][row]["results"]["answer change"][2], 
    		data["M4M_Phase2_AMT"][row]["results"]["answer change"][3], data["M4M_Phase2_AMT"][row]["results"]["answer change"][4]
    		])
    	except Exception as e:
    		print (e)

