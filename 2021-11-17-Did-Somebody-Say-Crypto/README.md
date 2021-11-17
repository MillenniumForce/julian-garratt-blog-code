# Read Me

## Assumptions

* Docker is pre-installed
* User has a Twitter Bearer token ([apply here](https://developer.twitter.com/en/apply-for-access))

## Running spark cluster

Go to the folder where the docker-compose file is in and run in a terminal:
`docker-compose up`  
If there are no failures you should be able to find the url to the jupyter lab session which can be opened in a browser.

## Run streamMessenger.py

First copy your Bearer token and paste where specified in line 9 of twitterStreamMaster.py. Now run using `python streamMessenger.py`

## Run twitterStreamMaster.py

Ensure that you've first run streamMessenger.py and the terminal has printed "Waiting for connection...". Next use `spark-submit twitterStreamMaster.py` to run the program

## Run csvCombineTool.py

Once you've collected a sufficient amount of tweets you can stop both programs using Ctrl-C. To combine all csv files in the 'sentiment' directory use the csv combine tool by running `python csvCombineTool.py`.

## Sample Output

Find sample output in twitterStreamSentimentSample.csv

## Contact Me

If you find any bugs, improvements or need additional help, get in contact with me at Julian Garratt on Facebook.
