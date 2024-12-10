
'''
###
我来总结一下这个项目中的主要知识点，并设计相关练习题。

### 一、基础知识点总结

1. **文件操作**
- 文件的读写（open, read, write）
- 文件路径处理（os.path, Path）
- JSON文件处理（json.load, json.dump）
- 压缩文件处理（tarfile）

2. **异步编程** 
- asyncio基础
- async/await语法
- 并发控制（Semaphore）
- 异步HTTP请求（aiohttp）

3. **面向对象编程**
- 类的定义和使用
- 构造函数
- 类方法

4. **错误处理**
- try/except异常处理
- 日志记录（logging）

5. **类型注解**
- 类型提示（typing模块）
- Optional, Union等类型

### 二、练习题

#### 1. 基础文件操作
```python
"""
练习1：创建一个函数，实现以下功能：
1. 读取一个文本文件
2. 统计文件中每个单词出现的次数
3. 将结果写入新的JSON文件
"""
'''


def count_words(input_file: str, output_file: str) -> dict:
    words_dict = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_words_list = f.read().lower().split()
    for word in raw_words_list:
        if word not in words_dict:
            words_dict[word] = 1
        else:
            words_dict[word] += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words_dict, f)

# 测试用例
# 输入文件内容: "hello world hello python"
# 预期输出JSON: {"hello": 2, "world": 1, "python": 1}


"""
练习2：创建一个函数，实现以下功能：
1. 读取一个JSON文件，文件包含学生信息列表
2. 根据学生成绩进行排序
3. 将排序后的结果写入新文件
"""

def sort_students(input_file: str, output_file: str) -> None:
    # 请实现此函数
    pass

# 测试数据示例：
# {
#   "students": [
#     {"name": "Tom", "score": 85},
#     {"name": "Jerry", "score": 92},
#     {"name": "Mike", "score": 78}
#   ]
# }
'''
#### 3. 异步编程基础
```python
"""
练习3：创建一个异步函数，实现以下功能：
1. 并发下载多个URL的内容
2. 限制最大并发数
3. 显示下载进度
"""
'''


async def download_urls(urls: list[str], max_concurrent: int = 3) -> list[str]:
    # 请实现此函数
    pass

# 测试用例
urls = [
    "http://example.com/1",
    "http://example.com/2",
    "http://example.com/3"
]
'''```

#### 4. 路径处理
```python
"""
练习4：创建一个函数，实现以下功能：
1. 递归遍历指定目录
2. 找出所有指定扩展名的文件
3. 返回文件的相对路径列表
"""'''

def find_files(directory: str, extension: str) -> list[str]:
    # 请实现此函数
    pass

'''# 测试用例
# find_files("./test_dir", ".txt")
```

#### 5. 错误处理和日志
```python
"""
练习5：创建一个函数，实现以下功能：
1. 处理文件操作可能出现的各种异常
2. 记录详细的错误日志
3. 实现优雅的错误恢复
"""'''

def safe_file_operation(file_path: str) -> bool:
    # 请实现此函数
    pass

'''# 测试各种异常情况：
# 1. 文件不存在
# 2. 权限不足
# 3. 磁盘空间不足
```

### 三、常用函数示例'''

'''1. **文件操作示例**：
```python'''
# 读取文件
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 写入文件
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello World')

# JSON操作
import json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
'''```

2. **路径处理示例**：
```python'''
from pathlib import Path

# 创建路径对象
path = Path('folder/subfolder/file.txt')

# 获取文件名
filename = path.name  # 'file.txt'

# 获取父目录
parent = path.parent  # 'folder/subfolder'

# 拼接路径
new_path = path.parent / 'newfile.txt'
'''```

3. **异步操作示例**：
```python'''
import asyncio

async def async_operation():
    await asyncio.sleep(1)
    return 'done'

# 运行异步函数
result = asyncio.run(async_operation())
'''```

4. **日志记录示例**：
```python
import logging'''

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('操作成功')
logging.error('发生错误')
'''```

这些练习题涵盖了项目中的主要知识点，建议按顺序完成，每个练习都包含了多个知识点的综合运用。完成这些练习后，你将能更好地理解和运用这个项目中的各种技术。'''