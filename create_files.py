path=r''

# with open(path+'\new_file5.txt', 'w+') as f:
#     for i in range(9999999):
#         f.write('a'*999999)
#         f.write('\n')

for i in range(100000):
    with open(path+'\\'+str(i)+'.txt', 'w') as f:
        f.write('my name is')
