This project references and learns a lot from [Daniel Van Flymen](https://hackernoon.com/u/dvf)
Do check out the original instructions from [Learn blockchains by building one by @dvf](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

# Getting Started

Lets start by understand some basic information about blockchains.

  1. Blockchain is a system of recording information in a way that makes it difficult or impossible to change, hack, or cheat the system.It is a digital ledger of transactions that is duplicated and shared with everyone on the network.

  2. All members share a single view of the truth, you can see all details of a transaction end to end.

  3. Blockchain information is verified by a system called =="hashes"==. Hashes are digital cryptic signatures. Each block contains the hash of the block that comes before and after it. This system helps verify the authenticity of the block.
  A hash looks something like this: ==2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824==
  ![Image shows blocks storing the hashes of previous and successive blocks, thus, verifying authenticity](C:\Users\JAHNAVI\Desktop\Project\Blocks&Hashes.jpg)

  4. 

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
            'amount': 5,
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
    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
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

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
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
Now, proof of work is a core concept of blockchains. The proof of work algorithm is how new blocks are created or _mined_ in the blockchain. The main function of the algorithm is to find a number that is hard to find from outside the network, but easy to verify from inside the network.

