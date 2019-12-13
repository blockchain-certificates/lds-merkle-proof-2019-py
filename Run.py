from lds_merkle_proof_2019.merkle_proof_2019 import MerkleProof2019

mp2019 = MerkleProof2019()

#decoded_value = mp2019.decode('asdfasdf')
#print(decoded_value)

json_string = '{' \
              '"path": [{ "right": "51b4e22ed024ec7f38dc68b0bf78c87eda525ab0896b75d2064bdb9fc60b2698" },{ "right": "61c56cca660b2e616d0bd62775e728f50275ae44adf12d1bfb9b9c507a14766b" }],' \
              '"merkleRoot": "3c9ee831b8705f2fbe09f8b3a92247eed88cdc90418c024924be668fdc92e781",' \
              '"targetHash": "c65c6184e3d5a945ddb5437e93ea312411fd33aa1def22b0746d6ecd4aa30f20",' \
              '"anchors": ["blink:btc:testnet:582733d7cef8035d87cecc9ebbe13b3a2f6cc52583fbcd2b9709f20a6b8b56b3"]' \
              '' \
              '}'
encoded_value = mp2019.encode(json_string)

print('\nresults::')
print(encoded_value)

print(mp2019.decode(encoded_value))