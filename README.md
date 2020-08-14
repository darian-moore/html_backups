# HTML Backups with Selenium

Came into an issue where employees could edit sensitive information, so this program is used to create automatic daily backups, via
Windows Task Scheduler, of all important admin tab settings. At first I wanted to scrape all data and put it into a csv file, however 
this data needed to be easy to read for other non-technical employees. So, I opted to save all HTML data for each important 
admin tab and make it an HTML file instead. Some tabs take a while to show all content due to the drop down button load times, 
so I decided to implement multi-threading to decrease the amount of time the program takes to complete. After each thread is finished, 
the amount of time it took to finish that thread is displayed; same thing once the program finishes.
