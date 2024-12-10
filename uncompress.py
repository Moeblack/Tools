import os
import tarfile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def uncompress_file(input_file: str, output_dir: str = None) -> str:
    """
    解压tar.gz格式的文件
    
    Args:
        input_file: 要解压的文件路径
        output_dir: 解压输出目录,如果为None则解压到当前目录
        
    Returns:
        str: 解压后的目录路径
    """
    try:
        # 如果未指定输出目录,则使用当前目录
        if output_dir is None:
            output_dir = os.path.dirname(input_file)
            
        # 解压tar.gz文件
        with tarfile.open(input_file, "r:gz") as tar:
            tar.extractall(path=output_dir)
            
        logging.info(f"成功解压文件 {input_file} 到 {output_dir}")
        return output_dir
        
    except Exception as e:
        logging.error(f"解压文件时出错: {str(e)}")
        raise

if __name__ == '__main__':
    # 示例用法
    input_file = "output.tar.gz" 
    output_dir = "extracted_females_processed"
    uncompress_file(input_file, output_dir)
