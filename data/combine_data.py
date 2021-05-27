import json
import random
import string

f_ = open('fb15k/entity_ids.del')
ids_ = f_.read().split('\n')
ids = []
strings = set()
for i in ids_[:-1]:
    s = i.split('\t')
    ids.append([int(s[0]), s[1]])
    strings.add(s[1])
f_.close()

rel_ids = open('fb15k/relation_ids.del')
rel_ids = rel_ids.read().split('\n')
fb15k_rel_id_to_word = {}
fb15k_rel_word_to_id = {}
for i in rel_ids[:-1]:
    s = i.split('\t')
    fb15k_rel_id_to_word[int(s[0])] = s[1]
    fb15k_rel_word_to_id[s[1]] = int(s[0])
rel_ids.close()

entity_ids = open('fb15k/entity_ids.del')
entity_ids = entity_ids.read().split('\n')
fb15k_ent_id_to_code = {}
fb15k_ent_code_to_id = {}
for i in entity_ids[:-1]:
    s = i.split('\t')
    fb15k_ent_id_to_code[int(s[0])] = s[1]
    fb15k_ent_code_to_id[s[1]] = int(s[0])
entity_ids.close()

entity_strings = open('fb15k/entity_strings.del')
entity_strings = entity_strings.read().split('\n')
fb15k_ent_code_to_word = {}
fb15k_ent_word_to_code = {}
for i in entity_strings[:-1]:
    s = i.split('\t')
    fb15k_ent_code_to_word[s[0]] = s[1]
    fb15k_ent_word_to_code[s[1]] = s[0]
entity_strings.close()

f = open('alchemy2.json')
recipe = json.load(f)
for i in recipe['entities']:
    recipe['entities'][i]['id'] += 14950
recipe_ids = [recipe['entities'][i]['id'] for i in recipe['entities']]
f.close()

wordcraft_rel_word_to_id = {'COMBINES_WITH' : 1345, 'COMPONENT_OF' : 1346}
wordcraft_rel_id_to_word = {1345 : 'COMBINES_WITH', 1346 : 'COMPONENT_OF'}

wordcraft_ent_word_to_id = {}
wordcraft_ent_id_to_word = {}

for i in recipe['entities']:
    wordcraft_ent_word_to_id[i] = recipe['entities'][i]['id']
    wordcraft_ent_id_to_word[recipe['entities'][i]['id']] = i

chars = string.ascii_lowercase + string.digits

wordcraft_ent_word_to_code = {}
wordcraft_ent_code_to_word = {}
wordcraft_ent_id_to_code = {}
wordcraft_ent_code_to_id = {}

for i in recipe_ids:
    s = "/m/"
    prop = s + ''.join(random.choice(chars) for i in range(5))
    while prop in strings:
        prop = prop + random.choice(chars)
    strings.add(prop)
    wordcraft_ent_word_to_code[wordcraft_ent_id_to_word[i]] = prop
    wordcraft_ent_code_to_word[prop] = wordcraft_ent_id_to_word[i]
    wordcraft_ent_id_to_code[i] = prop
    wordcraft_ent_code_to_id[prop] = i

combines = []
components = []
combines_num = []
components_num = []

for i in recipe['entities']:
    for j in recipe['entities'][i]['recipes']:
        combines.append(j)
        combines_num.append([recipe['entities'][combines[-1][0]]['id'], 1345, recipe['entities'][combines[-1][1]]['id']])
        if [j[0], i] not in components:
            components.append([j[0], i])
            components_num.append([recipe['entities'][components[-1][0]]['id'], 1346, recipe['entities'][components[-1][1]]['id']])
        if [j[1], i] not in components:
            components.append([j[1], i])
            components_num.append([recipe['entities'][components[-1][0]]['id'], 1346, recipe['entities'][components[-1][1]]['id']])

f_ = open('fb15k/train.del')
f_ = f_.read().split('\n')
triples = []
for i in f_[:-1]:
    triples.append(i + '\n')
for i in components_num:
    triples.append(''.join(str(j) + '\t' for j in i)[:-1] + '\n')
for i in combines_num:
    triples.append(''.join(str(j) + '\t' for j in i)[:-1] + '\n')

entity_ids_full = []
for key, value in fb15k_ent_id_to_code.items():
    entity_ids_full.append(''.join(str(key) + '\t' + value + '\n'))
for key, value in wordcraft_ent_id_to_code.items():
    entity_ids_full.append(''.join(str(key) + '\t' + value + '\n'))

entity_strings_full = []
for key, value in fb15k_ent_code_to_word.items():
    entity_strings_full.append(''.join(str(key) + '\t' + value + '\n'))
for key, value in wordcraft_ent_code_to_word.items():
    entity_strings_full.append(''.join(str(key) + '\t' + value + '\n'))

relation_ids_full = []
for key, value in fb15k_rel_id_to_word.items():
    relation_ids_full.append(''.join(str(key) + '\t' + value + '\n'))
for key, value in wordcraft_rel_id_to_word.items():
    relation_ids_full.append(''.join(str(key) + '\t' + value + '\n'))

train_full_f = open('train_full.del', 'w')
entity_ids_full_f = open('entity_ids_full.del', 'w')
entity_strings_full_f = open('entity_strings_full.del', 'w')
relation_ids_full_f = open('relation_ids_full.del', 'w')

train_full_f.writelines(triples)
entity_strings_full_f.writelines(entity_strings_full)
entity_ids_full_f.writelines(entity_ids_full)

for line in relation_ids_full:
    relation_ids_full_f.write(line)

train_full_f.close()
entity_ids_full_f.close()
entity_strings_full_f.close()
relation_ids_full_f.close()
