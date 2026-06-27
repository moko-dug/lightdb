"""
命令行交互界面
"""
from .parser import Parser
from .engine import QueryEngine


def format_output(data, max_rows=20):
    if not data:
        return "空结果集"
    
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
        if any(k.startswith(('COUNT', 'SUM', 'AVG', 'MAX', 'MIN')) for k in data[0].keys()):
            return '\n'.join([f"  {k}: {v}" for k, v in data[0].items()])
    
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            columns = list(data[0].keys())
           
            widths = {}
            for col in columns:
                widths[col] = len(str(col))
                for row in data[:max_rows]:
                    widths[col] = max(widths[col], len(str(row.get(col, ''))))
           
            header = ' | '.join(str(col).ljust(widths[col]) for col in columns)
            separator = '-' * len(header)
     
            lines = [separator, header, separator]
            for row in data[:max_rows]:
                line = ' | '.join(str(row.get(col, '')).ljust(widths[col]) for col in columns)
                lines.append(line)
            lines.append(separator)
            
            result = '\n'.join(lines)
            if len(data) > max_rows:
                result += f"\n... 共 {len(data)} 行，显示前 {max_rows} 行"
            
            return result
    
    return str(data)


def main():
    parser = Parser()
    engine = QueryEngine('data')
    
    print("=" * 60)
    print("  LightDB - 轻量级数据库查询引擎")
    print("=" * 60)
    print("  输入SQL查询语句，输入 'exit' 退出")
    print("  示例: SELECT * FROM sales WHERE price > 5000")
    print("=" * 60)
    
    while True:
        try:
            sql = input("\ndb> ").strip()
            
            if sql.lower() in ['exit', 'quit', 'q']:
                print("再见！")
                break
            
            if not sql:
                continue

            parsed = parser.parse(sql)
            
            result = engine.execute(parsed)

            print()
            print(format_output(result))

            if isinstance(result, list):
                print(f"\n({len(result)} 行)")
            
        except KeyboardInterrupt:
            print("\n NO!")
            break
        except FileNotFoundError as e:
            print(f"表不存在: {e}")
        except Exception as e:
            print(f"错误: {e}")


if __name__ == '__main__':
    main()