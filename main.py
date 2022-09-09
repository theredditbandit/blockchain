import hashlib
import json
from time import time, ctime
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        creates a new block and adds it to the chain
        :param proof: <int> The proof given by the proof of work algorithm
        :param previous_hash: (optional) <str> Hash of previous block
        :return: <dict> new block
        """
        block = {
            "index": len(self.chain) + 1,
            "timestamp-unix": time(),
            "datetime": ctime(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction to the list of transactions
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amount
        :return: <int> The index of block that will hold this transaction
        """
        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
        )

        return self.last_block["index"] + 1

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        - Find a number p' such that the hash(pp') contains 4 leading zeros, where p is the previous p'
        - p is the previous proof, and p' is the new proof
         :param last_proof: <int>
         :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof : Does the hash(last_proof,proof) contain 4 leading zeros?
        To adjust the difficulty of the algorithm we can modify the number of leading zeros
        :param last_proof:<int> previous proof
        :param proof:<int> current proof
        :return: <bool> True if correct , False if not.
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Creates an SHA-256 hash of a block
        :param block:<dict> block
        :return:<str>
        """
        # We must make sure that the dictionary is ordered , or we'll have inconsistent hashes

        block_string = json.dumps(
            block, sort_keys=True
        ).encode()  # converts our dict to json and encodes it to UTF-8
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]

    # --- Setting up flask to implement blockchain API---#


def setup_server():
    # Instantiate our node
    app = Flask(__name__)
    # Generate a globally unique address for this node using uuid
    node_identifier = str(uuid4()).replace("-", "")
    # Instantiate the blockchain
    blockchain = Blockchain()

    @app.route("/mine", methods=["GET"])
    def mine():
        # We run the proof of work algorithm to get the next proof
        last_block = blockchain.last_block
        last_proof = last_block["proof"]
        proof = blockchain.proof_of_work(last_proof)
        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )
        # Forge the new block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
        response = {
            "message": "New block forged",
            "index": block["index"],
            "transactions": block["transactions"],
            "proof": block["proof"],
            "previous_hash": block["previous_hash"],
        }
        return jsonify(response), 200

    @app.route("/transactions/new", methods=["POST"])
    def new_transaction():  # a method for creating transactions
        values = request.get_json()
        # check that the required fields are in the POSTed data
        required = ["sender", "recipient", "amount"]
        if not all(
            k in values for k in required
        ):  # checks if all the required values are present
            return "Missing values", 400

        # create a new transaction
        index = blockchain.new_transaction(
            values["sender"], values["recipient"], values["amount"]
        )
        response = {"message": f"Transaction will be added to block {index}"}
        return jsonify(response), 201

    @app.route("/chain", methods=["GET"])
    def full_chain():
        response = {
            "chain": blockchain.chain,
            "length": len(blockchain.chain),
        }
        return jsonify(response), 200

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)


def main():
    setup_server()


if __name__ == "__main__":
    main()
