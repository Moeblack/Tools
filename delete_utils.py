import os
import shutil

def delete_duplicates(input_folder, compare_folder):
    """
    检测两个文件夹中的重名文件,删除input_folder中的重名文件
    
    Args:
        input_folder: 需要检查和删除重复文件的文件夹路径
        compare_folder: 用于比较的文件夹路径
    """
    # 获取两个文件夹中的所有文件名
    input_files = set(os.listdir(input_folder))
    compare_files = set(os.listdir(compare_folder))
    
    # 找出重复的文件名
    duplicate_files = input_files.intersection(compare_files)
    
    # 删除重复文件
    deleted_count = 0
    for filename in duplicate_files:
        try:
            file_path = os.path.join(input_folder, filename)
            os.remove(file_path)
            deleted_count += 1
            print(f"已删除重复文件: {filename}")
        except Exception as e:
            print(f"删除文件 {filename} 时出错: {str(e)}")
    
    print(f"处理完成,共删除了 {deleted_count} 个重复文件")

if __name__ == '__main__':
    input_folder = r"D:\Project\Tools\cards"  # 需要检查的文件夹
    compare_folder = r"D:\Project\Tools\extracted_females\cards"  # 用于比较的文件夹
    delete_duplicates(input_folder, compare_folder)
