import unittest
from lds_merkle_proof_2019.merkle_proof_2019 import MerkleProof2019

proofEncoded = b'zmz7LKNSJbePX9eJWLTaNA3X69vbLSiaJWJPVpFWznKg19Aeug3PQHFrkySKFvvGJhECwPMn947tzUFYnVMxbS428oLi5tw2HLKP9szAArV3TbfDSKXddpfV6fPBde6XN8FDbri2wGtYrgyzDXEaGu6QzzUd1GDMTcZ7c9FVFTb8k5v6crug5aLt2Sevap1gE9DS7ZUpfRMv8TQHiktNnQBGgc74g8soERFuziTDWoPGTu3Xb6bAs431DJpGGKHDenmFjkQFUJnwQ9nFKKowYnf9h8Gp8gcQmE78aoWhtEG4qV6Jaik8HhPTQX3dD7MQrXzY8GAHh8tKWQfscyGWb6w4FMpok13jBpZWpaPTVR5fMXsa1garazbMRL7xssnwEJ2gzrCDrGkFXb3JyDGoXMffAYKHUetADrCd3sZKW9k5jC5d6bMA5zSwbyeZE9BjaD27mTrJXSzguAZ1pKsghFztG5u5h6jLgBGMp2aPFopvESSnCA'
proofDecoded = {
    "path": [
        {"right": "51b4e22ed024ec7f38dc68b0bf78c87eda525ab0896b75d2064bdb9fc60b2698"},
        {"right": "61c56cca660b2e616d0bd62775e728f50275ae44adf12d1bfb9b9c507a14766b"}
    ],
    "merkleRoot": "3c9ee831b8705f2fbe09f8b3a92247eed88cdc90418c024924be668fdc92e781",
    "targetHash": "c65c6184e3d5a945ddb5437e93ea312411fd33aa1def22b0746d6ecd4aa30f20",
    "anchors": [
        "blink:btc:testnet:582733d7cef8035d87cecc9ebbe13b3a2f6cc52583fbcd2b9709f20a6b8b56b3"
    ]
}

proofMocknetDecoded = {
    "path": [
        {"right": "51b4e22ed024ec7f38dc68b0bf78c87eda525ab0896b75d2064bdb9fc60b2698"},
        {"right": "61c56cca660b2e616d0bd62775e728f50275ae44adf12d1bfb9b9c507a14766b"}
    ],
    "merkleRoot": "3c9ee831b8705f2fbe09f8b3a92247eed88cdc90418c024924be668fdc92e781",
    "targetHash": "c65c6184e3d5a945ddb5437e93ea312411fd33aa1def22b0746d6ecd4aa30f20",
    "anchors": [
        "blink:mocknet:582733d7cef8035d87cecc9ebbe13b3a2f6cc52583fbcd2b9709f20a6b8b56b3"
    ]
}


class TestEncoding(unittest.TestCase):
    def test_decoding_correct(self):
        mp2019 = MerkleProof2019()

        check_decoded = mp2019.decode(proofEncoded)
        self.assertEqual(check_decoded, proofDecoded)

    def test_decoding_incorrect(self):
        mp2019 = MerkleProof2019()

        error = False
        try:
            check_decoded = mp2019.decode('not a valid encoding')
        except:
            error = True

        self.assertTrue(error)

    def test_encoding_correct(self):
        mp2019 = MerkleProof2019()

        check_encoded = mp2019.encode(proofDecoded)
        self.assertEqual(check_encoded, proofEncoded)

    def test_encoding_correct_mocknet(self):
        mp2019 = MerkleProof2019()

        check_encoded = mp2019.encode(proofMocknetDecoded)
        self.assertIsNotNone(check_encoded)

    def test_encoding_incorrect(self):
        mp2019 = MerkleProof2019()

        error = False
        try:
            check_encoded = mp2019.encode('not a valid decoding')
        except:
            error = True

        self.assertTrue(error)


if __name__ == '__main__':
    unittest.main()
