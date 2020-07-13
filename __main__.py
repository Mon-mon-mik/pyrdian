#!/usr/bin/python3

import argparse
import datetime
import feedparser
import sys


def getArticles(URL):

	'''
	Parses the feed in RSS format

	Args:
		URL (str): Web address

	Returns:
		articles: The list of retrieved articles parsed to a list of Python dict
	'''

	try:
		NewsFeed = feedparser.parse(URL)
	except Exception as e:
		print(e, file=sys.stderr)
		sys.exit(1)

	articles = []

	for news in NewsFeed.entries:

		article = {}

		article['title'] = news.title
		article['link'] = news.link
		try:
			day, month, year = news.published[5:16].split()
			day = int(day)
			month = {
				'jan': 1,
				'feb': 2,
				'mar': 3,
				'apr': 4,
				'may': 5,
				'jun': 6,
				'jul': 7,
				'aug': 8,
				'sep': 9,
				'oct': 10,
				'nov': 11,
				'dec': 12
			}[month.lower()]

			article['date'] = year + '-' + \
				'{:02d}'.format(month) + '-' + '{:02d}'.format(day)

		except Exception as e:
			print(e, file=sys.stderr)
			article['date'] = ""
		try:
			article['tags'] = [item['term'] for item in news.tags]
		except Exception as e:
			print(e, file=sys.stderr)
			article['tags'] = []

		articles.append(article)

	return articles


def printArticles(articles, count=None, newest=None, oldest=None,
				  sort=None, show_tags=None, tags=None, show_title=None, show_url=None, show_date=None):

	'''
	Prints the list of articles and selected details

	Args:
		count (int): Show no more than count articles
		newest (bool): Sort articles by newest to oldest
		oldest (bool): Sort articles by oldest to newest
		sort (bool): Sort articles in alphabetical order, from A to Z?
		show_tags (bool): Show tags
		tags (list): Show articles with at least one tag from the list 'tags'
		show_title (bool): Show titles
		show_url (bool): Show links
		show_date (bool): Show publish dates
		
	Returns:
		None
	'''

	color = {
		'title': '\033[0;31m',
		'link' : '\033[0;32m',
		'date' : '\033[0;33m',
		'tags' : '\033[0;34m'}

	defaultColor = '\033[0m'

	if tags is not None:
		if tags:
			articles = [x for x in articles if set(x['tags']).intersection(set(tags))]
	if sort:
		articles = sorted(articles, key=lambda x: x['title'])
	if newest:
		articles = sorted(articles, key=lambda x: x['date'])
	if oldest:
		articles = sorted(articles, key=lambda x: x['date'], reverse=True)
	if count is not None:
		articles = articles[0:min(count, len(articles))]

	for article in articles:
		if show_title:
			print(color['title'] + article['title'] + defaultColor)
		if show_url:
			print(color['link'] + article['link'] + defaultColor)
		if show_date:
			print(color['date'] + article['date'] + defaultColor)
		if show_tags:
			print(color['tags'] + ' '.join(['#' + tag for tag in article['tags']]) + defaultColor)



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='If you do not give any argument from list: -t, --show title, - u, --show url, -D, --show tags, -d, --show date, all values are printed')
	parser.add_argument('-c', '--count', type=int,
						help='show no more than count articles')
	parser.add_argument('-t', '--show-title',
						action='store_true', help='show titles')
	parser.add_argument('-u', '--show-url',
						action='store_true', help='show links')
	parser.add_argument('-s', '--sort', action='store_true',
						help='sort articles in alphabetical order, from A to Z')
	parser.add_argument('-n', '--newest', action='store_true',
						help='sort articles by newest to oldest')
	parser.add_argument('-o', '--oldest', action='store_true',
						help='sort articles by oldest to newest')
	parser.add_argument('-D', '--show-tags',
						action='store_true', help='show tags')
	parser.add_argument('-T', '--tags', nargs='+',
						help='show articles with at least one tag from the list')
	parser.add_argument('-d', '--show-date',
						action='store_true', help='show publish dates')

	args = parser.parse_args()

	if args.newest and args.oldest:
		print('Error', file=sys.stderr)
		sys.exit(1)
	if args.count is not None:
		if args.count < 1:
			print('Error', file=sys.stderr)
			sys.exit(1)

	URL = 'https://www.theguardian.com/international/rss'
	articles = getArticles(URL)

	if not any([args.show_title, args.show_url, args.show_date, args.show_tags]):
		args.show_title = True
		args.show_url = True 
		args.show_date = True
		args.show_tags = True

	printArticles(articles,
				  count=args.count,
				  newest=args.newest,
				  oldest=args.oldest,
				  sort=args.sort,
				  show_tags=args.show_tags,
				  tags=args.tags,
				  show_title=args.show_title,
				  show_url=args.show_url,
				  show_date=args.show_date)
