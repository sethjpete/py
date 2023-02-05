import subprocess

bible_books = ["Matthew",
"Mark",
"Luke",
"John",
"Acts",
"Romans",
"1 Corinthians",
"2 Corinthians",
"Galatians",
"Ephesians",
"Philippians",
"Colossians",
"1 Thessalonians",
"2 Thessalonians",
"1 Timothy",
"2 Timothy",
"Titus",
"Philemon",
"Hebrews",
"James",
"1 Peter",
"2 Peter",
"1 John",
"2 John",
"3 John",
"Jude",
"Revelation"]

def add_link(line):
    for book in bible_books:
        if line.find(book) != -1:
            line = "<a href=\"https://www.churchofjesuschrist.org/search?lang=eng&page=1&query="+line.replace("<li>","").replace("</li>","").replace(" ","+")+"\">"+line+"</a>"
    line = "<b>" + line + "</b>"
    return line

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def processText(contents):
    TAB_CHAR = "^" # Must be a unique character
    for index, line in enumerate(contents):
        if line.find(TAB_CHAR) != -1:
            line = line.replace(TAB_CHAR, "<TAB>")
        contents[index] = line
    
    output = []
    previous_depth = 0
    zoom_open = False
    for index, line in enumerate(contents):
        depth = line.count("<TAB>")
        if depth > previous_depth:
            if depth == 1: # First level of zoom
                output.append("<Zoom>")
                zoom_open = True
            output.append("<ul>")
        elif depth < previous_depth:
            for _ in range(previous_depth - depth):
                output.append("</ul>")
            if depth == 1:
                if zoom_open:
                    output.append("</Zoom>")
                output.append("<Zoom>")
        if line.find("<TAB>") != -1:
            line = line.replace("<TAB>", "<li>", 1)
            line = line.replace("<TAB>", "")
            line = line + "</li>"
        if depth == 1:
            line = add_link(line)
        previous_depth = depth
        output.append(line)

    for i in range(previous_depth):
        output.append("</ul>")
    if zoom_open:
        output.append("</Zoom>")

    return output

def list_to_string(list, end=""):
    string = ""
    for item in list:
        string += item + end
    return string

def printList(list, end=""):
    for item in list:
        print(item, end=end)

def count_zooms(contents):
    zooms = 0
    for line in contents:
        if line.find("<Zoom>") != -1:
            zooms += 1
    return zooms

def count_close_zooms(contents):
    zooms = 0
    for line in contents:
        if line.find("</Zoom>") != -1:
            zooms += 1
    return zooms

def main():
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    contents = processText(contents)

    printList(contents, end="\n")
    print("Zooms: " + str(count_zooms(contents)) + " Close Zooms: " + str(count_close_zooms(contents)))

    input1 = input("Copy to clipboard? (y/n): ")
    if input1 == "y":
        input2 = input("Add variable name? (y/n): ")
        if input2 == "y":
            write_to_clipboard("const lines = `" + list_to_string(contents, end="") + "`")
            exit()
        write_to_clipboard(list_to_string(contents, end=""))
        exit()

if __name__ == "__main__":
    main()