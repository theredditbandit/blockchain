
# Getting Started

Lets start by understand some basic information about blockchains.

  1. Blockchain is a system of recording information in a way that makes it difficult or impossible to change, hack, or cheat the system.It is a digital ledger of transactions that is duplicated and shared with everyone on the network.

  2. All members share a single view of the truth, you can see all details of a transaction end to end.

  3. Blockchain information is verified by a system called =="hashes"==. Hashes are digital cryptic signatures. Each block contains the hash of the block that comes before and after it. This system helps verify the authenticity of the block.
  A hash looks something like this: ==2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824==
  ![Image shows blocks storing the hashes of previous and successive blocks, thus, verifying authenticity](C:\Users\JAHNAVI\Desktop\Project\Blocks&Hashes.jpg)


### What does a block look like

Each block has an index , a timestamp in unix time , a list of transactions and the hash of the previous block.

Here's an example of a block in our blockchain.
```
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'item': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```
 ### Prerequisites 

Before we delve into the coding part, lets get some softwares set up.
  - Python 3.6 or higher with `pip` installed.
  - Flask and the Requests library
    You can do this with:
     ``pip install Flask==0.12.2 requests==2.18.4``
  - A http client like Postman.


## Get Set Go!
### Step 1: Building a blockchain
Start by creating a file in your favourite IDE. Name it `blockchain.py`

In `blockchain.py` create a `Blockchain` class.

```
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass
    
    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass
    
    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass
```
The blockchain class will store all the transactions and will help in adding new blocks to the chain.
Now that we have a base for managing our blockchain, we need a method to help us update our transactions into a block. The `new_transaction()` method will do this task.

```
class Blockchain(object):
    ...
    
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
```

Transactions are added to a list and the `new_transaction()` method returns the index of the block. This index is used when the next block is created linking the two blocks in a chain.

As you can see, our blockchain has slowly started taking shape.

When our blockchain is initiated, the first block, called the genesis block, needs to be initialized. This includes setting the hash of the previous block to 0 (as there is no predecessor). We will also need to add a **proof** to the block. We will talk more about this particular topic a little down the line.

Lets also update the methods `new_block()`, `hash()`, and `new_transaction()`.
```
import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, item):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param item: <int> item
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'item': item,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
```

### Proof of Work
Now, `proof of work` is a core concept of blockchains. The proof of work algorithm is how new blocks are created or _mined_ in the blockchain. The main function of the algorithm is to find a number that is hard to find from outside the network, but easy to verify from inside the network.

The proof of work that is used in this program is rather simple.
The algorithm finds a number p' such that the hash(pp') contains 4 leading zeros, where p is the previous proof, and p' is the new proof. This is constantly updated whenever new blocks are added to the network.

```
def proof_of_work(self, last_proof):
        """
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
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
```
Depending on the difficulty of the proof of work algorithm, we can modify the number of leading zeros.

# Creating an API for our blockchain
For a beginner, the biggest question right now must be, what is an API?
API stands for Application-Program Interface. Just the way the User Interface connects the user to the computer and makes it easier for the user to access the computer, the API connects two or more software components.
It is not ment to be used by the general users, but by programmers to efficiently link multiple pieces of software.

The most important use of API is in Data Abstraction. APIs hide all internat data that the programmer does not need making it a more secure evironment.

We’re going to use the Python Flask Framework. It’s a micro-framework and it makes it easy to map endpoints to Python functions. This allows us talk to our blockchain over the web using HTTP requests.

### Setting up our Server
```
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask


class Blockchain(object):
    ...


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
In our server code above, we create `/mine`, `/transaction/new` and `/chain` endpoints.
The `/mine` endpoint works as a GET request.
The `/trasnaction/new` endpoint works as a POST request.
The `/chain` endpoint returns the complete blockchain.

We now need to enable new transactions in the network.
```
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'item']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['item'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201
```
The above code will allow us to register new transactions into the blockchain network. But just registering the code is not enough. We also need to validate it.
This is where the `/mine` endpoint come into play. The mining endpoint will calculate our proof of work, it will reward the miner and add 1 new transaction, and forge a new block into the blockchain network.

```
@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        item=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
```
At this point we have reached a milestone. Our server interacts and works on the basis of our `blockchain class`
So now all we need to do is start interacting with the network directly.

# First Look at our Blockchain Network
```

```