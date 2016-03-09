#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import json

template_name = r'data.synthetic01.%s.json'
sets_splits = [('train', 500), ('dev', 100), ('test', 100)]
db_name = 'data.synthetic01.db.json'
dim_price=100
dim_food=100
other_ambiguous_factor=1  # use it in id


def gen_db(dim_price=2, dim_food=2, other_ambiguous_factor=1):
    db = []
    for p in range(dim_price):
        for f in range(dim_food):
            for a in range(other_ambiguous_factor):
                pr = "pricerange%d" % p
                fd = "food%d" % f
                db.append({
                    "addr": "constant_addr",
                    "pricerange": pr,
                    "name": "%s%s" % (fd, pr),
                    "area": "ambiguous%d" % a,
                    "food": fd,
                    "phone": "constant_phone",
                    "postcode": "constant_phone"
                })
    return db


def generate_synthetic01(num_dialog, dim_price=2, dim_food=2):
    dialogs = []
    for i in range(num_dialog):
        pr = 'pricerange%d' % random.randint(0, dim_price - 1)
        fd = 'food%d' % random.randint(0, dim_food - 1)
        q = 'I am looking for a %s %s restaurant' % (pr, fd)
        # a = '%s serves %{matched_slots} food'  should be better
        a = '%s%s matches the criteria.' % (pr, fd)
        dialogs.append([
            ['hello', 'hi', 'hi', -555.5555, 'none none none'],
            [a, q, q, -666.666, '%s %s none' % (fd, pr)]])
    return dialogs


if __name__ == "__main__":
    db_data1 = gen_db(dim_price, dim_food, other_ambiguous_factor)
    with open(db_name, 'w') as w:
        json.dump(db_data1, w, sort_keys=True, indent=4, separators=(',', ': '))
    for s, c in sets_splits:
        set_name = template_name % s
        with open(set_name, 'w') as w:
            json.dump(generate_synthetic01(c), w, sort_keys=True, indent=4, separators=(',', ': '))
