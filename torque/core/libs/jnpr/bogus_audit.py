def audit_pigs_in_space(number):
    import random
    possible_audit_outcomes = ["FAIL", "PASS"]
    outcome_names = ["Melody", "Sebastian", "Sigfrid", "Sven", "Robin", 
        "Luigi", "Pietro", "Bernadette", "Julie"
    ]
    outcome_verbs = ["flies", "runs", "bullfights", "sews", "paints", "climbs",
        "swims", "cuts the grass", "drinks", "eats", "jumps", "counts"
    ]
    outcome_adverbs = ["beautifully", "gently", "like a limp elephant", 
        "like a squirrel", "supremely", "neatly", "chancely", 
        "oddly", "like Beckam", "timidly", "cockily", "swiftly"
    ]
    list_report = []

    for n in range(number*1):
        my_result = random.choice(possible_audit_outcomes)
        my_name = random.choice(outcome_names)
        my_verb = random.choice(outcome_verbs)
        my_adverb = random.choice(outcome_adverbs)
        my_outcome = my_result + ", " + my_name + " " + my_verb + " " + my_adverb
        #list_report.append(random.choice(possible_audit_outcomes))
        list_report.append(my_outcome)
    return list_report

'''
# uncomment this section if you want to test
feed_me_audit_results= audit_pigs_in_space(7)
for i in feed_me_audit_results:
        print(i)
'''


