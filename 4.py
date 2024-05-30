def find_substring(s, sub):
    result = []
    i = 0
    while i < len(s):
        j = s.find(sub, i)
        if j != -1:
            result.append(j)
            i = j + 1
        else:
            break
    return result

s = input()
sub = input()
print(find_substring(s, sub))