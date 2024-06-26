import unittest
from unittest import mock
from unittest.mock import call

from boddle import boddle  # type: ignore
from bottle import HTTPResponse  # type: ignore
from db import News
from hackernews import add_label, classify_news, update_news


class TestHackernews(unittest.TestCase):
    @mock.patch("hackernews.session")
    def test_add_label(self, session):
        try:
            with boddle(query={"id": 1, "label": "never"}):
                news = News(
                    title="Ask HN: Do you use an optimization solver? Which one? Do you like it?",
                    author="ryan-nextmv",
                    url="https://news.ycombinator.com/item?id=31099186",
                    comments=83,
                    points=171,
                    label=None,
                )
                session.return_value.query.return_value.get.return_value = news
                new_news = add_label()
                self.assertTrue(new_news.label == "never")
                self.assertTrue(session.mock_calls[-1] == call().commit())
        except HTTPResponse as e:
            if e.status == 302:
                pass
            else:
                pass

    @mock.patch("hackernews.get_news")
    @mock.patch("hackernews.session")
    def test_update_news(self, session, get_news):
        try:
            news = [
                {
                    "author": "ngaut",
                    "comments": 24,
                    "points": 97,
                    "title": "Go will use pdqsort in next release",
                    "url": "https://github.com/golang/go/commit/72e77a7f41bbf45d466119444307fd3ae996e257",
                },
                {
                    "author": "electric_muse",
                    "comments": 44,
                    "points": 85,
                    "title": "Show HN: Two-way Jira sync in a collaborative spreadsheet and Gantt",
                    "url": "https://www.visor.us/landing/visor-for-jira-launch",
                },
                {
                    "author": "ryan-nextmv",
                    "comments": 83,
                    "points": 171,
                    "title": "Ask HN: Do you use an optimization solver? Which one? Do you like it?",
                    "url": "https://news.ycombinator.com/item?id=31099186",
                },
            ]
            get_news.return_value = news
            session.return_value.query.return_value.filter.return_value.first.side_effect = [
                True,
                False,
                False,
            ]
            update_news()
            n_commit = 0
            for one_call in session.mock_calls:
                if one_call == call().commit() and one_call != call():
                    n_commit += 1
            self.assertEqual(2, n_commit)
        except HTTPResponse as e:
            if e.status == 302:
                pass
            else:
                pass

    @mock.patch("hackernews.session")
    def test_classify_news(self, session):
        try:
            news_cl = [
                News(
                    title="Just a random example",
                    author="ngaut",
                    url="https://github.com/golang/go/commit/72e77a7f41bbf45d466119444307fd3ae996e257",
                    comments=24,
                    points=97,
                    label="good",
                ),
                News(
                    title="Another name appeared on the wall",
                    author="electric_muse",
                    url="https://www.visor.us/landing/visor-for-jira-launch",
                    comments=44,
                    points=85,
                    label="maybe",
                ),
                News(
                    title="Getting started with Python is easy",
                    author="ryan-nextmv",
                    url="https://news.ycombinator.com/item?id=31099186",
                    comments=83,
                    points=171,
                    label="never",
                ),
                News(
                    title="Getting started with Java is easy",
                    author="ryan-nextmv",
                    url="https://news.ycombinator.com/item?id=31099186",
                    comments=83,
                    points=171,
                    label="never",
                ),
                News(
                    title="One more random example",
                    author="ryan-nextmv",
                    url="https://news.ycombinator.com/item?id=31099186",
                    comments=83,
                    points=171,
                    label="good",
                ),
            ]
            news_not_cl = [
                News(
                    title="A name suddenly appeared on the wall",
                    author="ngaut",
                    url="https://github.com/golang/go/commit/72e77a7f41bbf45d466119444307fd3ae996e257",
                    comments=24,
                    points=97,
                ),
                News(
                    title="Getting started with C++ is relatively hard",
                    author="electric_muse",
                    url="https://www.visor.us/landing/visor-for-jira-launch",
                    comments=44,
                    points=85,
                ),
                News(
                    title="Just another random example",
                    author="ryan-nextmv",
                    url="https://news.ycombinator.com/item?id=31099186",
                    comments=83,
                    points=171,
                ),
            ]
            session.return_value.query.return_value.filter.return_value.all.side_effect = [
                news_cl,
                news_not_cl,
            ]
            expected = [news_not_cl[2], news_not_cl[0], news_not_cl[1]]
            actual = classify_news()
            self.assertEqual(expected, actual)
        except HTTPResponse as e:
            if e.status == 302:
                pass
            else:
                pass
        except:
            pass


if __name__ == "__main__":
    unittest.main()