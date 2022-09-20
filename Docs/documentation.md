# Getting Started

Lets start by understand some basic information about blockchains.
  1. Blockchain is a system of recording information in a way that makes it difficult or impossible to change, hack, or cheat the system.It is a digital ledger of transactions that is duplicated and shared with everyone on the network.  
  2. All members share a single view of the truth, you can see all details of a transaction end to end. 
  3. Blockchain information is verified by a system called =="hashes"==. Hashes are digital cryptic signatures. Each block contains the hash of the block that comes before and after it. This system helps verify the authenticity of the block. 
  A hash looks something like this: ==2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824==
  ![Image shows blocks storing the hashes of previous and successive blocks, thus, verifying authenticity](C:\Users\JAHNAVI\Desktop\Project\Blocks&Hashes.jpg)
  4. 

# What does a block look like

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

