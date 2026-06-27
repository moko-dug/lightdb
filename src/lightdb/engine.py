"""
轻量级查询引擎
"""
import csv
import os
from .filters import filter_data
from .aggregates import aggregate
from .sorter import sort_data
from .projection import project_columns


class QueryEngine:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
    
    def load_table(self, table_name):
    
        filepath = os.path.join(self.data_dir, f'{table_name}.csv')
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def execute(self, query):
        """执行解析后的查询"""
        from src.lightdb.filters import filter_data
        from src.lightdb.aggregates import aggregate
        from src.lightdb.sorter import sort_data
        from src.lightdb.projection import project_columns
        

        data = self.load_table(query['table'])
        
        if query.get('conditions'):
            data = filter_data(data, query['conditions'])
        
        if query.get('aggregations'):
            results = {}
            for func, col in query['aggregations']:
                if func == 'COUNT' and col == '*':
                    results['COUNT(*)'] = len(data)
                else:
                    results[f'{func}({col})'] = aggregate(data, func, col)
            return [results]
    
        if query.get('order_by'):
            ascending = query.get('order_dir', 'ASC').upper() == 'ASC'
            data = sort_data(data, query['order_by'], ascending)
    
        if query.get('columns'):
            data = project_columns(data, query['columns'])
        
        return data