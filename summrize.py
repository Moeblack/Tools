import os
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Union, Optional
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DescriptionProcessor:
    def __init__(self, api_url: str, max_concurrent: int = 5):
        self.api_url = api_url
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.error_messages = []

    async def process_single_file(self, file_path: Union[str, Path]) -> Union[bool, str]:
        try:
            # 跳过_summarize文件
            if '_summarize' in str(file_path):
                return False

            # 检查是否已存在summarize文件
            summary_file = Path(str(file_path).replace('.json', '_summarize.json'))
            if summary_file.exists():
                logging.debug(f"跳过已处理的文件: {file_path}")
                return False

            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查是否需要处理
            if 'data' not in data:
                return False

            card_data = data['data']
            if not card_data.get('description'):
                return False

            async with self.semaphore:
                # 调用API获取新的描述
                async with aiohttp.ClientSession() as session:
                    try:
                        request_data = {
                            "text": card_data['description'],
                            "prefix": "Generate a concise character introduction based on the following keywords, with a minimum length of 50-150 token:\n",
                            "suffix": "\nEnsure the sentence is fluent and easy to understand, and make it as concise as possible without changing the original meaning"
                        }
                        
                        async with session.post(self.api_url, json=request_data) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                raise Exception(f"API错误 ({response.status}): {error_text}")

                            result = await response.json()
                            new_description = result.get('summary', '')

                            if not new_description:
                                return False

                            # 生成同名的summarize.json文件
                            summary_file = Path(str(file_path).replace('.json', '_summarize.json'))
                            with open(summary_file, 'w', encoding='utf-8') as f:
                                json.dump(result, f, ensure_ascii=False, indent=2)

                            return True
                    except aiohttp.ClientError as e:
                        raise Exception(f"API请求失败: {str(e)}")

        except Exception as e:
            return f"{os.path.basename(str(file_path))}: 处理失败: {str(e)}"

    async def process_directory(self, directory: Union[str, Path], limit: Optional[int] = None):
        directory = Path(directory)
        # 只获取不包含_summarize的json文件
        json_files = [f for f in directory.rglob("*.json") if '_summarize' not in str(f)]
        if limit:
            json_files = json_files[:limit]

        lock = asyncio.Lock()
        pbar = tqdm(total=len(json_files), unit="个", ncols=80)

        success_count = 0
        tasks = []
        for file_path in json_files:
            tasks.append(self.process_single_file(file_path))

        for coro in asyncio.as_completed(tasks):
            result = await coro
            async with lock:
                pbar.update(1)
            if result is True:
                success_count += 1
            elif result is False:
                pass
            else:
                self.error_messages.append(result)
                async with lock:
                    tqdm.write(f"错误: {result}")

        pbar.close()

        with open('error_log.txt', 'w', encoding='utf-8') as f:
            for msg in self.error_messages:
                f.write(f"{msg}\n")

        logging.info(f"处理完成: 成功更新 {success_count} 个文件，共 {len(json_files)} 个文件")

async def main():
    api_url = "http://10.0.0.63:8086/api/summarize"
    target_path = "cards-json-processed"
    max_concurrent = 1

    processor = DescriptionProcessor(api_url, max_concurrent=max_concurrent)

    if os.path.isfile(target_path):
        with tqdm(total=1, desc="处理单个文件", ncols=80) as pbar:
            result = await processor.process_single_file(target_path)
            pbar.update(1)
            if result is True:
                logging.info("处理完成: 成功")
            elif result is False:
                logging.info("处理完成: 已跳过")
            else:
                logging.error(f"处理失败: {result}")
                tqdm.write(f"错误: {result}")
    else:
        await processor.process_directory(target_path)

if __name__ == "__main__":
    asyncio.run(main())