import re


art_url = "10.192.39.26:5001"
art_url1  = re.search('(.+?):',art_url).group(1)
print art_url1
