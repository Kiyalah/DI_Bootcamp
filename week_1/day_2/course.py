# sample_dict = { 
#    "class":{ 
#       "student":{ 
#          "name":"Mike",
#          "marks":{ 
#             "physics":70,
#             "history":80
#          }
#       }
#    }
# }

# print(sample_dict["class"]["student"]["marks"]["history"])



# for item in enumerate('abcd'):
#     print(item)

# (0, 'a') # Syntax : (index , value)
# (1, 'b')
# (2, 'c')
# (3, 'd')

# for (index_count, letter) in enumerate('abcd', start=15):
#     print('At index {} the letter is {}'.format(index_count, letter))
    
    
    
myList = [10, 25, 17, 9, 30, -5]
# Filters the elements which are not multiples of 5
myList2 = filter(lambda n : n%5 == 0, myList)
print(list(myList2))