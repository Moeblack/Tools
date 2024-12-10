import os
import tarfile
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compress_directory(input_dir: str, output_file: str = None, remove_source: bool = False) -> str:
    """
    将指定文件夹压缩为tar.gz格式
    
    Args:
        input_dir: 要压缩的文件夹路径
        output_file: 输出文件路径,如果为None则使用输入文件夹名称
        remove_source: 压缩后是否删除源文件夹
        
    Returns:
        str: 压缩文件的路径
    """
    try:
        # 如果未指定输出文件名,则使用输入文件夹名
        if output_file is None:
            output_file = os.path.basename(input_dir) + '.tar'
        
        output_path = os.path.join(os.path.dirname(os.path.dirname(input_dir)), output_file)
            
        # 创建tar文件
        with tarfile.open(output_path, "w") as tar:
            # 获取文件夹中的所有文件数量
            total_files = sum([len(files) for _, _, files in os.walk(input_dir)])
            processed_files = 0
            
            # 添加文件夹中的所有文件
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.join(os.path.basename(input_dir), os.path.relpath(file_path, input_dir))
                    tar.add(file_path, arcname=arcname)
                    processed_files += 1
                    # 显示进度
                    progress = (processed_files / total_files) * 100
                    print(f"\r压缩进度: {progress:.1f}% ({processed_files}/{total_files})", end="", flush=True)
            print()  # 换行
            
        logging.info(f"成功压缩文件夹 {input_dir} 为 {output_file}")
        
        # 压缩完成后删除源文件夹
        if remove_source:
            shutil.rmtree(input_dir)
            logging.info(f"已删除源文件夹 {input_dir}")
            
        return output_file
        
    except Exception as e:
        logging.error(f"压缩文件夹时出错: {str(e)}")
        raise

if __name__ == '__main__':
    # 示例用法
    input_dir = r"G:\AIGC\SD-WebUI"
    output_file = "done.tar"
    compress_directory(input_dir, output_file, remove_source=True)
