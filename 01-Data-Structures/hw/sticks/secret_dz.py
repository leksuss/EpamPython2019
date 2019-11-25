pizza = {
    'ground pepper',
    'salt',
    'cheese',
    'dough',
    'tomatoes',
    'sweet basil',
    'oregano',
    'onion',
    'pepperoni',
    'garlic'
}
shaverma = {
    'cabbages',
    'fried chicken',
    'onion',
    'cucumbers',
    'tomatoes',
    'lavash',
    'sauce'
}

# unoin
print(pizza | shaverma)
# intersection
print(pizza & shaverma)
# difference1
print(pizza - shaverma)
# difference2
print(shaverma - pizza)
# symm_difference1
print(pizza ^ shaverma)
# symm_difference2
print(shaverma ^ pizza)
