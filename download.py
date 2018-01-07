import pandas as pd
import tweepy

consumer_key = "x7XOywj3rgsSKn9MXkBNBpecr"
consumer_secret = "o4lHJPQQyVGQaojTGPTHR9BOXuEzvRzbghBkPMrAyaBoPRQjvd"

access_key = "3994061302-XFnBADeFR4WBxZzmXAy4sXn2sSHu6aYldjZgbVk"
access_secret = "g4FCmePHacsvv7nJOp2sJRaY9nbnH556s97whuOKILFrI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_all_tweets(screen_name):
    alltweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))

    data = [
        [obj.user.screen_name, obj.user.name, obj.user.id_str, obj.user.description.encode("utf8"), obj.created_at.year,
         obj.created_at.month, obj.created_at.day, "%s.%s" % (obj.created_at.hour, obj.created_at.minute), obj.id_str,
         obj.text.encode("utf8")] for obj in alltweets]
    dataframe = pd.DataFrame(data, columns=['screen_name', 'name', 'twitter_id', 'description', 'year', 'month', 'date',
                                            'time', 'tweet_id', 'tweet'])
    dataframe.to_csv("%s_tweets.csv" % (screen_name), index=False)


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("TimesNow")