import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(Previous_proof = '0')
        
    def create_block(self, Previous_proof):
        block = {'Index': len(self.chain) +1,
                 'Timestamp': str(datetime.datetime.now()),
                 'Previous_proof': Previous_proof
                 }
        nonce = 1 
        check = False
        while check is False:
            block['Nonce'] = nonce
            hash_operation = self.Hashing(block)
            if hash_operation[:4] != '0000' :
                nonce += 1
            else:
                check = True
                block['Hash'] = hash_operation
        self.chain.append(block)
        return block
    
      
    def Hashing(self, block):
        encoded_str = json.dumps(block, sort_keys=True).encode()
        Hash = hashlib.sha256(encoded_str).hexdigest()
        return Hash
    
    def get_last_block(self):
        return self.chain[-1]
    
    def Is_valid(self, chain):
        index = 1
        block1= chain[0]
        block2 = chain[index]
        block2_pr_hash = block2['Previous_proof']
        copyblock1 = block1
        del copyblock1['Hash']
        hash_operation = self.Hashing(copyblock1)
        if hash_operation != block2_pr_hash and hash_operation[:4] != '0000':
            return False
        else:
            index += 1
            block1 = block2
        return True
        
        
       
        
       
        
       
        
       
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain = Blockchain()

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/mine', methods = ['GET'])
def mine():
    prev_block = blockchain.get_last_block()
    prev_Hash = prev_block['Hash']
    block = blockchain.create_block(prev_Hash)
    response = {'Message': "henry, congrats on your block",   
                'Index': block['Index'],
                'Timestamp': block['Timestamp'],
                'Previous_hash': block['Previous_proof'],
                'Nonce': block['Nonce'],
                'Hash': block['Hash']}
    if len(blockchain.chain) == 2:
        response['Message'] = "your 1st bloxk"
    return jsonify(response), 200

@app.route('/valid', methods = ['GET'])
def valid():
    isvalid = blockchain.Is_valid(blockchain.chain)
    if isvalid:
        response = {'Message': 'chain is intact genius!',
                    'length': len(blockchain.chain)}
    else:
        response = {'message': 'Henry, you are a World Class Blockchain genius!'}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)






