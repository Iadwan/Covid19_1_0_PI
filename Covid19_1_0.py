import json
from urllib.request import Request, urlopen
import datetime


## We Read from this Public API 

complete_url = "https://api.thevirustracker.com/free-api?countryTotal=JO"
  

# ouput Looks like the below:
##########
'''
{
   "countrydata":[
      {
         "info":{
		    "ourid":81,
		    "title":"Jordan",
		    "code":"JO",
		    "source":"https://thevirustracker.com/jordan-coronavirus-information-jo"
         },
         "total_cases":381,
         "total_recovered":177,
         "total_unresolved":0,
         "total_deaths":7,
         "total_new_cases_today":0,
         "total_new_deaths_today":0,
         "total_active_cases":197,
         "total_serious_cases":5,
         "total_danger_rank":95}],
				"stat":"ok"}

'''
############

#Request the URL and decode

req = Request(complete_url, headers={'User-Agent': 'Mozilla/5.0'})


#json method of response object  


webpage = urlopen(req).read().decode()



# convert json data into python data 

jsonget = json.loads(webpage)


if jsonget["stat"] != "bad": 
  
    # Get the value of "countrydata" 

    country_data = jsonget["countrydata"] 

 
    total_cases = country_data[0]["total_cases"]
 
    total_recovered = country_data[0]["total_recovered"] 
  
    total_deaths = country_data[0]["total_deaths"] 
  
 
  
    # Print  Data 

    date_time = datetime.datetime.now()

    print (date_time)

    print("COVID-19 - Jordan \n" +
          "Jordan-Confirmed: " +
                    str(total_cases) + 
          "\nJordan-Recovered: " +
                    str(total_recovered) +
          "\nJordan-Death: " +
                    str(total_deaths))

  
else: 
    print(" Country Not Found ") 








