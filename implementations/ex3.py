import hashlib
import struct
import time
import os

def mine_block():
    print("INICIANDO MINERADOR DO BLOCO ")
    
    ex02_path = "solutions/exercise02.txt"
        
    with open(ex02_path, "r") as f:
        merkle_root_hex = f.readline().strip() 
        
    print(f"Merkle Root recuperada: {merkle_root_hex}")

    version_bytes = struct.pack(">I", 2)
    
    prev_block_hex = "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"
    prev_block_bytes = bytes.fromhex(prev_block_hex)
    
    merkle_bytes = bytes.fromhex(merkle_root_hex)
    
    timestamp_bytes = struct.pack(">I", 1231469705)

    static_header = version_bytes + prev_block_bytes + merkle_bytes + timestamp_bytes

    target_prefix = b'\x00\x00\x00\x00'

    nonce = 0
    start_time = time.time()
    
    print("Minerando...")
    
    while True:
        nonce_bytes = struct.pack(">Q", nonce)
        
        block_header = static_header + nonce_bytes
        
        block_hash = hashlib.sha256(block_header).digest()
        
        if block_hash[:4] == target_prefix and block_hash[4] <= 0xff:
            end_time = time.time()
            
            header_hex = block_header.hex()
            hash_hex = block_hash.hex()
            
            print("BLOCO MINERADO")
            print(f"Header Válido (Hex): {header_hex}")
            print(f"Hash do Bloco: {hash_hex}")
            print(f"Nonce utilizado: {nonce}")
                
            with open("solutions/exercise03.txt", "w") as out_file:
                out_file.write(header_hex + "\n")
                
            print("Arquivo solutions/exercise03.txt gerado com sucesso!")
            break
            
        nonce += 1
        
        if nonce % 5000000 == 0:
            print(f"Hashes testados: {nonce:,}...", end="\r")

if __name__ == "__main__":
    mine_block()