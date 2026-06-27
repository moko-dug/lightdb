"""
投影模块 
"""

def project_columns(data, columns):
   
    if columns == ['*'] or not columns:
        return data
    
    result = []
    for row in data:
        new_row = {}
        for col in columns:
            col = col.strip() 
            new_row[col] = row.get(col, '')
        result.append(new_row)
    return result

"""投影测试"""
if __name__ == '__main__':
    test_data = [
        {'id': '1', 'product': '手机', 'price': '3999', 'region': '北京', 'quantity': '10'},
        {'id': '2', 'product': '电脑', 'price': '5999', 'region': '上海', 'quantity': '5'},
        {'id': '3', 'product': '耳机', 'price': '499', 'region': '北京', 'quantity': '20'},
    ]
    
    print("=" * 50)
    print("  投影测试")
    print("=" * 50)
    
    print("\n原始数据（所有列）:")
    for r in test_data:
        print(f"   {r}")
    
    print("\nSELECT product, price:")
    result = project_columns(test_data, ['product', 'price'])
    for r in result:
        print(f"   {r}")
    
    print("\nSELECT product, region:")
    result = project_columns(test_data, ['product', 'region'])
    for r in result:
        print(f"   {r}")
    
    print("\nSELECT * (所有列):")
    result = project_columns(test_data, ['*'])
    for r in result:
        print(f"   {r}")
    
    print("\n测试完成!")