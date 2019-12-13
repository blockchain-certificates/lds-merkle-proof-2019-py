from cbor2 import dumps, loads
import json
from multibase import encode, decode
from .mappings import *


def map_root(json_dict):
    mapped_list = []

    for key in json_dict:
        if key == 'merkleRoot':
            mapped_list.append([root[key], dumps(json_dict[key])])
        if key == 'targetHash':
            mapped_list.append([root[key], dumps(json_dict[key])])
        if key == 'path':
            path_list = []
            for path_item in json_dict[key]:
                if 'right' in path_item:
                    path_list.append([path['right'], dumps(path_item['right'])])
                if 'left' in path_item:
                    path_list.append([path['left'], dumps(path_item['left'])])
            mapped_list.append([root[key], path_list])
        if key == 'anchors':
            anchor_list = []
            for anchor_item in json_dict[key]:
                anchor_item_list = []
                anchor_items = anchor_item.split(':')
                for i, anchor_partial in enumerate(anchor_items):
                    if i == 0:
                        continue
                    elif i == 1:
                        anchor_item_list.append([0, chain[anchor_partial]['id']])
                    elif i == 2:
                        anchor_item_list.append([1, chain[anchor_items[i - 1]]['networks'][anchor_partial]])
                    else:
                        anchor_item_list.append([i - 1, dumps(anchor_partial)])
                anchor_list.append(anchor_item_list)
            mapped_list.append([root[key], anchor_list])

    return mapped_list

def parse_map(map):
    # inverse mapping
    inv_root = {v: k for k, v in root.items()}
    inv_path = {v: k for k, v in path.items()}

    decoded_json = {}

    for map_item in map:
        print(root)

        if map_item[0] == 0:
            decoded_json[inv_root[map_item[0]]] = loads(map_item[1])
        elif map_item[0] == 1:
            decoded_json[inv_root[map_item[0]]] = loads(map_item[1])
        elif map_item[0] == 2:
            anchor_string_list = []
            for anchor in map_item[1]:
                anchor_string = 'blink:'
                anchored_chain = findChainById(anchor[0][1])
                anchor_string += anchored_chain + ':'
                anchor_string += findNetworkById(anchored_chain, anchor[1][1]) + ':'
                anchor_string += loads(anchor[2][1])

                anchor_string_list.append(anchor_string)
            decoded_json[inv_root[map_item[0]]] = anchor_string_list
        elif map_item[0] == 3:
            path_list = []
            for path_item in map_item[1]:
                path_item_obj = {}
                direction = inv_path[path_item[0]]
                path_item_obj[direction] = loads(path_item[1])
                path_list.append(path_item_obj)
            decoded_json[inv_root[map_item[0]]] = path_list

    print(decoded_json)
    return decoded_json


class MerkleProof2019:
    def __init__(self):
        proof_value = None
        proof_json = None

    def decode(self, proof_value):
        multibase_decoded = decode(proof_value)
        decoded_map = loads(multibase_decoded)
        return parse_map(decoded_map)

    def encode(self, proof_json):
        if type(proof_json) == str:
            json_object = json.loads(proof_json)
        else:
            json_object = proof_json
        map_root_value = map_root(json_object)

        # cbor encode map
        cbor_map = dumps(map_root_value)

        # multibase encode to base58btc
        multibase = encode('base58btc', cbor_map)
        return multibase
