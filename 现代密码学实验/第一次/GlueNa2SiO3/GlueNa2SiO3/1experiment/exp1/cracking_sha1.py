import hashlib
import itertools

target = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
chars = ['(', 'Q','q', '=', '%','w','W', 'i','I','~','@', 'n','N','*','8','4','6','5','2']  

found_key = False
for i in range(1, len(chars) + 1):
    for perm in itertools.permutations(chars, i):
        s = ''.join(perm)
        if hashlib.sha1(s.encode()).hexdigest() == target:
            print("key:", s)
            found_key = True
            break
    if found_key:
        break
    
    
