# Data cleaning and Visualisation

Covid-19 data serves perfectly for learning Python. There are many sources with Covid-19 data. As a start I decided to use Lithuanian open data portal. It provides data on testing results and positive cases by gender and age. File are .CSV and .JSON formats.

For analysis, I use epidemiological data published in [here](https://data.gov.lt/dataset/covid-19-epidemiologiniai-duomenys)

To visualize correctly current situation in Lithuania, I needed to clean data a bit.
  * Source has two columns of date: "Start of sickness" and "Positive test date". 
    * I used `<pd.to_datetime>` to convert string type to date type 
  * Gender column had empty values so I changed it to "unknown" and the same value for female was written in two ways.

This data set has an information on the end of the case. The values is the column are:
    * Gydomas - currently sick
    * Pasveiko - recovered   
    * Mirė - died         
    * Kita - other         
    * Nesirgo - never were sick
    *         - unknown
        
