from flair.models import TextClassifier
from flair.data import Sentence


def get_review_sentement(reviews):
    """
    Given a list of reviews, uses flair positive sentiment classification to assign each review a positivity score.
    The entire title and body are run through the classifier at once so that sentences that are neutral don't bring down the average score.
    Returns a tuple of the review and its positivity score sorted in descending order.

    return tup(dict, float)
    """

    classifier = TextClassifier.load('en-sentiment')
    scored_reviews = []
    for review in reviews:
        text = review['title'] + ' ' + review['body']
        sentence = Sentence(text)
        classifier.predict(sentence)
        scored_reviews.append((review, sentence.labels[0].score))

    return sorted(scored_reviews, key=lambda x: float(x[1]), reverse=True)
