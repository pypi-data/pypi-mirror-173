#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/10/21 10:15
# @Author  : xgy
# @Site    : 
# @File    : transform.py
# @Software: PyCharm
# @python version: 3.7.13
"""
import json
import os

from csp.common.utils import check_jsonl
from loguru import logger


def std_doccano(data_folder, output):
    os.makedirs(output, exist_ok=True)
    st_data, file_name = check_jsonl(data_folder)

    doccano_data = []
    for item in st_data:
        id = item["id"]
        text = item["text"]
        tags = item["tags"]
        doccano_item = {"id": id, "text": text, "entities": []}
        for index, tag in enumerate(tags):
            entity = {"id": index, "label": tag["category"], "start_offset": tag["start"] - 1,
                      "end_offset": int(tag["start"]) - 1 + len(tag["mention"])}
            doccano_item["entities"].append(entity)
            doccano_item["relations"] = []
        doccano_data.append(doccano_item)

    save_path = os.path.join(output, file_name)
    with open(save_path, "w", encoding="utf-8") as fw:
        for item in doccano_data:
            fw.write(json.dumps(item, ensure_ascii=False))
            fw.write("\n")
    logger.info("the result saved in {}".format(output))


if __name__ == '__main__':
    print("start")
