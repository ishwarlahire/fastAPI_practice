dic = {
    "name":"Ishwar",
    "roll_no":22,
}

obj = {
    "first_name":"om",
    "roll_no":22,
    "school":{
        "name":"jpmorgan",
        "address":"JPnager"
    }
}

print(obj["school"]["name"])

print(type(dic),type(1))

num = 121 

str1 = str(num)
str2 = str1[::-1]
str2 = int(str2)
print(True if str2 == num else False)