import os
import json
import shutil

def check_description_and_move(input_dir, output_dir):
    """
    检查文件夹中的json文件,如果description为'Creator\'s notes go here.'则移动到指定文件夹
    
    Args:
        input_dir: 输入文件夹路径
        output_dir: 输出文件夹路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 计数器
    moved_count = 0
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 检查description是否为目标字符串
                    if data.get('description') == "Creator's notes go here.":
                        # 构建目标文件路径
                        dest_path = os.path.join(output_dir, filename)
                        
                        # 移动文件
                        shutil.copy(file_path, dest_path)
                        moved_count += 1
                        print(f"已移动文件: {filename}")
                        
            except json.JSONDecodeError:
                print(f"无法解析JSON文件: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
    
    print(f"处理完成,共移动了 {moved_count} 个文件到 {output_dir}")

if __name__ == '__main__':
    input_dir = r"D:\Project\extracted_females\females_json"  # 输入文件夹路径
    output_dir = r"D:\Project\extracted_females\no_des"  # 输出文件夹路径
    check_description_and_move(input_dir, output_dir)
