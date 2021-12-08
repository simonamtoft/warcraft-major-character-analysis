import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

import random
import numpy as np
from typing import List, Tuple

import config

def standardize_comment(comment):
    return {
        'id': comment['id'],
        'body': comment['body'],
        'user': comment.get('user', comment.get('username')),
        'date': comment.get('date', comment.get('creationdate')),
        'rating': comment['rating'],
        'is_reply': comment.get('nreplies', 0) > 0
    }

def get_ts(df, breakdown_lookup, char_sentiments, char_data, params) -> List[Tuple[list, list]]:
    k,grps = breakdown_lookup[params['breakdown']]
    X = []
    Y = []
    for val in grps:
        grp_chars = list(df[df[k] == val].Name)
        points = []
        for char in grp_chars:
            for C in char_sentiments[char]:
                comment_id = C[0]
                data = char_data[char][comment_id]
                if params['replies'] and not data['is_reply']:
                    continue
                points.append({
                    'date': data['date'],
                    'score': data[params['metric']]
                })
        d = pd.DataFrame(points)
        d = d[d.date > datetime(2006,6,1)]
        d = d[d.date < datetime(2021,11,1)]
        d = d.resample(params['resample'], on='date')
        x = list(d.indices)
        if params['metric'] == 'count':
            y = list(d.score.count().dropna().values.astype('float64'))
        else:
            y = list(d.score.mean().dropna().values)
        X.append(x)
        Y.append(y)
    return X, Y
    

def plot_timeseries(params, breakdown_lookup, X, Y):    
    plt.figure(figsize=(12,5))
    k,grps = breakdown_lookup[params['breakdown']]
    for val,x,y in zip(grps, X,Y):
        plt.plot(x, y, 'o-', ms=9, linewidth=3, label=val)

    plt.title(
        'Wowhead comments %s by %s (%sreplies)' % (
            params['metric'].title().replace('_', ' '),
            k,
            'no ' if not params['replies'] else ''
        )
    )
    plt.ylabel(params['metric'].title().replace('_', ' '))
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_specific_comment(k, t, char_data, char_comments):
    for char_name,comment_data in random.sample(char_data.items(), len(char_data)):
        for comment_id, cd in comment_data.items():
            if cd[k] > t:
                comment = next(cc for cc in char_comments[char_name] if cc['id'] == comment_id)
                return cd['bert_sentiment'], cd['vader_sentiment'], comment['body']


def plot_comments_dist(df, char_data, params, breakdown_lookup):
    cs = pd.DataFrame.from_records(
        df.apply(
            lambda x: {
                **dict(x),
                **{ k: np.mean([v[k] for v in char_data[x.Name].values()]) for k in ['bert_sentiment', 'vader_sentiment'] },
            },
            axis=1
        )
    )

    plt.figure(figsize=(10,5))
    k, grps = breakdown_lookup[params['breakdown']]

    for val in grps:
        counts,bins = np.histogram(cs[cs[k] == val][params['metric']], density=True)
        x = 0.5 * (bins[1:] + bins[:-1])
        y = counts/counts.sum()
        plt.plot(x, y, 'o-', label=val, linewidth=3)

    plt.title('Wowhead Comments %s by %s' % (params['metric'].title().replace('_', ' '), k))
    plt.legend()
    plt.xlabel('%s' % params['metric'].title().replace('_', ' '))
    plt.ylabel('Cumulative Density')
    plt.show()


def plot_quote_dist(df, quote_sentiments, breakdown_lookup, params):
    qs = pd.merge(
        pd.DataFrame(quote_sentiments).groupby('char').mean().reset_index(),
        df,
        left_on='char',
        right_on='Name',
        how='inner'
    ).drop('char', axis=1)

    plt.figure(figsize=(10,5))
    k, grps = breakdown_lookup[params['breakdown']]

    for val in grps:
        counts,bins = np.histogram(qs[qs[k] == val][params['metric']], density=True)
        x = 0.5 * (bins[1:] + bins[:-1])
        y = counts/counts.sum()
        plt.plot(x, y, 'o-', label=val, linewidth=3)

    plt.title('Wiki Quotes %s by %s' % (params['metric'].title().replace('_', ' '), k))
    plt.legend()
    plt.xlabel('%s' % params['metric'].title().replace('_', ' '))
    plt.ylabel('Cumulative Density')
    plt.show()