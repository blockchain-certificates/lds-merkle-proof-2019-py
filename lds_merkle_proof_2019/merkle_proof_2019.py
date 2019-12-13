from cbor2 import dumps, loads
import json
from multibase import encode, decode
import binascii
from .mappings import *


def map_root(json_dict):
    mapped_list = []

    for key in json_dict:
        print(key, '->', json_dict[key])
        if key == 'merkleRoot':
            print('hex rep of ' + json_dict[key] + ': ')
            print(bytes.fromhex(json_dict[key]))
            print(bytes.fromhex(json_dict[key]))
            print(bytearray.fromhex(json_dict[key]))
            print(json_dict[key].encode())
            print('cbor: ')
            print(dumps(bytes.fromhex(json_dict[key])))
            print(dumps(bytearray.fromhex(json_dict[key])))
            print(dumps(json_dict[key].encode()))
            # mapped_list.append([root[key], dumps(json_dict[key].encode())])
            mapped_list.append([root[key], dumps(json_dict[key])])
        if key == 'targetHash':
            mapped_list.append([root[key], dumps(json_dict[key])])
        if key == 'path':
            path_list = []
            for path_item in json_dict[key]:
                print(path_item)
                if 'right' in path_item:
                    path_list.append([path['right'], dumps(path_item['right'])])
                if 'left' in path_item:
                    path_list.append([path['left'], dumps(path_item['left'])])
            mapped_list.append([root[key], path_list])
        if key == 'anchors':
            anchor_list = []
            for anchor_item in json_dict[key]:
                print(anchor_item)
                anchor_item_list = []
                anchor_items = anchor_item.split(':')
                print(anchor_items)
                for i, anchor_partial in enumerate(anchor_items):
                    if i == 0:
                        continue
                    elif i == 1:
                        anchor_item_list.append([0, chain[anchor_partial]['id']])
                    elif i == 2:
                        print(chain[anchor_items[i - 1]])
                        print(anchor_partial)
                        print(chain[anchor_items[i - 1]]['networks'][anchor_partial])
                        anchor_item_list.append([1, chain[anchor_items[i - 1]]['networks'][anchor_partial]])
                    else:
                        anchor_item_list.append([i - 1, dumps(anchor_partial)])
                anchor_list.append(anchor_item_list)
            mapped_list.append([root[key], anchor_list])

    return mapped_list

def parse_map(map):
    decoded_json = {}

    print('\nDecoding map into json..')
    print(map)

    # inverse mapping
    inv_root = {v: k for k, v in root.items()}
    inv_path = {v: k for k, v in path.items()}
    # inv_chain = {v: k for k, v in chain.items()}

    for map_item in map:
        print(root)

        if map_item[0] == 0:
            # print('merkle map..')
            # print(map_item[1])
            #print(loads(map_item[1]))
            # print(inv_root[map_item[0]])
            decoded_json[inv_root[map_item[0]]] = loads(map_item[1])
        elif map_item[0] == 1:
            decoded_json[inv_root[map_item[0]]] = loads(map_item[1])
        elif map_item[0] == 2:
            print('anchor list:')
            print(map_item[1])
            anchor_string_list = []
            for anchor in map_item[1]:
                print('anchor item..')
                print(anchor)
                anchor_string = 'blink:'
                anchored_chain = findChainById('id', anchor[0][1])
                anchor_string += anchored_chain + ':'
                anchor_string += findNetworkById(anchored_chain, 'networks', anchor[1][1]) + ':'
                anchor_string += loads(anchor[2][1])

                anchor_string_list.append(anchor_string)
            decoded_json[inv_root[map_item[0]]] = anchor_string_list
        elif map_item[0] == 3:
            print('path list:')
            print(map_item[1])
            path_list = []
            for path_item in map_item[1]:
                print('path item:')
                print(path_item)
                path_item_obj = {}
                direction = inv_path[path_item[0]]
                path_item_obj[direction] = loads(path_item[1])
                path_list.append(path_item_obj)
            decoded_json[inv_root[map_item[0]]] = path_list

    print(decoded_json)
    return decoded_json


class MerkleProof2019:
    def __init__(self):
        print('initializing...')
        proof_value = None
        proof_json = None

    def decode(self, proof_value):
        print('\ndecoding proof value: ', proof_value)
        multibase_decoded = decode(proof_value)
        print ('multibase decoded into cbor:')
        print(multibase_decoded)
        print(binascii.hexlify(multibase_decoded))
        decoded_map = loads(multibase_decoded)
        print('cbor map: ', decoded_map)
        return parse_map(decoded_map)

        # turn map back into json

    def encode(self, proof_json):
        # print('encoding proof_json: ' + proof_json)

        # validate json

        # construct root map
        # turn "merkleRoot": "3c9.." into [ [ 0, buffer] ]
        if type(proof_json) == str:
            json_object = json.loads(proof_json)
        else:
            json_object = proof_json
        # print('about to go through map of json:')
        # print(json_object)
        map_root_value = map_root(json_object)
        print('map: ')
        print(map_root_value)

        # cbor encode map
        cbor_map = dumps(map_root_value)
        print('cbor encoded map: ')
        print(cbor_map)
        print(binascii.hexlify(cbor_map))

        # multibase encode to base58btc
        multibase = encode('base58btc', cbor_map)
        print('multibase of encoded map: ')
        print(multibase)

        print('decode multibase right after: ', decode(multibase))

        # print(encode('base58btc', 'hello world'))

        # testing

        return multibase
