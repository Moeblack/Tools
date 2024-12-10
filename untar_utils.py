import os
import tarfile
import json

def extract_unique_files(tar_path, compare_folders, output_dir):
    """
    从tar.gz文件中提取不在比较文件夹中的json文件
    
    Args:
        tar_path: tar.gz文件路径
        compare_folders: 用于比较的文件夹路径列表
        output_dir: 输出文件夹路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取比较文件夹中的所有文件名
    existing_files = set()
    for folder in compare_folders:
        if os.path.exists(folder):
            existing_files.update(os.listdir(folder))
    
    # 计数器
    extracted_count = 0
    
    # 流式读取tar文件
    with tarfile.open(tar_path, 'r:gz') as tar:
        for member in tar:
            if member.name.endswith('.json'):
                filename = os.path.basename(member.name)
                
                # 检查文件是否已存在
                if filename not in existing_files:
                    try:
                        tar.extract(member, output_dir)
                        extracted_count += 1
                        print(f"已提取文件: {filename}")
                    except Exception as e:
                        print(f"提取文件 {filename} 时出错: {str(e)}")
    
    print(f"处理完成,共提取了 {extracted_count} 个新文件到 {output_dir}")

if __name__ == '__main__':
    tar_path = r"C:\Users\Moeblack\Downloads\Compressed\females_json.tar.gz"
    compare_folders = [
        r"D:\Project\extracted_females\females_json",
        r"D:\Project\extracted_females\no_des"
    ]
    output_dir = r"D:\Project\extracted_females\new_files"
    extract_unique_files(tar_path, compare_folders, output_dir)
