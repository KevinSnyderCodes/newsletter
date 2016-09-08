import feedparser
import os
from markdown2 import Markdown
import jinja2

d = feedparser.parse('https://api.orgsync.com/api/v3/portals/139259/events.rss?key=TD18DDaXso6j_3R0F_nnpYHU4Xh5XnUaNBh0ZLpB9Ac&per_page=100&upcoming=true')
for entry in d.entries:
	print(entry.title)
	print(entry.link)
	print(entry.description)
	print(entry.published)
	print(entry.published_parsed)
	print(entry.id)

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)
	return jinja2.Environment(
		loader=jinja2.FileSystemLoader(path or './')
	).get_template(filename).render(context)

context = {
	'message': '''Hello, world!\n\nTesting, testing.\n\n- Item 1\n- Item 2'''
}
md = Markdown()
for key, val in context.items():
	context[key] = md.convert(val)
print(context['message'])
result = render('template.html', context)
with open('result.html', 'w') as file:
	file.write(result)