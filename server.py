# Paste your python program here
import datetime
import pickle
import re
import nltk
import pandas as pd
from instaloader import Instaloader, Profile
from nltk import word_tokenize
from spacy.lang.en import English
import gspread
nltk.download('punkt')
gc = gspread.service_account(filename='data/sheets-json-secret-key.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1U3gypkEa3Qjbf4f5w3zFFEm5P4_Jfkble3zsyg6Isc4/edit?usp=sharing')

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
pipeline.predict(['good'])
L = Instaloader()

start_date = datetime.date(year=2020, month=8, day=1)
end_date = datetime.date(year=2020, month=8, day=31)
# TODO: CHANGE HANDLE TO THE ONE ASSIGNED TO YOU
df = pd.read_csv('data/Page Rank Handles.csv', encoding='cp1252')
handles = df['Insta Handle'].dropna().tolist()
print("yo")
rows = []
comments = []
for handle in handles:
    print(handle)
    profile = Profile.from_username(L.context, handle)
    num_followers = profile.followers
    total_likes = 0
    total_comments = 0
    pos_comments = 0
    neg_comments = 0
    total_posts = 0
    for post in profile.get_posts():
        if end_date < post.date_utc.date():
            continue
        if post.date_utc.date() < start_date:
            break
        print(total_posts)
        total_likes += post.likes
        total_comments += post.comments

        getcomments = list(post.get_comments())
        all_comments = 0
        good_comments = 1
        while good_comments <= 1000 and all_comments < len(getcomments):
            comment = getcomments[all_comments]
            clean_comment = cleaning(comment.text)
            all_comments += 1
            if clean_comment != '':
                # calculate senti
                good_comments += 1
                comments.append([handle, comment.text])
                senti = pipeline.predict([clean_comment])[0]
                if senti == 4:  # positive
                    pos_comments += 1
                elif senti == 0:  # negative
                    neg_comments += 1
        total_posts += 1
    # print(handle, total_likes, pos_comments, neg_comments, total_comments, total_posts, num_followers)
    rows.append([handle, total_likes, pos_comments, neg_comments, total_comments, total_posts, num_followers])
insta = pd.DataFrame(rows,
                     columns=['handle', 'total_likes', 'pos_comments', 'neg_comments', 'total_comments', 'total_posts',
                              'num_followers'])
comments_df = pd.DataFrame(comments, columns=['handle', 'comment'])
# insta.to_csv(''.join(handles) + '_insta.csv', index=False)
# comments_df.to_csv(''.join(handles) + '_insta_comments.csv', index=False)
# TODO: WILL SAVE TO CSV
worksheet = sh.get_worksheet(0)

worksheet.update([comments_df.columns.values.tolist()] + comments_df.values.tolist())
worksheet = sh.get_worksheet(1)

worksheet.update([insta.columns.values.tolist()] + insta.values.tolist())
