import hashlib
import json
from time import time, ctime
from uuid import uuid4
from flask import Flask, jsonify, request


class Supplier:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.add_new_block(previous_hash=1, proof=100)

    def add_new_block(self, proof, previous_hash=None):
        block = {

            "index": len(self.chain) + 1,
            "date_time": ctime(),
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),

        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, supplier, manufacturer, raw_material):

        self.current_transactions.append(
            {"sender": supplier, "recipient": manufacturer, "item": raw_material}
        )
        return self.recent_block["index"] + 1


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
S = Supplier()



@app.route("/supply", methods=["GET"])
def supply():
    recent_block = S.recent_block
    last_proof = recent_block["proof"]

    proof = S.proof_of_work(last_proof)
    S.new_transaction(
        supplier=node_identifier1,
        manufacturer=node_identifier2,

        raw_material="raw_material",

    )
    previous_hash = S.hash(recent_block)
    block = S.add_new_block(proof, previous_hash)

    res = {

        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],

    }
    return jsonify(res), 200



@app.route("/supply/transaction", methods=["POST"])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "item"]
    if not all(k in values for k in required):
        return "Missing values", 400
    index = S.new_transaction(values["sender"], values["recipient"], values["item"])

    res = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(res), 201


@app.route("/blockchain", methods=["GET"])
def full_chain():
    res = {
        "chain": S.chain,
        "length": len(S.chain),

    }
    return jsonify(res), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

