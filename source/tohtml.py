import re, html, sys

src = open(sys.argv[1], encoding='utf-8', errors='replace').read()

# Drop head/script/style
src = re.sub(r'(?is)<(script|style|head)\b.*?</\1>', ' ', src)

# Replace <math ... alttext="LATEX" ...>...</math> with $LATEX$
def math_repl(m):
    tag = m.group(0)
    alt = re.search(r'alttext="(.*?)"', tag, re.S)
    if alt:
        return ' $' + html.unescape(alt.group(1)) + '$ '
    return ' '
src = re.sub(r'(?is)<math\b.*?</math>', math_repl, src)

# Block-level tags -> newlines
src = re.sub(r'(?i)</?(p|div|br|li|tr|h1|h2|h3|h4|h5|h6|section|table|blockquote)\b[^>]*>', '\n', src)
src = re.sub(r'(?i)</?(td|th)\b[^>]*>', ' | ', src)
src = re.sub(r'(?s)<[^>]+>', '', src)
src = html.unescape(src)
src = re.sub(r'[ \t\xa0]+', ' ', src)
src = re.sub(r'\n\s*\n\s*\n+', '\n\n', src)
open(sys.argv[2],"w",encoding="utf-8").write(src.strip())
