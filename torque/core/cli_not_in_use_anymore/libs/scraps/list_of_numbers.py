def decreasing_numbers(number):
    list_report = []
    for n in range(number):
        #print(n)
        list_report.append(n)
    return list_report

feed_me_numbers = decreasing_numbers(7)
for i in feed_me_numbers:
    print(i)
