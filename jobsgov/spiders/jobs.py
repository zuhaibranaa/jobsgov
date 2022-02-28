import scrapy
import requests
import re
from ..items import JobsgovItem
class jobs(scrapy.Spider):
	name = 'jobs'
	end_page = None
	start_page = input('Enter Your Start Range :  ')
	dump = input('Do You Want To Using End Limit [Y/N] :  ')
	if dump[0].upper() == 'Y':
		end_page = int(input('Enter Your End Range :  '))
	start_urls = ['https://www2.jobs.gov.hk/0/en/JobSeeker/jobsearch/joblist/?page='+start_page]
	curr_page = int(start_page)
	def parse(self, response):
		self.curr_page+=1
		cards = response.css('.jobseeker_grid_row')
		for card in cards:
			url = card.css('.flex-column span:nth-child(2) a::attr(href)').get()
			yield scrapy.Request(response.urljoin(url), callback=self.parse2)
		if self.end_page is None:
			yield scrapy.Request(
                    response.urljoin('https://www2.jobs.gov.hk/0/en/JobSeeker/jobsearch/joblist/?page='+str(self.curr_page)),
                    callback=self.parse
                )
		else:
			if self.curr_page <= self.end_page: # Check Page Limit Described
				yield scrapy.Request(
                        response.urljoin('https://www2.jobs.gov.hk/0/en/JobSeeker/jobsearch/joblist/?page='+str(self.curr_page)),
                        callback=self.parse
                    )

	def parse2(self, response):
		item = JobsgovItem()
		order_no = response.css('#ordNo::text').get().split()[0]
		emp_name = response.css('#empName::text').get()
		temp = response.css('#postedDt::text').get().split('/')
		posted_date = temp[-1]+'-'+temp[-2]+'-'+temp[-3]
		job_title = response.css('#jobTitle::text').get()
		info = response.css('#openupRemark::text').get()
		name = [i for i in re.findall("([A-Z][A-Z]+)", info) if i not in re.findall("([A-Z][A-Z]+)", emp_name)]
		temp = ""
		for i in range(len(name)):
			if i == 0 and name[i][i] != 'M':
				i+=1
			temp+=name[i]+" "
		name = temp
		email = info[info.find('l(')+2:]
		if(email.find('@') > 0):
			email = email[:email.find(')')]
		else:
			email = None
		number = [i for i in re.findall("([0-9][0-9]+)", info)]
		if len(number) == 0:
			number = None
		elif len(number) == 1:
			number = number[0]
		else:
			number = number[-1]
		if number is not None and len(number) < 8 :
			number = None

		item['_id'] =  order_no
		item['company'] = emp_name
		item['email'] = email
		item['phone'] = number
		item['person'] = name
		item['day'] = posted_date
		item['title'] = job_title
		item['link'] = response.request.url

		yield item