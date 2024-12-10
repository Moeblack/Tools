import os
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Union, Optional
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TagProcessor:
    def __init__(self, api_url: str, max_concurrent: int = 5):
        self.api_url = api_url
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.error_messages = []

    async def process_single_file(self, file_path: Union[str, Path]) -> Union[bool, str]:
        try:
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if processing is needed
            if 'data' not in data:
                return False

            card_data = data['data']
            if 'tags' in card_data and len(card_data['tags']) >= 3:
                return False

            async with self.semaphore:
                # Call the API to get new tags
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.post(self.api_url, json=card_data) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                raise Exception(f"API错误 ({response.status}): {error_text}")

                            result = await response.json()
                            new_tags = result.get('tags', [])

                            if not new_tags:
                                return False

                            # Update the JSON file
                            data['data']['tags'] = new_tags
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)

                            return True
                    except aiohttp.ClientError as e:
                        raise Exception(f"API请求失败: {str(e)}")

        except Exception as e:
            # Return the error message instead of printing it here
            return f"{os.path.basename(str(file_path))}: 处理失败: {str(e)}"

    async def process_directory(self, directory: Union[str, Path], limit: Optional[int] = None):
        directory = Path(directory)
        json_files = [f for f in directory.rglob("*.json") if "_summarize" not in str(f)]
        if limit:
            json_files = json_files[:limit]

        # Create a lock for synchronizing progress bar updates and writes
        lock = asyncio.Lock()

        # Initialize the progress bar
        pbar = tqdm(total=len(json_files), unit="个", ncols=80)

        success_count = 0
        tasks = []
        for file_path in json_files:
            tasks.append(self.process_single_file(file_path))

        # Process tasks as they complete
        for coro in asyncio.as_completed(tasks):
            result = await coro
            async with lock:
                pbar.update(1)
            if result is True:
                success_count += 1
            elif result is False:
                # Skipped files
                pass
            else:
                # It's an error message
                self.error_messages.append(result)
                async with lock:
                    tqdm.write(f"错误: {result}")

        pbar.close()

        # Write all error messages to a log file
        with open('error_log.txt', 'w', encoding='utf-8') as f:
            for msg in self.error_messages:
                f.write(f"{msg}\n")

        logging.info(f"处理完成: 成功更新 {success_count} 个文件，共 {len(json_files)} 个文件")

async def main():
    # Configuration
    api_url = "http://10.0.0.63:8086/api/tag"
    target_path = "extracted_females"
    max_concurrent = 8  # Control the concurrency

    processor = TagProcessor(api_url, max_concurrent=max_concurrent)

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
