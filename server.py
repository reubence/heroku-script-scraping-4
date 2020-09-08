# Paste your python program here
from apiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
# TODO: CHANGE TO YOUR OWN API
DEVELOPER_KEY = "AIzaSyCxx5KJAIbRw81BVA8eukEc9oyhVbXBwXg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

gc = gspread.service_account(filename='data/sheets-json-secret-key.json')
sh = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/15dA7G6TQozLCQHC6_42aJFz7gmid06Ktm4cRKUn90xs')

# start_date = datetime(year=2020, month=8, day=1, tzinfo=timezone.utc).astimezone()
# end_date = datetime(year=2020, month=8, day=31, tzinfo=timezone.utc).astimezone()
# start_date = start_date.isoformat("T") + "Z"
# end_date = end_date.isoformat("T") + "Z"

time1 = '2020-06-01T00:00:00Z'
time2 = '2020-06-15T00:00:00Z'
time3 = '2020-06-30T00:00:00Z'

import pickle
import pandas as pd
import re
from spacy.lang.en import English
from nltk import word_tokenize

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

emoticons_sad = {':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/',
                 '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('}

emoticons_happy = {':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D',
                   '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)",
                   ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b',
                   '>:)', '>;)', '>:-)', '<3'}

emoticons = emoticons_happy.union(emoticons_sad)

stop_words = ['PRON', '15', 'in', 'the', 'and', 'of', 'to', 'is', 'in', 'it', 'this', 'that', 'was', 'as', 'movie',
              'for', 'with', 'but', 'be', 'film', 'on',
              'have', 'his', 'he', 'do', 'all', 'at', 'you', 'are', 'your', 'one', 'all', 'by', 'me', 'my', 'myself',
              'we', 'our', 'ours', 'yours', 'yourself', 'yourselves',
              'has', 'an', 'who', 'they', 'so', 'from', 'there', 'or', 'just', 'her', 'hers', 'out', 'about', 'if',
              'him', 'himself', 'she', 'herself', 'it', 'its', 'itself',
              'them', 'their', 'what', 'can', 'some', 'would', 'could', 'when', 'more', 'very', 'up', 'will', 'time',
              'even', 'which', 'only', 'story', 'really', 'whom',
              'these', 'those', 'see', 'had', 'were', 'then', 'much', 'get', 'been' 'other', 'people', 'also', 'into',
              'because', 'how', 'am', 'is', 'are', 'was', 'were', 'be',
              'been', 'being', 'having', 'do', 'does', 'did', 'doing', 'too', 'than', 'other', 'first', 'most', 'make',
              'made', 'way', 'movies', 'any', 'after', 'characters',
              'an', 'plot', 'life', 'acting', 'where', 'think', 'seen', 'films', 'two', 'many', 'seen', 'having', 'do',
              'does', 'did', 'doing', 'until', 'while', 'of', 'watch',
              'character', 'show', 'know', 'little', 'over', 'off', 'ever', 'man', 'woman', 'scenes', 'why', 'end',
              'here', 'there', 'still', 'should', 'before', 'after', 'above',
              'below', 'between', 'into', 'through', 'during', 'to', 'from', 'up', 'down', 'further', 'then', 'in',
              'out', 'again', 'once', 'any', 'both', 'few', 'over', 'under',
              'then', 'once', 'same', 'so', 'can', 'will', 'could', 'thing', 'say', 'go', 'something', 'back', 'just',
              'actors', 'director', 'actor', 'actress']

nlp = English()
tokenizer = nlp.Defaults.create_tokenizer(nlp)


def cleaning(text):
    text = str(text)
    text = text.lower()  # lower case
    # text = text.replace(u'\U0001F494', "sad")
    text = ' '.join([w for w in text.split() if w not in emoticons])
    text = re.sub("&amp;", 'and', text)
    text = re.sub(r'<[^>]+>', '', text)  # html tags
    text = ' '.join(re.sub("(#[A-Za-z0-9_]+)|(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    text = re.sub(r'\b(http|https):\/\/.*[^ alt]\b', '', text)  # html link remove
    text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)  # numbers
    tokens = tokenizer(text)
    lemma_list = []
    for token in tokens:
        lemma_list.append(token.lemma_)  # lemmas
    text = ' '.join(lemma_list)
    text = re.sub(r'\b\w{1}\b', '', text)
    # text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)  # PUNCTUATIONS
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    # lemmatize_words = np.vectorize(lem.lemmatize , otypes=[str])
    filtered_sentence = ' '.join(filtered_sentence).strip()

    return filtered_sentence


cleaning('Yay the cleaning PiPeline works!! :D #yebish')


####
url = "https://www.dropbox.com/s/manoypretrz3sq8/pipeline.sav?dl=1"  # dl=1 is important
import urllib.request

u = urllib.request.urlopen(url)
data = u.read()
u.close()

with open('data/model.sav', "wb") as f:
    f.write(data)
####


pipeline = pickle.load(open('data/model.sav', 'rb'))
pipeline.predict(['bad'])[0]

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# TODO: CHANGE NAMES TO THOSE ASSIGNED TO YOU
names = ['Shreyas Talpade']
rows = []
comments_list = []
for name in names:
    print(name)
    videos = 0
    views = 0
    likes = 0
    dislikes = 0
    favorites = 0
    comments = 0
    pos_comments = 0
    neg_comments = 0
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response1 = youtube.search().list(q=name, part="id", maxResults=50, publishedAfter=time1,
                                             publishedBefore=time2, order='viewCount').execute()
    search_response2 = youtube.search().list(q=name, part="id", maxResults=50, publishedAfter=time2,
                                             publishedBefore=time3, order='viewCount').execute()

    # Add each result to the appropriate list, and then display the lists of matching videos, channels, and playlists.
    for search_result in search_response1.get("items", []) + search_response2.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videoId = search_result["id"]["videoId"]

            # Get video statistics
            video_response = youtube.videos().list(id=videoId, part="statistics").execute()
            videos += 1
            print(videos)
            for video_result in video_response.get("items", []):
                views += int(video_result["statistics"]["viewCount"])
                if 'likeCount' in video_result["statistics"]:
                    likes += int(video_result["statistics"]["likeCount"])
                if 'dislikeCount' in video_result["statistics"]:
                    dislikes += int(video_result["statistics"]["dislikeCount"])
                if 'commentCount' in video_result["statistics"]:
                    comments += int(video_result["statistics"]["commentCount"])
                if 'favoriteCount' in video_result["statistics"]:
                    favorites += int(video_result["statistics"]["favoriteCount"])

            # Get video comments
            try:
                response = youtube.commentThreads().list(videoId=videoId, part="snippet").execute()
            except HttpError:
                continue
            for result in response.get("items", []):
                comment = result['snippet']['topLevelComment']['snippet']['textOriginal']
                comments_list.append([name, comment])

                clean_comment = cleaning(comment)
                if clean_comment != '':
                    # calculate senti
                    senti = pipeline.predict([clean_comment])[0]
                    if senti == 'positive':  # positive
                        pos_comments += 1
                    elif senti == 'negative':  # negative
                        neg_comments += 1
    rows.append([name, videos, views, likes, dislikes, comments, pos_comments, neg_comments, favorites])
yt = pd.DataFrame(rows,
                  columns=['name', 'videos', 'views', 'likes', 'dislikes', 'comments', 'pos_comments', 'neg_comments',
                           'favorites'])
comments_df = pd.DataFrame(comments_list, columns=['handle', 'comment'])
# yt.to_csv('yt_july.csv', index=False)
# comments_df.to_csv('yt_july_comments.csv', index=False)

worksheet = sh.get_worksheet(0)

worksheet.update([comments_df.columns.values.tolist()] + comments_df.values.tolist())
worksheet = sh.get_worksheet(1)

worksheet.update([yt.columns.values.tolist()] + yt.values.tolist())

# TODO: WILL SAVE TO CSV


