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
        # This will fail if i+2 is out of bounds
        if i + 2 < len(markdown) and markdown[i:i+2] == "\n\n":
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
            if i + 1 < len(markdown) and markdown[i] == " ":
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
    html += "</p>"
    return html

if __name__ == "__main__":
   # Sample test cases for Markdown processor

    # List of input strings
    test_inputs = [
        # Sample 1 – Basic paragraphs and line breaks
        "Hello world.\nThis is a second line in the same paragraph.\n\nThis is a new paragraph.",

        # Sample 2 – Paragraphs with blockquote
        "Normal paragraph here.\n\n> This is a blockquote line 1\n> This is line 2 of the same blockquote\n\nBack to normal paragraph.",

        # Sample 3 – Strikethrough inside a paragraph
        "This is a ~~mistyped~~ corrected word.\nAnother paragraph without formatting.",

        # Sample 4 – Mix of everything
        "Paragraph one with a soft\nline break.\n\nParagraph two starts here\n> Blockquote line 1\n> Blockquote line 2\n\nFinal paragraph with a ~~strikethrough~~ word.",

        # Sample 5 – Consecutive blockquotes
        "> First blockquote\n> still first blockquote\n\n> Second blockquote starts here\n> continues\nNormal paragraph after blockquotes."
    ]

    # Optional: placeholder expected outputs (replace with your real HTML if available)
    expected_outputs = [
        "<p>Hello world.<br />This is a second line in the same paragraph.</p>\n<p>This is a new paragraph.</p>",
        "<p>Normal paragraph here.</p>\n<p><blockquote>This is a blockquote line 1<br />This is line 2 of the same blockquote</blockquote></p>\n<p>Back to normal paragraph.</p>",
        "<p>This is a <del>mistyped</del> corrected word.</p>\n<p>Another paragraph without formatting.</p>",
        "<p>Paragraph one with a soft<br />line break.</p>\n<p>Paragraph two starts here<br /><blockquote>Blockquote line 1<br />Blockquote line 2</blockquote></p>\n<p>Final paragraph with a <del>strikethrough</del> word.</p>",
        "<p><blockquote>First blockquote<br />still first blockquote</blockquote></p>\n<p><blockquote>Second blockquote starts here<br />continues</blockquote></p>\n<p>Normal paragraph after blockquotes.</p>"
    ]

    # Run tests
    for i, input_text in enumerate(test_inputs):
        result = markdownToHTML(input_text)
        print(f"Test case {i+1}:")
        print("Input:")
        print(input_text)
        print("Output:")
        print(result)
        print("Expected:")
        print(expected_outputs[i])
        print("-" * 40)