a1 = '123'
b1 = '12'
a = list(a1)
b = list(b1)
a.reverse()
b.reverse()

t = False
for i in range(len(a)):
    if a[i] == b[i]:
        t = True
    else:
        t = False
        break
print(t)

print(a, b)

100 +1000

