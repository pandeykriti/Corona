import sys
import config,web_scrapper
from skill_keywords_match import*
def main():
    # If city is included,only search and recommend jobs in the city
    location=''
    if (len(sys.argv) > 1):
        #Check if input city nae matches our pre-defined list
        if(sys.argv[1] in config.JOB_LOCATIONS):
            location=sys.argv[1]
        else:
            sys.exit('***Please ttry again.***\nEither leave it blank or input a city from list:\n{}'.format('\n'.join(config.JOB_LOCATIONS)))
        #------------------------------
        #------Scrape from web or read from local saved
        jobs_info=web_scrapper.get_jobs_info(location)
        #-----Keyword extraction and analysis-----
        skill_match = skill_keywords_match(jobs_info)
        # Extract skill keywords from job descriptions
        skill_match.extract_jobs_keywords()
        # Show exploratory data analysis if job search is nationwide i.e. no iput for city
        if(len(sys.argv)==1):
            skill_match.exploratory_data_analysis()
        resume_skills = skill_match.extract_resume_keywords(config.SAMPLE_RESUME_PDF)
        # Calculate similarity of skills from a resume and job posts
        top_job_matches = skill_match.cal_similarity(resume_skills.index, location)
        # Save matched jobs to a file
        top_job_matches.to_csv(config.RECOMMENDED_JOBS_FILE + location + '.csv', index=False)
        print('File of recommended jobs saved')

    if __name__ == "__main__":
        main()