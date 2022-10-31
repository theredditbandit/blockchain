from uuid import uuid4
import uuid
from flask import Flask, jsonify, request
from blockchain import Blockchain

# --- Setting up flask to implement blockchain API---#
def get_values():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        return request.get_json()
    else:
        return "Content-Type not supported"


def setup_server():
    # Instantiate our node
    app = Flask(__name__)
    # Generate a globally unique address for this node using uuid
    sender_id = str(uuid4()).replace("-","")
    recipient_id = str(uuid4()).replace("-", "")
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
            sender=sender_id,
            recipient=recipient_id,
            item="Nill",
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
        required = ["sender", "recipient", "item"]
        if not all(
            k in values for k in required
        ):  # checks if all the required values are present
            return "Missing values", 400

        # create a new transaction
        index = blockchain.new_transaction(
            values["sender"], values["recipient"], values["item"]
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

    @app.route("/nodes/register", methods=["POST"])
    def register_nodes():
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            values = request.get_json()
        else:
            return "Content-Type not supported"

        nodes = values.get("nodes")
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400
        for node in nodes:
            blockchain.register_node(node)

        response = {
            "message": "New nodes have been added",
            "total_nodes": list(blockchain.nodes),
        }

        return jsonify(response), 201

    @app.route("/nodes/resolve", methods=["GET"])
    def consensus():
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                "message": "Our chain was replaced",
                "new_chain": blockchain.chain,
            }
        else:
            response = {
                "message": "Our chain is authoritative",
                "chain": blockchain.chain,
            }
        return jsonify(response), 200

    app.run(host="0.0.0.0", port=5000)

setup_server()