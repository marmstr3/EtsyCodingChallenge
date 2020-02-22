# EtsyCodingChallenge
## --- REQUIREMENTS ---
In order to run this program, you need to have **Python 3.6.7** with the 
requests **2.22.0** module installed. Compatibility with other versions
of Python cannot be guaranteed.

## --- RUNNING THE PROGRAM ---
This program can be ran in two ways. You can open the file from your 
OS's file explorer running main.py with the Python Launcher. This
should bring up a command line or bash interface for the program.
You can also run the program by navigating to the folder where you
saved main.py in your command line or bash interface. From there, 
type **python main.py**. This should run the
program from your command line or bash interface.

## --- DESCRIPTION ---
This program uses the Etsy API to analyze the top 5 words used by a
shop. The program starts by analyzing a predetermined set of 10 Etsy
shops. After this initial analysis, the user is able to analyze a
specific shop by entering the shop's name as it appears in the Etsy
URL for that shop.

## --- ANALYSIS ALGORITHM ---
The algorithm used to identify the top 5 terms for each Etsy shop is
a simple word count algorithm, filtered by a stop word list. A stop
word is Natural Language Processing concept. Stop words are words
that appear at a much higher rate in a language without providing 
insight into the context of the text. Below is the list of stop words
used for this analysis. Individual letters are also filtered out. 
  
['THE', 'BUT', 'AN', 'AND', 'ARE', 'AS', 'AT', 'BE', 'BY', 'FOR',
'FROM', 'HAS', 'HAD', 'IF', 'IN', 'IS', 'IT', 'ITS', 'NO', 'OF', 'ON',
'OR', 'OUR', 'THAT', 'TO', 'WAS', 'WERE', 'WILL', 'WITH', 'YOU', 
'YOUR', 'I', 'ME', 'MINE', 'MY', 'THIS', 'YES']

## --- ASSUMPTIONS ---
This program assumes that we are only concerned with current listings.
This assumption was made because old listings may not be reflective of
the shop's current type of products.


## --- POTENTIAL IMPROVEMENTS ---
- The API calls tend to take a long time to get a response (a little over
1 second when tested). This leads to the 10 shop analysis taking over
10 seconds to run, which is not ideal. This runtime could be brought
down by an order of magnitude by adding multi-threading and running
all 10 shop anlyses in parallel. 

- A dictionary of known singular-plural pairs could be used to identify
when the plural form of a word is being used, and counting that just
as a use of the singular form. This would prevent the same word showing
up twice in the analysis due to the plural form being used often, and 
would prevent words that are used more often but in an even mix of
plural and singular forms from being missed by the analysis.

- Future functionality to allow users to analyze multiple shops at a time
and to determine how many top terms per shop they want listed could be 
added. The get_top_n_counts method and the get_shops_and_listings method
both are already designed to allow for this functionality. The UI would
need to be modified to allow for the user to input that info upon request. 
