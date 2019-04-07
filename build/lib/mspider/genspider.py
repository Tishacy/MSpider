# -*- coding: utf-8 -*-
import argparse, os

def genspider():
	"""Generate your spider based on templates.
	"""
	parser = argparse.ArgumentParser("Generate your spider based on templates")
	parser.add_argument('name', help="Your spider name")
	parser.add_argument('-b', '--base', help="Spider template that based. 'm'/'MSpider': MSpider 'c'/'Crawler': Crawler. Default spider template is MSpider.")
	args = parser.parse_args()

	spider_path = './{0}.py'.format(args.name)
	if os.path.isfile(spider_path):
		raise ValueError("File %s.py already exists, please change your spider name." %(args.name))

	if args.base in ["m", 'MSpider', None]:
		templ_path = get_resource_path('templates/spider_templ_based_MSpider.py')
	elif args.base in ['c', 'Crawler']:
		templ_path = get_resource_path('templates/spider_templ_based_Crawler.py')
	else:
		raise ValueError("-b or --base is the spider template that based, choose 'm'/'MSpider' for MSpider template, or 'c'/'Crawler' for Crawler.")

	class_name = _format_class_name(args.name)
	templ = open(templ_path, 'r', encoding='utf-8').read().format(class_name, args.name)
	with open(spider_path, 'w', encoding='utf-8') as f:
		f.write(templ)
	print("A spider named %s is initialized." %(args.name))

def _format_class_name(spider_name):
	return spider_name.capitalize() + 'Spider'

def get_resource_path(path):
    dir_path = os.path.dirname(__file__)
    dir_path = dir_path if dir_path else os.getcwd()
    return os.path.join(dir_path, path)

if __name__=="__main__":
	genspider()
