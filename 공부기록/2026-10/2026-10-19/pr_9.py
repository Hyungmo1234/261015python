str= "Hello, World!"
print(str)

print(str.upper())

print(str.lower())
print(str.capitalize())

print(str.join(["a", "b"])) 
print(str.split(","))
print(str)

print(len(str))

str = str + " "
str = " " + str

print(str.replace("World", "Python"))

print(len(str))
str = str.strip()
print(str)


print(str.ljust(20, "*"))
print(str.zfill(20))