from collections import deque

search_collection =["a", "a", "a"]
sc = deque(search_collection)
if len(sc) < 2:
    sc.append("a")
    print(sc)
elif len(sc) == 2:
    print(sc)
elif len(sc) > 2:
    sc.pop()
    print(sc)



