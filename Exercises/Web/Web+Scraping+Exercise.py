
# coding: utf-8

# # Web Scraping Exercise
# 
# Lets Scrape the wall of shame from the U.S. Department of Health and Human Services
# Office for Civil Rights (You could just download the data file, but where is the fun in that!)

# ## Step 1 - Import all of the libraries you'll need
# 1. requests
# 2. pandas
# 3. numpy
# 4. matplotlib.pyplot
# 5. Beautiful Soup

# In[25]:


import requests, pandas, numpy, matplotlib.pyplot
from bs4 import BeautifulSoup


# ## Step 2 - Download the data
# 2.a Use the requests library to grab the content of this page <https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf>

# In[26]:


page = requests.get("https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf")


# In[ ]:


page.content


# 2.b Check thte status code of the page and print it to the screen

# In[29]:


page.status_code


# # Step 3 - BeautifulSoup

# 3.a Load the page content into a BeautifulSoup object named soup

# In[30]:


soup = BeautifulSoup(page.content, 'html.parser')


# 3.b Display the soup object to visually interrogate

# In[31]:


soup


# # Step 4 - Parse the Breach data
# 
# After inspecting the page we found that ```<td role="gridcell">``` usually precedes the breach records.
# 
# 4.a find the gridcells and store in a variable named ```gridCell```

# In[35]:


gridCells = soup.find_all(role="gridcell")


# In[33]:


tr = soup.find_all('tr')


# In[34]:


len(tr)


# 4.b display the gridCells to inspect

# In[36]:


gridCells


# We've decided that we want to store the contents of the breach data into lists named:
# 
# ```
# singleBreachList - contains the tokenized breach data from the web page
# ```
# 
# We'll use singleBreachList to construct the following lists
# 
# ```
# nameCoveredEntityList             - singleBreachList item 0
# stateList                         - singleBreachList item 1
# coveredEntityTypeList             - singleBreachList item 2
# affectIndividualsList             - singleBreachList item 3
# breachSubmittedDateList           - singleBreachList item 4
# typeOfBreachList                  - singleBreachList item 5
# locationOfBreachedInformationList - singleBreachList item 6
# 
# ```
# 
# Also notice that not all of "gridcell" was breach data, we need to skip a couple lines to get to the good stuff. Use a counter to do this, specifically 
# 
# ```
# skipTheBoringStuffCounter
# ```
# 
# There also appears to be a pattern in how the gridcell data is organized, there is a new event every 8 lines. Use a counter for that as well, specifically 
# 
# ```
# theGoodStuffCounter
# ```
# 
# 4.c Initialize all of the lists to empty lists and the counters to zero.

# In[21]:


nameCoveredEntityList = []
stateList = []
coveredEntityTypeList = []
affectIndividualsList = []
breachSubmittedDateList = []
typeOfBreachList = []
locationOfBreachedInformationList = []
singleBreachList = []
skipTheBoringStuffCounter = 0
theGoodStuffCounter = 0


# 4.d Complete the loop below

# In[39]:


for c in gridCells:
    if skipTheBoringStuffCounter <= 4:
        # todo: increment the counter
        
        # *** begin solution
        skipTheBoringStuffCounter = skipTheBoringStuffCounter + 1
        # *** end solution

    if skipTheBoringStuffCounter > 4:
        # todo: remove whitespace from the text
        
        # *** begin solution
        c = c.get_text().strip()
        # *** end solution
        
        if c != '':
            # todo: add the cell to the singleBreachList and increment theGoodStufCounter
            
            # *** begin solution
            singleBreachList.append(c)
            theGoodStuffCounter = theGoodStuffCounter + 1
            # *** end solution

            if theGoodStuffCounter == 8:
                # todo: add breach data to each list as described above
                
                # *** begin solution
                nameCoveredEntityList.append(singleBreachList[0])
                stateList.append(singleBreachList[1])
                coveredEntityTypeList.append(singleBreachList[2])
                affectIndividualsList.append(singleBreachList[3])
                breachSubmittedDateList.append(singleBreachList[4])
                typeOfBreachList.append(singleBreachList[5])
                locationOfBreachedInformationList.append(singleBreachList[6])
                # *** end solution
                
                theGoodStuffCounter = 0
                singleBreachList = []


# In[38]:


nameCoveredEntityList[0:3]


# # Step 5 - Create a Dataframe and Visualize the Data

# In[40]:


# create a dataframe using the newly scraped data
breachDF = pandas.DataFrame({
"Company Name":nameCoveredEntityList,
"State":stateList,
"Company Type":coveredEntityTypeList,
"Affected Individuals":affectIndividualsList,
"Breach Date":breachSubmittedDateList,
"Breach Type":typeOfBreachList,
"Data location":locationOfBreachedInformationList
})


# In[41]:


breachDF


# In[42]:


# group by the Breach Type
breachDF.groupby('Breach Type').size()


# In[43]:


# allow matplotlib graphs to show in the notebook
get_ipython().magic('matplotlib inline')


# In[44]:


# group by the Breach Type
breachDist = breachDF.groupby('Breach Type').size()


# In[45]:


# plot the data
breachDist.plot(kind='bar')


# [Source](https://www.peerlyst.com/posts/python-webscraping-anaconda-beautifulsoup-jupyter-and-the-hhs-wall-of-shame-molly-payne)
