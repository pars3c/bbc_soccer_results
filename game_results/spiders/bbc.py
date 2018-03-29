# -*- coding: utf-8 -*-
import scrapy
import datetime
import csv
now = datetime.datetime.now()

class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bbc.co.uk']
    start_urls = []

    def __init__(self):
        
        year = int(now.year) # Capture present Year
        month = int(now.month) # Capture present Month
        for i in range(1 ,13): # This will make sure we get all the 12 months from the present one to the 12 past ones
            month = int(month) 
            '''
            The results only show the previous month never the present
            (i.e: if we are in March we can only get February's results) 
            So, we go back 1 Month in the beggining of each iteration
            '''
            month = month - 1 

            '''
            If month is less than 1 or equal to 0 means it goes back to the Last Month of last Year 
            So month becomes 12 and goes one year back
            '''
            if month == 0:
                month = 12
                year = year - 1    
            month = str(month) # Month becomes a string in order to concatenate with the url string   
            if len(month) < 2:
                month = '0' + month
            url = 'http://www.bbc.co.uk/sport/football/portuguese-primeira-liga/scores-fixtures/' + str(year) + '-' + month
            self.start_urls.append(url)
   

    def parse(self, response):
        # Get Selected Year
        year = response.css('#sp-timeline-past-dates > li.sp-c-date-picker-timeline__item.sp-c-date-picker-timeline__item--selected > a > span.gel-long-primer.gs-u-display-block::text').extract_first()
        # Get Selected Month
        month = response.css('#sp-timeline-past-dates > li.sp-c-date-picker-timeline__item.sp-c-date-picker-timeline__item--selected > a > span.gel-long-primer-bold.gs-u-display-block::text').extract_first()
        # Get Results of the Home Team
        results_home = response.css('li.gs-o-list-ui__item.gs-u-pb- span.sp-c-fixture__team.sp-c-fixture__team--home')
        # Get Results of the Home Away
        results_away = response.css('li.gs-o-list-ui__item.gs-u-pb- span.sp-c-fixture__team.sp-c-fixture__team--away')
        # Iterate all the results
        for result_home, result_away in zip(results_home, results_away):
            team_home = result_home.css('span.sp-c-fixture__team-name.sp-c-fixture__team-name--home span span::text').extract_first()
            team_home_result = result_home.css('span.sp-c-fixture__block span::text').extract_first()
            team_away = result_away.css('span.sp-c-fixture__team-name.sp-c-fixture__team-name--away span span::text').extract_first()
            team_away_result = result_away.css('span.sp-c-fixture__block span::text').extract_first()
            yield{'Date': str(year) + ' ' + str(month), 'Home Team': team_home, 'Home Result': team_home_result, 'Away Result': team_away_result, 'Team Away': team_away}

            
            