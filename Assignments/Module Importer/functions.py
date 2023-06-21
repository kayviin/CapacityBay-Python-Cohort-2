file = open("data.txt","w")
content = {'I am A Python Developer \n', 'I Believe in Hard Work \n' , 'I Love CapacityBay'}
file.writelines(content)
file.close()

def display_content(data):
    f = open('data.txt', 'r')
    content = f.read()
    print(content)