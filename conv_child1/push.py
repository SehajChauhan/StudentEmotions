from psaw import PushshiftAPI
import boto3
import json
import datetime as dt

api = PushshiftAPI() #invokes api

def redditposts(post_id, submission):
#creates a dictionary containing post data.
    data = {
                submission.id : {
                    "author": submission.author,
                    "title": submission.title,
                    "body": submission.selftext,
                    "url": submission.url,
                    "date_created": submission.created,
                    "subreddit": submission.subreddit,
                    "subreddit_subscribers": submission.subreddit_subscribers,
            }
        }
    for k, v in data[submission.id].items():
        if v == None:
            data[k] = "None"
    return data

def redditcomments(_id, comment):
#creates a dictionary containing comment data.
    data = {
                    comment.id : {
                        "article_id": comment.link_id,
                        "parent_id": comment.parent_id,
                        "author": comment.author,
                        "body": comment.body,
                        "date_created": comment.created,
                        "subreddit": comment.subreddit
                        }
                    }
    for k, v in data[comment.id].items():
        if v == None:
            data[k] = "None"
    return data


def reddit_lister(submissions, comments):
#fill lists with scraped data.
    articles = {}
    commenters = {}
    for submission in submissions:
        post_id = submission.id
        article = redditposts(post_id, submission)
        article[post_id]['subreddit'] = str(submission.subreddit)
        articles.update(article)

        for comment in comments:
            _id = hash(comment.body)
            comment2 = redditcomments(_id, comment)
            commenters.update(comment2)

    return articles, commenters


def sub_data(submissions, comments):
    articles, commenters = reddit_lister(submissions, comments)
    return articles, commenters


def savedata(sub, submissions, comments):
#saves the data in JSON format and uploads the files to amazon S3 buckets.
    try:
        s3 = boto3.resource('s3')
        now = dt.datetime.utcnow()
        formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
        articles, commenters = sub_data(submissions, comments)
        if hasattr(savedata, "acounter"):
            savedata.acounter+=1
        else:
            savedata.acounter=0

        if hasattr(savedata, "ccounter"):
            savedata.ccounter+=1
        else:
            savedata.ccounter=0

        print("Number of articles, commenters {}, {}".format(len(articles), len(commenters)))
        articles_name = '2019/articles/' + sub + "/" + str(savedata.acounter) + '_articles.json'
        commenters_name = '2019/commenters/' + sub + "/" + str(savedata.ccounter) + '_commenters.json'
        object = s3.Object('convscraper', articles_name)
        object.put(Body=json.dumps(articles))
        print("Finished writing articles to {}".format(articles_name))
        object = s3.Object('convscraper', commenters_name)
        object.put(Body=json.dumps(commenters))
        print("Finished writing commenters to {}".format(commenters_name))
    except AttributeError:
        pass
        
def lambda_handler(x, y):
#configure lambda to run the scraping process on several subreddits after regular intervals of time.

     monthstarter = x['monthstarter']
     monthstopper = x['monthstopper']
     subredditer = x['subredditer']

     import time
     start = time.time()

     for i in range(len(subredditer)):

         sub = subredditer[i]
         start_time = int(dt.datetime(2019, monthstarter, 1).timestamp()) #timestamp to start scraping
         stop_time = int(dt.datetime(2019, monthstopper, 1).timestamp()) #timestamp to stop scraping

         submissions = list(api.search_submissions(after=start_time, before=stop_time,
                                                           subreddit= subredditer[i], limit=2000))
         comments = list(api.search_comments(after=start_time, before=stop_time,
                                                          subreddit= subredditer[i], limit=9000))

         savedata(sub, submissions, comments)
         print("="*50)

     end = time.time()
     print("Elapsed time {}".format(end - start))

'''
#for manual execution from local machine.
if __name__ == "__main__":
     import time
     start = time.time()
     for i in range(len(subreddits)):
         sub = subreddits[i]

         start_time = int(dt.datetime(2019, 2, 1).timestamp()) #timestamp to start scraping
         stop_time = int(dt.datetime(2019, 3, 1).timestamp()) #timestamp to stop scraping

         submissions = list(api.search_submissions(after=start_time, before=stop_time,
                                                       subreddit= subreddits[i], limit=2500))
         comments = list(api.search_comments(after=start_time, before=stop_time,
                                                      subreddit= subreddits[i], limit=10000))

         savedata(sub, submissions, comments)
         print("="*50)

     end = time.time()
     print("Elapsed time {}".format(end - start))
'''
