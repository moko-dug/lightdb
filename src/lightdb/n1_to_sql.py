"""
自然语言转SQL接口
支持两种模式：
1. 本地规则匹配（无需API，离线可用）
2. OpenAI API（需密钥，效果更好）
"""
import re


class NLToSQL:
    def __init__(self, mode='local', api_key=None):
        """
        mode: 'local' 基于规则 | 'openai' 使用GPT
        """
        self.mode = mode
        self.api_key = api_key
        
        # 表结构描述
        self.schema = """
表名: sales
列:
  - id: 订单编号
  - product: 商品名称
  - price: 单价
  - quantity: 数量
  - total: 总销售额
  - region: 地区（北京、上海、广州、深圳、杭州、成都、武汉、南京）
  - status: 状态（已签收、运输中、待发货、已退货）
  - date: 日期（格式：2024-MM-DD）
"""
    
    def convert(self, nl_query):
        """自然语言转SQL"""
        if self.mode == 'openai' and self.api_key:
            return self._convert_openai(nl_query)
        else:
            return self._convert_local(nl_query)
    
    def _convert_local(self, nl_query):
        """基于规则匹配转换（本地离线）"""
        nl = nl_query.lower()
        sql = "SELECT "
        
        # ===== 1. 检测聚合函数 =====
        if any(w in nl for w in ['平均', 'avg']):
            if '价格' in nl or 'price' in nl:
                sql = "SELECT AVG(price)"
            elif '销售额' in nl or '总额' in nl or 'total' in nl:
                sql = "SELECT AVG(total)"
            elif '数量' in nl or 'quantity' in nl:
                sql = "SELECT AVG(quantity)"
            else:
                sql = "SELECT AVG(total)"
        elif any(w in nl for w in ['总和', '总销售额', '总金额', 'sum', '加起来', '一共']):
            if '价格' in nl or 'price' in nl:
                sql = "SELECT SUM(price)"
            else:
                sql = "SELECT SUM(total)"
        elif any(w in nl for w in ['最大', '最高', 'max', '最大值']):
            if '价格' in nl or 'price' in nl:
                sql = "SELECT MAX(price)"
            else:
                sql = "SELECT MAX(total)"
        elif any(w in nl for w in ['最小', '最低', 'min', '最小值']):
            if '价格' in nl or 'price' in nl:
                sql = "SELECT MIN(price)"
            else:
                sql = "SELECT MIN(total)"
        elif any(w in nl for w in ['数量', '多少', '几个', '个数', 'count', '统计', '计数']):
            sql = "SELECT COUNT(*)"
        else:
            sql = "SELECT *"
        
        sql += " FROM sales"
        
        # ===== 2. 检测WHERE条件 =====
        conditions = []
        
        # 地区
        regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京']
        for region in regions:
            if region in nl_query:
                conditions.append(f"region = '{region}'")
        
        # 状态
        statuses = ['已签收', '运输中', '待发货', '已退货']
        for status in statuses:
            if status in nl_query:
                conditions.append(f"status = '{status}'")
        
        # 商品名
        products = ['手机', '笔记本电脑', '平板', '耳机', '智能手表', '键盘', '鼠标', '显示器', '充电器', '音箱']
        for product in products:
            if product in nl_query:
                conditions.append(f"product = '{product}'")
        
        # 价格/金额比较
        # 匹配: 大于/小于/等于 + 数字
        price_patterns = [
            (r'(?:价格|销售额|金额|price|total)\s*(?:大于|超过|高于|>)\s*(\d+)', '>'),
            (r'(?:价格|销售额|金额|price|total)\s*(?:小于|低于|<)\s*(\d+)', '<'),
            (r'(?:价格|销售额|金额|price|total)\s*(?:大于等于|>=|不小于|不低于)\s*(\d+)', '>='),
            (r'(?:价格|销售额|金额|price|total)\s*(?:小于等于|<=|不大于|不超过)\s*(\d+)', '<='),
            (r'(?:价格|销售额|金额|price|total)\s*(?:等于|=|是|为)\s*(\d+)', '='),
        ]
        
        col_to_use = 'total'
        if '价格' in nl_query or 'price' in nl_query:
            col_to_use = 'price'
        elif '数量' in nl_query or 'quantity' in nl_query:
            col_to_use = 'quantity'
        
        for pattern, op in price_patterns:
            match = re.search(pattern, nl)
            if match:
                val = match.group(1)
                conditions.append(f"{col_to_use} {op} {val}")
                break
        
        # 检测: 大于/超过/小于/低于 + 数字（不带列名）
        if not conditions or all('=' not in c for c in conditions):
            for pattern, op in [(r'(?:大于|超过|高于)\s*(\d+)', '>'), 
                               (r'(?:小于|低于)\s*(\d+)', '<')]:
                match = re.search(pattern, nl)
                if match:
                    val = match.group(1)
                    conditions.append(f"{col_to_use} {op} {val}")
                    break
        
        # 组装WHERE
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        # ===== 3. 检测排序 =====
        if any(w in nl for w in ['降序', '从高到低', '从大到小', 'desc', '最高', '最大']):
            if '价格' in nl or 'price' in nl:
                sql += " ORDER BY price DESC"
            else:
                sql += " ORDER BY total DESC"
        elif any(w in nl for w in ['升序', '从低到高', '从小到大', 'asc']):
            if '价格' in nl or 'price' in nl:
                sql += " ORDER BY price ASC"
            else:
                sql += " ORDER BY total ASC"
        
        return sql
    
    def _convert_openai(self, nl_query):
        """使用OpenAI API转换"""
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""数据库表结构：
{self.schema}

请将以下自然语言查询转换为SQL语句。只返回SQL，不要解释。

自然语言：{nl_query}

SQL："""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            sql = response.choices[0].message.content.strip()
            # 去掉可能的markdown代码块标记
            sql = sql.replace('```sql', '').replace('```', '').strip()
            return sql
            
        except ImportError:
            print("⚠️ OpenAI库未安装，使用本地规则转换")
            return self._convert_local(nl_query)
        except Exception as e:
            print(f"⚠️ API调用失败: {e}，使用本地规则转换")
            return self._convert_local(nl_query)


# ========== 测试用例 ==========
if __name__ == '__main__':
    import sys
    sys.path.append('.')
    from src.lightdb.parser import Parser
    from src.lightdb.engine import QueryEngine
    
    nl = NLToSQL(mode='local')
    parser = Parser()
    engine = QueryEngine('data')

    print("  自然语言查询接口 - 测试用例")
    
    # 10个测试用例
    test_cases = [
        "查询销售额大于 1000 的所有订单",
        "统计北京地区的订单数量",
        "计算已签收订单的平均销售额",
        "查询价格大于5000的商品",
        "查询广州地区销售额最高的一批订单",
        "统计耳机类商品的总销售额",
        "查询上海地区已退货的订单",
        "查询销售额小于500的订单",
        "计算所有订单的最大销售额",
        "查询成都地区销售额大于2000且已签收的订单",
    ]
    
    print(f"\n{'序号':<5} {'自然语言查询':<40} {'生成SQL':<50} {'执行结果':<20}")
    print("=" * 120)
    
    for i, nl_query in enumerate(test_cases, 1):
        try:
            # 自然语言 → SQL
            sql = nl.convert(nl_query)
            
            # SQL → 执行
            parsed = parser.parse(sql)
            result = engine.execute(parsed)
            
            # 格式化结果
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict):
                    # 聚合结果
                    if any(k.startswith(('COUNT', 'SUM', 'AVG', 'MAX', 'MIN')) for k in result[0].keys()):
                        result_str = ', '.join([f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" for k, v in result[0].items()])
                    else:
                        result_str = f"返回 {len(result)} 行"
                else:
                    result_str = f"返回 {len(result)} 行"
            else:
                result_str = "空结果"
            
            print(f"{i:<5} {nl_query:<40} {sql:<50} {result_str:<20}")
            
        except Exception as e:
            print(f"{i:<5} {nl_query:<40} {'ERROR':<50} {str(e):<20}")
    
    print(" 测试完成!")