import csv
import os

def load_mempool(file_path):
    mempool = {}
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            txid = row[0].strip()
            fee = int(row[1].strip())
            weight = int(row[2].strip())
            parents = [p.strip() for p in row[3].split(';') if p.strip()] if len(row) > 3 else []
            
            mempool[txid] = {
                'fee': fee,
                'weight': weight,
                'parents': parents
            }
    return mempool

def get_all_ancestors(txid, mempool, visited, ordered_ancestors):
    if txid in visited:
        return
    visited.add(txid)
    
    if txid in mempool:
        for parent in mempool[txid]['parents']:
            get_all_ancestors(parent, mempool, visited, ordered_ancestors)
            
    ordered_ancestors.append(txid)

def main():
    mempool_path = "tarefa-3-pow-lucasTL1/data/mempool.csv"
    required_txid = "4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6"

    mempool = load_mempool(mempool_path)
    
    block_txids = []
    block_set = set()
    current_weight = 0
    current_fees = 0
    
    ordered_req_family = []
    get_all_ancestors(required_txid, mempool, set(), ordered_req_family)
    
    for txid in ordered_req_family:
        if txid in mempool:  # Se o ancestral estiver no mempool ativo
            tx_data = mempool[txid]
            block_txids.append(txid)
            block_set.add(txid)
            current_weight += tx_data['weight']
            current_fees += tx_data['fee']
            
    print(f"Após incluir a obrigatória e ancestrais:")
    print(f"Peso: {current_weight} | Taxas: {current_fees} sats")

    
    # Ordena todas as transações do mempool pela razão (fee / weight) decrescente
    available_txs = sorted(
        [tx for tx in mempool if tx not in block_set],
        key=lambda tx: mempool[tx]['fee'] / mempool[tx]['weight'],
        reverse=True
    )
    
    for txid in available_txs:
        tx_data = mempool[txid]
        
        if current_weight + tx_data['weight'] > 4000000:
            continue
            
        # Verifica se todos os pais dessa transação já estão no bloco
        parents_valid = all(parent in block_set for parent in tx_data['parents'])
        
        if parents_valid:
            block_txids.append(txid)
            block_set.add(txid)
            current_weight += tx_data['weight']
            current_fees += tx_data['fee']

    print(f"\nBloco Finalizado:")
    print(f"Total de Transações: {len(block_txids)}")
    print(f"Peso Total: {current_weight} / 4000000")
    print(f"Taxa Total Coletada: {current_fees} sats")
        
    with open("tarefa-3-pow-lucasTL1/solutions/exercise01.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(block_txids))
    print("\nArquivo solutions/exercise01.txt gerado com sucesso.")

if __name__ == "__main__":
    main()