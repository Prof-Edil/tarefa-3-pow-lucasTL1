import hashlib
import os

def sha256_bytes(b):
    return hashlib.sha256(b).digest()

def build_merkle_tree_and_proof(txid_list_path, target_txid_hex):
    with open(txid_list_path, 'r', encoding='utf-8') as f:
        level = [bytes.fromhex(line.strip()) for line in f if line.strip()]
    
    target_bytes = bytes.fromhex(target_txid_hex)
    
    if target_bytes not in level:
        print(f"Erro: Alvo {target_txid_hex} não está na lista!")
        return None, []
    
    target_index = level.index(target_bytes)
    proof = []
    
    while len(level) > 1:
        next_level = []
        
        if target_index % 2 == 0:
            sibling_index = target_index + 1 if target_index + 1 < len(level) else target_index
        else:
            sibling_index = target_index - 1
            
        proof.append(level[sibling_index].hex())
        
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i + 1 < len(level) else level[i]
            parent = sha256_bytes(left + right)
            next_level.append(parent)
            
        level = next_level
        target_index = target_index // 2 
        
    merkle_root = level[0].hex()
    return merkle_root, proof

def main():
    tx_list = "data/ex02_txid_list.txt"
    target_tx = "49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb"
        
    root, proof = build_merkle_tree_and_proof(tx_list, target_tx)
    
    if root:
        print(f"Merkle Root calculada: {root}")
        print(f"Passos da Prova obtidos: {len(proof)}")
        
        output_lines = [root] + proof
            
        with open("solutions/exercise02.txt", "w", encoding='utf-8') as f:
            f.write("\n".join(output_lines))
            
        print("Arquivo solutions/exercise02.txt gerado com sucesso!")

if __name__ == "__main__":
    main()