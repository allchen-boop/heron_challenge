# heron_challenge

file overview:
- function.py will hold the implementation to the challenge
- brainstorm.ipynb will be where I brainstorm (easier for me to track and visualize my ideas)
- tests folder
- download dependencies on local env by installing requirements.txt

on mac os
pip3 install pandas
pip3 install matplotlib

to think about if more time:
1. what happens if we cancel a subscription and repurchase it again -- how do customers want to categorize that
2. what if a reccuring payment is done in two parts
3. how much do customers want to weight diff features

approach outline in brainstorm.ipynb

## adding this in overtime ##

ran out of time to wrap in API framework. if more time would:
1. make a flask app
2. api endpoint to get the json data. we read transactions from request


references used:
regex: https://developers.google.com/edu/python/regular-expressions
computing deltas: https://docs.python.org/3/library/difflib.html
pandas time date: https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html

didn't get to:
1. write more tests
2. get imports in requirements.txt
3. figure out a threshold for time delta based on deviation vals
4. get rid of print

basic outline (if notebook is hard to follow):
1. identify possible recurring based on amount -- operate under assumption that any single value can not be a recurring transaction
2. eliminate transactions of unique amount
3. group descriptions based on similarity
4. idenitfy grouping ranges to calculate time delta
5. mark time delta as 0 (when consecutive transactions occur at around the same time date weekly, monthly, yearly)
6. we are left with a list of the transactions that are flagged as recurring

if more time based on what i have now (besides looking into ml, nlp algos):
give score for each feature. rough example:
1. if there are any outlier amounts give it zero points.
2. if similarity score is 1 give it 10 points. if it is 0.6 give it 5. etc...
3. if time deltas are exactly the same wihtin a cluster give it 10 points, etc...
4. calculate ending points and classify if definately recurring, maybe, or most likely not

think more about ordering of classifications:
1. we could group by desc first and then investigate amounts within each grouping -- i just got rid of outlying amounts first for the sake of time. also, im assuming that amounts are the least variable to differences in recurring payments (a recurring payment should not have wildy diff amounts each month?)
2. again, this goes to how the client wants to define recurring based on how their transaction data is


1. How would you measure the accuracy of your approach? -- feedback so customers can confirm or reject those flagged as recurring
3. How would you know whether solving this problem made a material impact on customers? -- how often they use recurring feature
4. How would you deploy your solution? -- cicd for testing and deployment. put in container?
5. What other approaches would you investigate if you had more time?
   customers can define their own rules for identifying recurring transactions. option to weight how heavily each feature plays in determining recurrence.
   increase accurency with ML models -- use time series algo? others to research




