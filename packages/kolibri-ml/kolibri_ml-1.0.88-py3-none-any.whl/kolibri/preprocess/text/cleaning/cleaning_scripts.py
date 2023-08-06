import pandas as pd
import regex as re
from kdmt.text import clean_text

def fix_formating(text):
    text=str(text)
    text = text.replace(u'\\xa333', u' ')
    text = text.replace(u'\\u2019', u'\'')
    text = text.replace(u' B7; ', '')
    text = text.replace(u'\\xb4', u'\'')
    text = text.replace(u'\\xa0', u' ')
    text = text.replace(u'\\xa0', u' ')
    text = text.replace(u'f\\xfcr', u'\'s')
    text = text.replace(u'\\xa', u' x')
    text = text.replace(u'_x000D_', u'\n')
    text = text.replace(u'x000D', u'\n')
    text = text.replace(u'.à', u' a')
    text = text.replace(u' ', u'')
    text = text.replace(u'‎', u'')
    text = text.replace(u'­', '')
    text = text.replace(u'﻿', u'')
    text = text.replace('&nbsp;', u'')
    text = text.replace('&#43;', '')
    text = text.replace('&lt;', '<')
    text = text.replace('&quot;', '"')
    text = text.replace('&gt;', '>')
    text = text.replace('ï»¿', '')
    text = text.replace('...', '.')
    text = text.replace('..', '.')
    text = text.replace(' .', '. ')
    text = text.replace('\r\n', '\n')
    text = text.replace('\xa0', ' ').replace('：', ': ').replace('\u200b', '').replace('\u2026', '...').replace('’', "'")
    text = text.replace('...', '.')
    text = text.replace('..', '.')
    text = re.sub(r':\s+', ': ', text)
    #    text = text.replace('\\r', '. ')
    text = text.replace(' .', '. ')
    text = re.sub(r':\s?\.', ':', text)

    return text.strip('\n').strip().strip('\n')


def clean(text, remove_html=True, email_forward=True):
    if remove_html:
        text = re.sub(r"(<|\[)https?:\/\/.*(\.).*(>|\])", "", text, 0, re.M)
        text = re.sub(r'[#@>\?\/\*^\'\<\!\[\(\)\w:="\.;\|\&, %\]0-9\s-]+\{[\s\w:@;\!\.%\'",\\=#\s\/*>-]*\}', '', text,0, re.MULTILINE)
        text = re.sub(r'[#@>\?\/\*^\'\<\!\[\(\)\w:="\.;\|\&, %\]0-9\s-]+\{[\s\w:@;\!\.%\'",\\=#\s\/*>-]*\}', '', text, 0, re.MULTILINE)
    text= fix_formating(text).strip()
    text=re.sub(r"\[cid:.*\]", "", text, 0, re.MULTILINE)

    if email_forward:
        text = re.sub(r"^>+[ ]*", "", text, 0, re.MULTILINE)
    return text


if __name__ == '__main__':

    df=pd.read_excel("/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/examples/email_data.xlsx")
    df['body']=df['body'].apply(clean)

    df.to_excel("email_data_clean.xlsx")

