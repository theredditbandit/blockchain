import hashlib
import json
from time import time, ctime
from uuid import uuid4
from flask import Flask, jsonify, request


class Manufacturer:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.add_new_block(previous_hash=1, proof=100)

    def add_new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'date_time': ctime(),
            "timestamp": time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, manufacturer, supplier, raw_material):
        self.current_transactions.append({
            'sender': manufacturer,
            'recipient': supplier,
            'item': raw_material
        })
        return self.recent_block['index'] + 1

    @property
    def recent_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


app = Flask(__name__)
node_identifier1 = str(uuid4())
node_identifier2 = str(uuid4())
M = Manufacturer()


@app.route('/demand', methods=['GET'])
def demand():
    recent_block = M.recent_block
    M.new_transaction(
        manufacturer=node_identifier2,
        supplier=node_identifier1,
        raw_material='raw_material',
    )
    previous_hash = M.hash(recent_block)
    block = M.add_new_block(previous_hash)

    res = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(res), 200


@app.route('/demand/transaction', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'item']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = M.new_transaction(values['sender'], values['recipient'], values['item'])

    res = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(res), 201


@app.route('/blockchain', methods=['GET'])
def full_chain():
    res = {
        'chain': M.chain,
        'length': len(M.chain),
    }
    return jsonify(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
