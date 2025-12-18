
synonyms = {}
word = input()
with open(word + ".txt") as f:
    linelist = f.readlines()
syn_was_found = False
letter = input()
for item in linelist:
    if item[0] == letter:
        list_of_syns = item.split(" ")
        print("\n".join(list_of_syns))
        syn_was_found = True
if not syn_was_found:
    print(f"No synonyms found for {word} beginning with {letter}.")