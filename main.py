"""
测试Python环境和CSV读取是否正常
"""
import csv
import os

print("=" * 50)
print("  LightDB 环境测试")
print("=" * 50)

# 测试1：Python版本
import sys
print(f"✅ Python版本: {sys.version}")

# 测试2：data目录是否存在
if os.path.exists('data'):
    print("✅ data目录存在")
else:
    print("❌ data目录不存在，正在创建...")
    os.makedirs('data')
    print("✅ data目录已创建")

# 测试3：尝试读取sales.csv（如果有的话）
csv_path = 'data/sales.csv'
if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        first_row = next(reader)
        # 统计行数
        row_count = sum(1 for _ in reader) + 2
        print(f"✅ sales.csv存在")
        print(f"   列名: {headers}")
        print(f"   第一行: {first_row}")
        print(f"   总行数: {row_count}")
else:
    print(f"⚠️  sales.csv还不存在，需要运行数据生成脚本")

print("\n✅ 环境测试完成！")