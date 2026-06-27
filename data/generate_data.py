"""
生成10万行测试数据
运行：在终端执行  uv run python data/generate_data.py
"""
import csv
import random
import os

print("=" * 50)
print("  生成测试数据")
print("=" * 50)

# 商品列表
products = [
    ('手机', 999, 4999),
    ('笔记本电脑', 2999, 9999),
    ('平板', 1499, 5999),
    ('耳机', 99, 1999),
    ('智能手表', 799, 3499),
    ('键盘', 79, 999),
    ('鼠标', 29, 599),
    ('显示器', 699, 3999),
    ('充电器', 19, 199),
    ('音箱', 199, 2999)
]

regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京']
statuses = ['已签收', '运输中', '待发货', '已退货']

print("正在生成10万行数据...")
print("(这可能需要1-2分钟)\n")

with open('data/sales.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 写表头
    writer.writerow(['id', 'product', 'price', 'quantity', 'total', 'region', 'status', 'date'])
    
    for i in range(100000):
        # 随机选择商品
        product_name, min_price, max_price = random.choice(products)
        price = round(random.uniform(min_price, max_price), 2)
        quantity = random.randint(1, 50)
        total = round(price * quantity, 2)
        region = random.choice(regions)
        status = random.choice(statuses)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = f'2024-{month:02d}-{day:02d}'
        
        writer.writerow([i+1, product_name, price, quantity, total, region, status, date])
        
        # 每1万行显示进度
        if (i+1) % 10000 == 0:
            print(f'  进度: {(i+1)//1000}万行 / 10万行')

print('\n✅ 数据生成完成！')

# 验证文件
file_size = os.path.getsize('data/sales.csv')
print(f'📁 文件大小: {file_size / 1024 / 1024:.2f} MB')

# 预览前5行
print('\n📋 前5行预览：')
with open('data/sales.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i <= 5:
            print(f'  {", ".join(row)}')
        else:
            break

# 统计信息
with open('data/sales.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 跳过表头
    count = sum(1 for _ in reader)

print(f'\n📊 总计: {count} 行数据')
print('\n✅ 可以开始下一步了！')