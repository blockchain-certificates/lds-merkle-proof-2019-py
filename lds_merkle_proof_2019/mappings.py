root = {
    'merkleRoot': 0,
    'targetHash': 1,
    'anchors': 2,
    'path': 3
}

path = {
    'left': 0,
    'right': 1
}

chain = {
  'btc': {
    'id': 0,
    'networks': {
      'mainnet': 1,
      'testnet': 3
    }
  },
  'eth': {
    'id': 1,
    'networks': {
      'mainnet': 1,
      'ropsten': 3,
      'rinkeby': 4
    }
  }
}

def findChainById(key, value):
    for i, dic in chain.items():
        if chain[i]['id'] == value:
            return i
    return ''



def findNetworkById(blockchain, key, value):
    networks = chain[blockchain]['networks']
    for i, dic in networks.items():
        if networks[i] == value:
            return i
    return ''