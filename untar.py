import tarfile
import json
import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_json(json_path):
    try:
        if '_summarize' in json_path:
            return False
        else:
            summary_file = Path(str(json_path).replace('.json', '_summarize.json'))
            if summary_file.exists():
                logging.debug(f"跳过已处理的文件: {json_path}")
                return False
            else:
                return True
    except Exception as e:
        logging.error(f"处理文件时出错: {str(e)}")
        return False


def move_json(json_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    should_move = False
    for file in os.listdir(json_dir):
        if file.endswith('.json'):
            should_move = process_json(os.path.join(json_dir, file))
            if should_move:
                shutil.move(os.path.join(json_dir, file), os.path.join(output_dir, file))
                logging.info(f"已移动: {file}") 

# def process_tar(tar_path, output_dir):
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     if not os.path.exists(tar_path):
#         logging.error(f"文件不存在: {tar_path}")
#         return
    
#     try:
#         with tarfile.open(tar_path, 'r:gz') as tar:
#             for member in tar:
#                 member_name = member.name
#                 should_extract = False
#                 if member_name.endswith('.json'):
#                     should_extract = process_json(member_name)
#                 if should_extract:
#                     tar.extract(member, output_dir)
#                     logging.info(f"已提取: {member_name}")
#     except Exception as e:
#         logging.error(f"处理文件时出错: {str(e)}")

if __name__ == '__main__':
    move_json('cards-json\cards', 'cards-json-processed')
