import re
inputlist = []
[inputlist.append(m.start()) for m in re.finditer('test', 'test test test test')]
print(inputlist)