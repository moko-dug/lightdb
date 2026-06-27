"""
哈希索引
"""
import time


class HashIndex:
    def __init__(self):
        self.indexes = {}
    
    def build(self, data, table, column):
        key = f'{table}.{column}'
        index = {}
        
        for i, row in enumerate(data):
            value = row.get(column, '')
            if value not in index:
                index[value] = []
            index[value].append(i)
        
        self.indexes[key] = index
        return index
    
    def lookup(self, table, column, value):
        key = f'{table}.{column}'
        if key in self.indexes:
            return self.indexes[key].get(value, [])
        return None
    
    def has_index(self, table, column):
        return f'{table}.{column}' in self.indexes

if __name__ == '__main__':
    import csv
    
    print("  哈希索引性能测试")
    
    print("\n加载数据...")
    with open('data/sales.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    print(f"加载了 {len(data)} 行数据")

    test_id = data[50000]['id']
    test_region = data[30000]['region'] 
    print(f"\n测试等值查询: id = '{test_id}'")
    print(f"测试等值查询: region = '{test_region}'")
  
    print("  无索引等值查询")

    start = time.time()
    result_no_idx = []
    for row in data:
        if row['id'] == test_id:
            result_no_idx.append(row)
    time_id_no_idx = time.time() - start
    print(f"id等值查询: {time_id_no_idx:.6f} 秒, 找到 {len(result_no_idx)} 行")
    
    start = time.time()
    result_no_idx = []
    for row in data:
        if row['region'] == test_region:
            result_no_idx.append(row)
    time_region_no_idx = time.time() - start
    print(f"region等值查询: {time_region_no_idx:.6f} 秒, 找到 {len(result_no_idx)} 行")

    print("  建立哈希索引")
    
    idx = HashIndex()
    
    start = time.time()
    idx.build(data, 'sales', 'id')
    time_build_id = time.time() - start
    print(f"id索引建立: {time_build_id:.4f} 秒")
    
    start = time.time()
    idx.build(data, 'sales', 'region')
    time_build_region = time.time() - start
    print(f"region索引建立: {time_build_region:.4f} 秒")
  
    print("  有索引等值查询")

    start = time.time()
    row_ids = idx.lookup('sales', 'id', test_id)
    result_idx = [data[i] for i in row_ids] if row_ids else []
    time_id_idx = time.time() - start
    print(f"id等值查询: {time_id_idx:.6f} 秒, 找到 {len(result_idx)} 行")
    
    start = time.time()
    row_ids = idx.lookup('sales', 'region', test_region)
    result_idx = [data[i] for i in row_ids] if row_ids else []
    time_region_idx = time.time() - start
    print(f"region等值查询: {time_region_idx:.6f} 秒, 找到 {len(result_idx)} 行")
    
    print("  性能对比")

    speedup_id = time_id_no_idx / time_id_idx if time_id_idx > 0 else float('inf')
    speedup_region = time_region_no_idx / time_region_idx if time_region_idx > 0 else float('inf')
    
    print(f"{'测试':<20} {'无索引':<15} {'有索引':<15} {'加速比':<10}")
    print("-" * 60)
    print(f"{'id等值查询':<20} {time_id_no_idx:<15.6f} {time_id_idx:<15.6f} {speedup_id:<10.2f}x")
    print(f"{'region等值查询':<20} {time_region_no_idx:<15.6f} {time_region_idx:<15.6f} {speedup_region:<10.2f}x")
    
    print(f"\n索引建立耗时: id={time_build_id:.4f}s, region={time_build_region:.4f}s")

    print("  多次查询平均耗时(10次)")
  
    import random
    test_ids = [data[random.randint(0, len(data)-1)]['id'] for _ in range(10)]

    total = 0
    for tid in test_ids:
        start = time.time()
        for row in data:
            if row['id'] == tid:
                break
        total += time.time() - start
    avg_no_idx = total / 10

    total = 0
    for tid in test_ids:
        start = time.time()
        row_ids = idx.lookup('sales', 'id', tid)
        if row_ids:
            _ = data[row_ids[0]]
        total += time.time() - start
    avg_idx = total / 10
    
    print(f"无索引平均: {avg_no_idx:.6f} 秒")
    print(f"有索引平均: {avg_idx:.6f} 秒")
    print(f"加速比: {avg_no_idx/avg_idx:.2f}x")
    
    print("\n实验完成!")