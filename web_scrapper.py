import random,json
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time,os
import config
#maximum 500 jobs per city
max_results_per_city=500
#Number of jobs show on each result page
page_record_limit=50
number_pages=int(max_results_per_city/page_record_limit)
def get_jobs_info(search_location):
    #Scrape from web/saved file
    #Input: Search location
    #Output:Jobs_info
    exists=os.path.isfile(config.JOBS_INFO_JSON_FILE)
    if exists:
        with open(config.JOBS_INFO_JSON_FILE,'r') as fp:
            jobs_info=json.load(fp)
    else:
        jobs_info=web_scrape(search_location)
    return jobs_info
def web_scrape(search_location):
    '''Scrape jobs from indeed.ca
    Web scraping 101:http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/
    Input:
       search_location-search job in a certain city.Input from command line.
    Output: jobs-info'''
    #urls of all jobs
    job_links=[]
    #record time for web scrapping
    start=time.time()#start time
    #Launch webdriver
    driver=webdriver.Chrome(config.WEBDRIVER_PATH)
    job_locations=config.JOB_LOCATIONS
    #If search location is defined,only search that location
    if(len(search_location)>0):
        job_locations=[search_location]
    for location in job_locations:
        url = 'https://www.indeed.ca/jobs?q=' + config.JOB_SEARCH_WORDS + '&l=' \
              + location + '&limit=' + str(page_record_limit) + '&fromage=' + str(config.DAY_RANGE)
        # Set timeout
        driver.set_page_load_timeout(15)
        webdriver.DesiredCapabilities.CHROME["unexpectedAlertBehaviour"]="accept"
        driver.get(url)
        #Be kind and don't hit indeed server so hard
        time.sleep(3)
        for i in range(num_pages):

            try:
                # For each job on the page find its url
                for job_each in driver.find_elements_by_xpath('//*[@data-tn-element="jobTitle"]'):
                    job_link = job_each.get_attribute('href')
                    job_links.append({'location':location,'job_link':job_link})
                print('scrapping{} page{}'.format(location,i+1))
                # Go next page
                driver.find_element_by_link_text('Next »').click()
            except NoSuchElementException:
                # If nothing find, we are at the end of all returned results
                print("{} finished".format(location))
                break
                # Be kind and don't hit indeed server so hard
                time.sleep(3)
            # Write all jobs links to a json file so it can be reused later
        with open(config.JOBS_LINKS_JSON_FILE, 'w') as fp:
            json.dump(job_links, fp)
        #***Go through each job and gather detailed job info***
            # Info of all jobs
            jobs_info = []
            for job_lk in job_links:
    # Make some random wait time between each page so we don't get banned
               m=random.randint(1,5)
               time.sleep(m)
            # Retrieve single job url
            link = job_lk['job_link']
            driver.get(link)
            # Job city and province
            location = job_lk['location']
            # Job title
            title = driver.find_element_by_xpath(
                '//*[@class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"]').text
            # Company posted the job
            company = driver.find_element_by_xpath('//*[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]').text
            # Salary: if no such info, assign NaN
            if (len(driver.find_elements_by_xpath('//*[@class="jobsearch-JobMetadataHeader-item "]')) == 0):
                salary = np.nan
            else:
                salary = driver.find_element_by_xpath('//*[@class="jobsearch-JobMetadataHeader-item "]').text
            #description of job
            desc=driver.find_element_by_xpath('//*[@class="jobsearch-JobComponent-description ic-u-xs-mt--md"]').text
            jobs_info.append({'link':link,'location':location,'title':title,'company':company,'salary':salary,'desc':desc})
         #Write all jobs info to a jason so that can be re-used later
        with open(config.JOBS_INFO_JSON_FILE, 'w') as fp:
            json.dump(jobs_info, fp)
        #Close and quit webdriver
        driver.quit()
        #end time
        end=time.time()
        #Calculating web scaping time
        scaping_time=(end-start)/60
        print('Took{0:.2f} minutes scraping {1:d} data scientist/engineer/analyst_jobs'.format(scraping_time,len(jobs_info)))
        return jobs_info