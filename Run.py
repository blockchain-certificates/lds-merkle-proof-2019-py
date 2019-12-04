from lds_merkle_proof_2019.merkle_proof_2019 import MerkleProof2019

mp2019 = MerkleProof2019()

decoded_value = mp2019.decode('asdfasdf')
print(decoded_value)

encoded_value = mp2019.encode('{"test": true}')
print(encoded_value)