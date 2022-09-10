from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain

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
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            values = request.get_json()
        else:
            return "Content-Type not supported"
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

    app.run(host="0.0.0.0", port=5000)
