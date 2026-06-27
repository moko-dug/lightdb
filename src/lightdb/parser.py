"""
SQL
"""
import re


class Parser:
    def parse(self, sql):
        sql = sql.strip().rstrip(';')
        query = {
            'type': 'SELECT',
            'columns': ['*'],
            'table': '',
            'conditions': [],
            'order_by': None,
            'order_dir': 'ASC',
            'aggregations': []
        }
        
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.I)
        if select_match:
            cols_str = select_match.group(1).strip()
            if cols_str != '*':
                query['columns'] = []
                for col_part in cols_str.split(','):
                    col_part = col_part.strip()
                    agg_match = re.match(r'(COUNT|SUM|AVG|MAX|MIN)\s*\(\s*(.*?)\s*\)', col_part, re.I)
                    if agg_match:
                        query['aggregations'].append((agg_match.group(1).upper(), agg_match.group(2)))
                    else:
                        query['columns'].append(col_part)
      
        from_match = re.search(r'FROM\s+(\w+)', sql, re.I)
        if from_match:
            query['table'] = from_match.group(1)
   
        where_match = re.search(r'WHERE\s+(.*?)(?:ORDER\s+BY|LIMIT|$)', sql, re.I | re.S)
        if where_match:
            where_str = where_match.group(1).strip()
            query['conditions'] = self._parse_conditions(where_str)
        
        return query
    
    def _parse_conditions(self, where_str):
        conditions = []
   
        parts = re.split(r'\s+(AND|OR)\s+', where_str, flags=re.I)
        logic = 'AND'

        pattern = r"""(\w+)\s*(=|!=|>=|<=|>|<)\s*('[^']*'|"[^"]*"|\d+\.?\d*)"""
        
        for part in parts:
            if part.upper() in ['AND', 'OR']:
                logic = part.upper()
                continue
            
            match = re.search(pattern, part.strip())
            if match:
                col, op, val = match.groups()
                val = val.strip("'\"")
                conditions.append((col, op, val, logic))
                logic = 'AND'
        
        return conditions

"""CLI接口测试"""
if __name__ == '__main__':
    parser = Parser()
    
    print("=" * 60)
    print("  SQL解析器测试")
    print("=" * 60)
    
    tests = [
        "SELECT * FROM sales",
        "SELECT product, price FROM sales WHERE price > 1000",
        "SELECT * FROM sales WHERE region = '北京' AND price > 500",
        "SELECT * FROM sales WHERE region = '北京' OR region = '上海'",
        "SELECT * FROM sales WHERE price > 1000 ORDER BY price DESC",
        "SELECT AVG(price) FROM sales WHERE status = '已签收'",
        "SELECT COUNT(*) FROM sales",
    ]
    
    for sql in tests:
        print(f"\nSQL: {sql}")
        result = parser.parse(sql)
        print(f"  解析结果: {result}")
    
    print("\n测试完成!")