'''
You are tasked with building a simplified Markdown-to-HTML converter.

Given a raw input string that represents text written in a limited Markdown-like syntax, your job is to transform it into an HTML-formatted string.

For this first part, you only need to support the following conversions:

Paragraphs → <p> ... </p>
Paragraphs are separated by blank lines (\n\n).

Soft line breaks → <br />
A single newline (\n) inside a paragraph becomes a line break.

Block quotes → <blockquote> ... </blockquote>
Lines starting with > belong to a block quote.

Strikethrough → <del> ... </del>
Text wrapped in ~~ should be converted into strikethrough formatting.

For example, given the input string:
"This is a paragraph with a soft\nline break.\n\nThis is another paragraph that has\n> Some text that\n> is in a\n> block quote.
\n\nThis is another paragraph with a ~~strikethrough~~ word."

<p>
This is a paragraph with a soft<br />
line break.
</p>

<p>
This is another paragraph that has<br />
<blockquote>
Some text that<br />
is in a<br />
block quote.
</blockquote>
</p>

<p>
This is another paragraph with a <del>strikethrough</del> word.
</p>
'''


'''
Approach:
1. Loop through the string.
2. Start with a paragraph tag. DONE.
3. If we encounter \n\n, close paragraph tag, and start a new one. DONE.
4. If we encounter \n, add a <br /> tag. DONE.
5. A blockquote starts when we encounter a line starting with '>' and ends when we encounter a new paragraph.
6. A strikethough starts when we encounter '~~' and ends when we encounter the next '~~'.

'''

def markdownToHTML(markdown: str) -> str:
    html = "<p>"
    i = 0
    in_blockquote = False
    in_strikethough = False

    #Handle all newlines and brs first
    while i < len(markdown):
        if markdown[i:i+2] == "\n\n":
            if in_blockquote:
                html += "</blockquote>"
                in_blockquote = False
            # Don't add a new paragraph tag if we're at the end of the string
            if i != len(markdown) - 2:
                html += "</p><p>"
                i += 2
            else:
                html += "</p>"
                i += 2
        elif markdown[i] == "\n":
            html += "<br />"
            i += 1
        #Handle the blockquote
        elif markdown[i] == ">":
            if not in_blockquote:
                html += "<blockquote>"
                in_blockquote = True
                i += 1
        #Handle the strikethrough
        elif markdown[i:i+2] == "~~":
            if not in_strikethough:
                html += "<del>"
                in_strikethough = True
            else:
                html += "</del>"
                in_strikethough = False
            i += 2
        else:
            html += markdown[i]
            i += 1