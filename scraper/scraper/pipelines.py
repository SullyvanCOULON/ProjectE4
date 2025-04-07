import json
import os
from itemadapter import ItemAdapter

class JsonExportPipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if os.path.exists('output/data.json'):
            os.remove('output/data.json')
        self.file = open('output/data.json', 'w', encoding='utf-8')
        self.file.write('[\n')  
        self.first_item = True

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        json_line = json.dumps(adapter.asdict(), ensure_ascii=False, indent=4)
        if not self.first_item:
            self.file.write(',\n')
        self.file.write(json_line)
        self.first_item = False
        return item
