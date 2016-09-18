from urllib.request import urlopen
from icalendar import Calendar, Event, vDatetime
from datetime import datetime, date, timezone
import os
from markdown2 import Markdown
import jinja2

def getCal(url):
	with urlopen(url) as ics:
		return Calendar.from_ical(ics.read())

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)
	return jinja2.Environment(
		loader=jinja2.FileSystemLoader(path or './')
	).get_template(filename).render(context)

url = "https://seattleu.instructure.com/feeds/calendars/user_hDYTHQB70FzLttLqhwsWN8dCxxi8OZkX16aYSCN2.ics"
cal = getCal(url)
md = Markdown()
context = {
	'message': md.convert('''Hello, world!\n\nTesting, testing.\n\n- Item 1\n- Item 2'''),
	'events': []
}
for item in cal.walk():
	if item.name == "VEVENT" and item.get("summary").endswith(" [CS Club]"):
		dt = item.get('dtstart').dt
		if not isinstance(dt, datetime):
			dt = datetime.combine(dt, datetime.min.time()).replace(tzinfo=timezone.utc)
		else:
			dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
		if dt > datetime.now(timezone.utc):
			event = {
				'name': item.get('summary')[:-len(" [CS Club]")],
				'description': md.convert(item.get('description')),
				'sMonth': dt.strftime('%b'),
				'sDay': dt.strftime('%d'),
				'sTime': dt.strftime('%I:%M %p').lstrip('0')
			}
			duplicate = False
			for i in range(len(context['events'])):
				if context['events'][i]['name'] == event['name'] and context['events'][i]['description'] == event['description']:
					duplicate = True
					# No need to compare dates since events are processed in chronological order
					# (current event will always have greater date than last event)
					context['events'][i]['eMonth'] = event['sMonth']
					context['events'][i]['eDay'] = event['sDay']
					context['events'][i]['eTime'] = event['sTime']
			if not duplicate:
				context['events'].append(event)
			# for k,v in event.items():
			# 	print(k, v.replace(u"\u2018", "'").replace(u"\u2019", "'"))
			# print()

for event in context['events']:
	for k,v in event.items():
		print(k, v.replace(u"\u2018", "'").replace(u"\u2019", "'"))

print(str(context).replace(u"\u2018", "'").replace(u"\u2019", "'"))
result = render('template.html', context)
with open('result.html', 'w') as file:
	file.write(result)