import re

pattern = r"\$ezC:.+?\-\>.+?\$"
text = "Some text //$ezC:test->int$ and more text //$ezC:example->string$"

matches = re.findall(pattern, text)
print(matches)
for match in matches:
    print(match)
