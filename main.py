import tarfile
import rarfile
import json
import os
from pathlib import Path

def process_archive(archive_path, output_dir):
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"开始处理文件: {archive_path}")
    
    # 根据文件扩展名选择appropriate的处理方法
    if archive_path.lower().endswith('.tar.gz'):
        process_tar(archive_path, output_dir)
    elif archive_path.lower().endswith('.rar'):
        process_rar(archive_path, output_dir)
    elif archive_path.lower().endswith('.json'):
        process_json(archive_path, output_dir)
    else:
        print("不支持的文件格式。目前只支持.tar.gz、.rar和.json文件。")

def process_json(json_path, output_dir):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # 检查topics是否为空
                if 'data' in data and ('topics' not in data['data'] or not data['data']['topics']):
                    # 复制文件到输出目录
                    output_path = os.path.join(output_dir, os.path.basename(json_path))
                    import shutil
                    shutil.copy2(json_path, output_path)
                    print(f"已复制: {json_path} 到 {output_path}")
                    return 1
                else:
                    print(f"文件 {json_path} 包含topics，已跳过")
                    return 0
            except json.JSONDecodeError:
                print(f"无法解析JSON文件: {json_path}")
                return 0
    except Exception as e:
        print(f"处理文件时出错 {json_path}: {str(e)}")
        return 0

def process_tar(tar_path, output_dir):
    with tarfile.open(tar_path, 'r:gz') as tar:
        print(f"tar文件中的所有文件:")
        tar.list()
        
        file_count = process_archive_members(tar, output_dir)
        print(f"处理完成，共找到 {file_count} 个符合条件的文件")

def process_rar(rar_path, output_dir):
    with rarfile.RarFile(rar_path) as rar:
        print(f"rar文件中的所有文件:")
        for item in rar.namelist():
            print(item)
        
        file_count = process_archive_members(rar, output_dir)
        print(f"处理完成，共找到 {file_count} 个符合条件的文件")

def process_archive_members(archive, output_dir):
    file_count = 0
    for member in archive.namelist() if isinstance(archive, rarfile.RarFile) else archive:
        member_name = member if isinstance(archive, rarfile.RarFile) else member.name
        print(f"正在处理: {member_name}")
        
        # 处理female文件夹中的所有json文件
        if os.path.dirname(member_name) == 'cards' or member_name.endswith('.json'):
            try:
                if isinstance(archive, rarfile.RarFile):
                    f = archive.open(member_name)
                else:
                    f = archive.extractfile(member)
                
                if f is not None:
                    try:
                        data = json.loads(f.read().decode('utf-8'))
                        should_extract = False
                        
                        if 'data' in data:
                            # 检查tags（之前是topics）
                            if 'tags' not in data['data'] or len(data['data']['tags']) < 3:
                                should_extract = True
                                print(f"{member_name}: tags少于3个或不存在")
                            
                            # 检查description
                            if 'description' not in data['data']:
                                should_extract = True
                                print(f"{member_name}: 没有description")
                            else:
                                import tiktoken
                                enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
                                desc_tokens = len(enc.encode(data['data']['description']))
                                if desc_tokens < 50:
                                    should_extract = True
                                    print(f"{member_name}: description token数少于50")
                        
                        if should_extract:
                            archive.extract(member_name if isinstance(archive, rarfile.RarFile) else member, output_dir)
                            file_count += 1
                            print(f"已提取: {member_name}")
                    except json.JSONDecodeError:
                        print(f"无法解析JSON文件: {member_name}")
                    finally:
                        f.close()
            except Exception as e:
                print(f"处理文件时出错 {member_name}: {str(e)}")
    
    return file_count

if __name__ == '__main__':
    archive_path = r"D:\Tencent Files\WeChat Files\wxid_o39zyo52lr1w22\FileStorage\File\2024-11\cards.tar.gz"  # 或者 .rar 文件
    output_dir = 'extracted_females'
    process_archive(archive_path, output_dir)
