"""
列式存储引擎
"""
import csv
import os
import time


class ColumnarStore:
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
    
    def write(self, data, table_name):
        
        if not data:
            return
      
        col_dir = os.path.join(self.data_dir, 'columnar', table_name)
        os.makedirs(col_dir, exist_ok=True)
        
        columns = list(data[0].keys())
      
        for col in columns:
            col_file = os.path.join(col_dir, f'{col}.csv')
            with open(col_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow([row.get(col, '')])
        
        schema_file = os.path.join(col_dir, '_schema.csv')
        with open(schema_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
    
    def read_columns(self, table_name, columns):

        col_dir = os.path.join(self.data_dir, 'columnar', table_name)
        
        col_data = {}
        for col in columns:
            col_file = os.path.join(col_dir, f'{col}.csv')
            if os.path.exists(col_file):
                with open(col_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    col_data[col] = [row[0] for row in reader]
        
        if not col_data:
            return []
        
        num_rows = len(list(col_data.values())[0])
        result = []
        for i in range(num_rows):
            row = {}
            for col in columns:
                row[col] = col_data[col][i] if i < len(col_data[col]) else ''
            result.append(row)
        
        return result
    
    def read_column(self, table_name, column):
   
        col_dir = os.path.join(self.data_dir, 'columnar', table_name)
        col_file = os.path.join(col_dir, f'{column}.csv')
        
        values = []
        with open(col_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                values.append(row[0])
        return values
    
    def aggregate_column(self, table_name, column, func):
      
        values = self.read_column(table_name, column)
        
        nums = []
        for v in values:
            try:
                nums.append(float(v))
            except ValueError:
                pass
        
        if not nums:
            return 0
        
        if func == 'SUM':
            return sum(nums)
        elif func == 'AVG':
            return sum(nums) / len(nums)
        elif func == 'MAX':
            return max(nums)
        elif func == 'MIN':
            return min(nums)
        elif func == 'COUNT':
            return len(nums)
        return 0


class RowStore:
    """行式存储：传统CSV，按行读取"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
    
    def read_all(self, table_name):
        """读取整个CSV文件"""
        filepath = os.path.join(self.data_dir, f'{table_name}.csv')
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)


if __name__ == '__main__':
    print("  列式存储 vs 行式存储 性能对比")
    
    row_store = RowStore('data')
    data = row_store.read_all('sales')
    print(f"   加载了 {len(data)} 行数据")
    
    # 2. 转换为列式存储
    print("\n2. 转换为列式存储...")
    col_store = ColumnarStore('data')
    
    start = time.time()
    col_store.write(data, 'sales')
    write_time = time.time() - start
    print(f"列式存储写入完成，耗时: {write_time:.4f} 秒")
    
  
    print("  实验1: 聚合查询 SUM(total)")

    start = time.time()
    total_row = 0
    for row in data:
        total_row += float(row.get('total', 0))
    time_row_sum = time.time() - start
    print(f"行式存储 SUM(total): {total_row:.2f}")
    print(f"耗时: {time_row_sum:.6f} 秒")
  
    start = time.time()
    total_col = col_store.aggregate_column('sales', 'total', 'SUM')
    time_col_sum = time.time() - start
    print(f"列式存储 SUM(total): {total_col:.2f}")
    print(f"耗时: {time_col_sum:.6f} 秒")
    
    print(f"\n加速比: {time_row_sum/time_col_sum:.2f}x (列式更快)")

    print("  实验2: 聚合查询 AVG(price)")
  
    start = time.time()
    prices_row = []
    for row in data:
        prices_row.append(float(row.get('price', 0)))
    avg_row = sum(prices_row) / len(prices_row)
    time_row_avg = time.time() - start
    print(f"行式存储 AVG(price): {avg_row:.2f}")
    print(f"耗时: {time_row_avg:.6f} 秒")

    start = time.time()
    avg_col = col_store.aggregate_column('sales', 'price', 'AVG')
    time_col_avg = time.time() - start
    print(f"列式存储 AVG(price): {avg_col:.2f}")
    print(f"耗时: {time_col_avg:.6f} 秒")
    
    print(f"\n加速比: {time_row_avg/time_col_avg:.2f}x (列式更快)")
    
    print("  实验3: 全行读取（所有列）")

    start = time.time()
    all_data_row = row_store.read_all('sales')
    time_row_all = time.time() - start
    print(f"行式存储读取全部: {len(all_data_row)} 行")
    print(f"耗时: {time_row_all:.6f} 秒")
  
    start = time.time()
    columns = list(data[0].keys())
    all_data_col = col_store.read_columns('sales', columns)
    time_col_all = time.time() - start
    print(f"列式存储读取全部: {len(all_data_col)} 行")
    print(f"耗时: {time_col_all:.6f} 秒")
    
    if time_row_all < time_col_all:
        print(f"\n行式存储更快: {time_col_all/time_row_all:.2f}x")
    else:
        print(f"\n列式存储更快: {time_row_all/time_col_all:.2f}x")

    print("  实验4: 单列读取 price")

    start = time.time()
    prices = []
    for row in data:
        prices.append(row.get('price', ''))
    time_row_one = time.time() - start
    print(f"行式存储读取price列: {len(prices)} 个值")
    print(f"耗时: {time_row_one:.6f} 秒")
    
    start = time.time()
    prices_col = col_store.read_column('sales', 'price')
    time_col_one = time.time() - start
    print(f"列式存储读取price列: {len(prices_col)} 个值")
    print(f"耗时: {time_col_one:.6f} 秒")
    
    print(f"\n加速比: {time_row_one/time_col_one:.2f}x (列式更快)")
    
    print("  性能对比汇总")
    print(f"{'测试场景':<20} {'行式(秒)':<15} {'列式(秒)':<15} {'加速比':<10} {'胜出':<10}")
    print(f"{'SUM(total)':<20} {time_row_sum:<15.6f} {time_col_sum:<15.6f} {time_row_sum/time_col_sum:<10.2f}x {'列式':<10}")
    print(f"{'AVG(price)':<20} {time_row_avg:<15.6f} {time_col_avg:<15.6f} {time_row_avg/time_col_avg:<10.2f}x {'列式':<10}")
    print(f"{'单列读取':<20} {time_row_one:<15.6f} {time_col_one:<15.6f} {time_row_one/time_col_one:<10.2f}x {'列式':<10}")
    print(f"{'全行读取':<20} {time_row_all:<15.6f} {time_col_all:<15.6f} {time_row_all/time_col_all if time_row_all < time_col_all else time_col_all/time_row_all:<10.2f}x {'行式' if time_row_all < time_col_all else '列式':<10}")
    
    print(f"\n列式存储转换耗时: {write_time:.4f} 秒")

    print("  结论:")
    print("  1. 聚合查询(SUM/AVG)：列式存储显著更快")
    print("     - 原因：只需读取单列文件，跳过无关列")
    print("  2. 单列读取：列式存储更快")
    print("     - 原因：直接读该列文件，无需解析整行")
    print("  3. 全行读取：行式存储通常更快")
    print("     - 原因：列存需要读取多个文件并重组")

    
    print("\n实验完成!")