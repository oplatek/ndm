#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate synthetic datasets for demonstration purposes
"""
import random
import json
import argparse


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
        q = "i'm looking for a %s %s restaurant" % (pr, fd)
        a = '%s%s serves %s food in the %s price range.' % (pr, fd, fd, pr)
        dialogs.append([
            ['hello', q, q, -555.5555, 'none none none'],
            [a, 'thank you goodbye', 'thank you goodbye', -666.666, '%s %s none' % (fd, pr)]])
    return dialogs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--train-size', type=int, default=500)
    parser.add_argument('--dev-size', type=int, default=100)
    parser.add_argument('--test-size', type=int, default=100)
    parser.add_argument('--price-dim', type=int, default=2)
    parser.add_argument('--food-dim', type=int, default=2)
    args = parser.parse_args()

    other_ambiguous_factor=1  # use it in id
    template_name = r'data.synthetic01.%s.json'
    db_name = 'data.synthetic01.db.json'
    db_data1 = gen_db(args.price_dim, args.food_dim, other_ambiguous_factor)
    with open(db_name, 'w') as w:
        json.dump(db_data1, w, sort_keys=True, indent=4, separators=(',', ': '))
    for s, c in [('train', args.train_size), ('dev', args.dev_size), ('test', args.test_size)]:
        set_name = template_name % s
        with open(set_name, 'w') as w:
            json.dump(generate_synthetic01(c, dim_price=args.price_dim, dim_food=args.food_dim), w, sort_keys=True, indent=4, separators=(',', ': '))
