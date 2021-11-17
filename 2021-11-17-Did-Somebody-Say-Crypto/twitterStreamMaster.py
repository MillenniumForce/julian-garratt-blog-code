from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


def main():

    # Initiate Spark Streaming Context
    spark = SparkSession \
        .builder \
        .appName("Twitter Streaming") \
        .getOrCreate()

    # Get Tweets
    rawTweets = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Preprocess and then estimate sentiment on stream
    cleanedTweets = rawTweets \
        .select(col('value').cast("string").alias("Tweets")) \
        .withColumn("Processed Tweets", process(col("Tweets"))) \
        .withColumn("Sentiment", getSentiment(col("Processed Tweets")))
    
    # Start stream and write to csv
    query = cleanedTweets \
        .writeStream \
        .format("csv") \
        .trigger(processingTime="10 seconds") \
        .option("checkpointLocation", "checkpoint/") \
        .option("path", "/opt/workspace/sentiment") \
        .outputMode("append") \
        .start()
    query.awaitTermination()

@udf(returnType=StringType())
def process(tweet):
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.corpus import stopwords

    # Clean tweet
    flatTweet = re.sub(r"\n", " ", tweet)
    refinedTweet = re.sub(r"@[\w]*|[^a-zA-Z#]|http[s]?://\S+", " ", flatTweet)
    
    # Tokenize
    tokens = word_tokenize(refinedTweet)

    # Run port stemmer
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    # Run word lammetizer
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Remove stopwords
    stopWords = set(stopwords.words("english"))
    tokens = [word for word in tokens if word.lower() not in stopWords]

    return " ".join(tokens)
    
@udf(returnType=StringType())
def getSentiment(tweet):
    vader = SentimentIntensityAnalyzer()
    sentiment = vader.polarity_scores(tweet)
    return str(sentiment) 

if __name__ == "__main__":
    nltk.download("vader_lexicon")
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    main()