# Tweet.Ly 

This is a text prediction application that uses 3 machine learning algorithms and scraped Twitter history to predict, w/ 96% accuracy, future user speech patterns.

This command-line application has two modes, analyze and compare. Analyze reports a users tweeting patterns and other fun statistics. Compare takes in a sample of text and a list of 2 or more users and predicts which user is most likely to say that tweet based on one of 3 machine learning algorithms, along with a similarity index. All input handled through command line. Requires Twitter developer account with access keys.

Framework is developed in Python using Tweepy API and twitter developer account. Initial steps were designing a scraping algorithm to process user tweets via Tweepy. Next steps were designing a machine-learning classification algorithm (NumPy/SciPy) using a Bayesian model and a multinomial random variable distribution to use a "Bag of Words" model. Simulations were run w/ 100,000 user tweets to test the accuracy of the model in many different categories. Next, two modern ML algorithms were developed, Naive Bayes and Logistic Regression. Accuracy was also tested for these models.

### Features:
- 3 ML prediction algorithms: Multinomial RV model, Naive Bayes, Logistic Regression
- 2 modes of analyzing scraped data
  - Analyze: Tweeting statistics and patterns for set of users
  - Compare: apply text predictionl algorithm to predict future speech patterns for users
- Reads up-to-date tweet data on each call for an automatically updating dataset
- Set number of tweets to base models from

### Usage
    python3 analzetweets.py -command [users...]

    arguments:
      command         the method of analysis, 'compare' or 'analyze'
      users           space delimited list of twitter handles (without @) (for compare mode)
      
### Libraries Used:
- Tweepy - handle twitter API and scraping
- NumPy/SciPy - mathematical analysis with large data sets, building classification models

### Set-Up:
- Requires twitter developer account w/ consumer key & access token (https://developer.twitter.com/en)
  - Replace lines 6-9 in authentication.py with developer account information
  - Adjust lines 23 in analyzetweets.py to specify the ML classifier to use
- Run analyzetweets.py in command line with specified parameters
    
### Most Recent Changes (06/12/20):
- Implemented 2 machine learning algorithms (Naive Bayes / Logistic regression)
- ML algorithm tester to test accuracy of new approaches
- New authentication file for simplifying twitter authentication
- More descriptive error messages
- Dramatic efficiency improvements - reduced tweet parsing from O(n^2) to O(n)
    - Improved efficiency of building dictionary by 2-fold

