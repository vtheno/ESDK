#coding=utf-8
import re
collection = ['django_migrations.py',
                'django_admin_log.py',
                'main_generator.py',
                'migrations.py',
                'api_user.doc',
                'user_group.doc',
                'accounts.txt',]
collection = map(str,range(1000000))
def fuzzy(user_input,collection):
    suggestions = []
    pattern = '.*?'.join(user_input)    # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)      # Compiles a regex.
    for item in collection:
        match = regex.search(item)   # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]
import timeit
t1 = timeit.Timer("fuzzy('23333',collection)",'from __main__ import collection,fuzzy')
print t1.timeit(20)
