import json
import tiktoken

def should_extract_json(json_data):
    """
    测试json数据是否符合提取条件
    
    条件：
    1. topics为空或少于3项
    2. description不存在
    3. description的token数少于50
    """
    if not isinstance(json_data, dict) or 'data' not in json_data:
        print("无效的JSON格式：缺少'data'字段")
        return False
    
    data = json_data['data']
    
    # 检查topics
    if 'tags' not in data:
        print("符合条件：没有topics字段")
        return True
    
    if len(data['tags']) < 3:
        print(f"符合条件：topics数量少于3 (当前数量: {len(data['topics'])})")
        return True
        
    # 检查description
    if 'description' not in data:
        print("符合条件：没有description字段")
        return True
        
    # 检查description的token数
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    desc_tokens = len(enc.encode(data['description']))
    if desc_tokens < 50:
        print(f"符合条件：description的token数少于50 (当前token数: {desc_tokens})")
        return True
    
    print("不符合任何提取条件")
    return False

def test_json_file(file_path):
    """测试指定的json文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            result = should_extract_json(data)
            print(f"\n文件 {file_path} {'应该' if result else '不应该'}被提取")
            return result
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return False

if __name__ == '__main__':
    # 测试实际文件
    test_json_file("117.json")