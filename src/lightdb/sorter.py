"""
排序
"""

def sort_data(data, column, ascending=True):
    if not data:
        return data
    
    try:
        float(data[0][column])
        return sorted(data, key=lambda x: float(x.get(column, 0)), reverse=not ascending)
    except (ValueError, KeyError, TypeError):
        return sorted(data, key=lambda x: x.get(column, ''), reverse=not ascending)

"""排序测试"""
if __name__ == '__main__':
    test_data = [
        {'product': '手机', 'price': '3999', 'quantity': '10'},
        {'product': '电脑', 'price': '5999', 'quantity': '5'},
        {'product': '耳机', 'price': '499', 'quantity': '20'},
        {'product': '平板', 'price': '2999', 'quantity': '15'},
    ]
    
    print("  排序测试")
    
    print("\n原始数据:")
    for r in test_data:
        print(f"   {r['product']}: ¥{r['price']}")
    
    print("\n按价格升序 (ORDER BY price ASC):")
    result = sort_data(test_data, 'price', True)
    for r in result:
        print(f"   {r['product']}: ¥{r['price']}")
    
    print("\n按价格降序 (ORDER BY price DESC):")
    result = sort_data(test_data, 'price', False)
    for r in result:
        print(f"   {r['product']}: ¥{r['price']}")
    
    print("\n按数量降序 (ORDER BY quantity DESC):")
    result = sort_data(test_data, 'quantity', False)
    for r in result:
        print(f"   {r['product']}: {r['quantity']}个")
    
    print("\n测试完成!")