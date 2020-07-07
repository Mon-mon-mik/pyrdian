#!/usr/bin/python3

import feedparser
import datetime
import sys
import argparse


def getArticles(URL):
	try:
		NewsFeed = feedparser.parse(URL)
	except Exception as e:
		print(e, file = sys.stderr)
		sys.exit(1)

	articles = []

	for news in NewsFeed.entries:

		article = {}

		article['title'] = news.title
		article['link']  = news.link
		try:
			day, month, year = news.published[5:16].split()
			day = int(day)
			month = {
					'jan' : 1,
					'feb' : 2,
					'mar' : 3,
					'apr' : 4,
					'may' : 5,
					'jun' : 6,
					'jul' : 7,
					'aug' : 8,
					'sep' : 9,
					'oct' : 10,
					'nov' : 11,
					'dec' : 12
			}[month.lower()]

			article['date'] = year +'-' + '{:02d}'.format(month) + '-' + '{:02d}'.format(day)
			
		except Exception as e:
			print(e, file = sys.stderr)
			article['date'] = ""
		try:
			article['tags'] = [item['term'] for item in news.tags]
		except Exception as e:
			print(e, file = sys.stderr)
			article['tags'] = []
		
		articles.append(article)

	return articles


def printArticles(articles, count=None, newest=None, oldest=None, 
	sort=None, show_tags=None, tags=None, show_title=None, show_url=None, show_date=None):

	color = {
		'title' :'\033[0;31m',
		'link'  : '\033[0;32m',
		'date'  : '\033[0;33m',
		'tags'  : '\033[0;34m' }
	

	defaultColor = '\033[0m'


	if tags is not None:
		if tags:
			articles = [article for article in articles if set(article['tags']).intersection(set(tags))]
	if sort:
		articles = sorted(articles, key=lambda x: x['title'])
	if newest:
		articles = sorted(articles, key=lambda x: x['date'])
	if oldest:
		articles = sorted(articles, key=lambda x: x['date'], reverse = True)
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
			if tags:
				for tag in tags:
					print(color['tags'] + "#" + article['tags'] + defaultColor)
			
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser() 
	parser.add_argument('-c', '--count', type=int, help='show max COUNT articles')
	parser.add_argument('-t', '--show-title', action='store_true', help='show titles')
	parser.add_argument('-u', '--show-url', action='store_true', help='show links')
	parser.add_argument('-s', '--sort', action='store_true', help='sort alphabeticaly')
	parser.add_argument('-n', '--newest', action='store_true', help='sort by publish date, newest first')
	parser.add_argument('-o', '--oldest', action='store_true', help='sort by publish date, oldest first')
	parser.add_argument('-D', '--show-tags', action='store_true', help='show tags')
	parser.add_argument('-T', '--tags', nargs='+', help='show titles with tags')
	parser.add_argument('-d', '--show-date', action='store_true', help='show publish date')
	
	args = parser.parse_args()

	print(args)

	if args.newest and args.oldest:
		print('Error')
		sys.exit(1)
	if args.count is not None:
		if args.count < 1:
			print('Error')
			sys.exit(1)


	URL = 'https://www.theguardian.com/international/rss'
	articles = getArticles(URL)
	
	if not args.show_title and not args.show_url and not args.show_date and not args.show_tags:
		args.show_title, args.show_url, args.show_date, args.show_tags = True, True, True, True


	printArticles(articles, count=args.count, newest=args.newest, oldest=args.oldest, 
					sort=args.sort, show_tags=args.show_tags, tags=args.tags, show_title=args.show_title, show_url=args.show_url, show_date=args.show_date)

	#for article in articleList:
	#	allTags.append()#