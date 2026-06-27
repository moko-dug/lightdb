"""
聚合查询
"""

def aggregate(data, func, column):
    if func.upper() == 'COUNT':
        return len(data)

    values = []
    for row in data:
        try:
            val = float(row.get(column, 0))
            values.append(val)
        except (ValueError, TypeError):
            pass 
    if not values:
        return 0
    
    if func.upper() == 'SUM':
        return sum(values)
    elif func.upper() == 'AVG':
        return sum(values) / len(values)
    elif func.upper() == 'MAX':
        return max(values)
    elif func.upper() == 'MIN':
        return min(values)
    
    return None


"""聚合查询测试"""
if __name__ == '__main__':
    test_data = [
        {'product': '手机', 'price': '3999', 'quantity': '10'},
        {'product': '电脑', 'price': '5999', 'quantity': '5'},
        {'product': '耳机', 'price': '499', 'quantity': '20'},
    ]

    print("  聚合查询测试")
    
    print(f"\n数据: 3行 (手机3999, 电脑5999, 耳机499)")
    print(f"COUNT: {aggregate(test_data, 'COUNT', '*')}")
    print(f"SUM(price): {aggregate(test_data, 'SUM', 'price')}")
    print(f"AVG(price): {aggregate(test_data, 'AVG', 'price'):.2f}")
    print(f"MAX(price): {aggregate(test_data, 'MAX', 'price')}")
    print(f"MIN(price): {aggregate(test_data, 'MIN', 'price')}")
    print(f"SUM(quantity): {aggregate(test_data, 'SUM', 'quantity')}")