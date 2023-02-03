import os
import unittest
import json

class TestMergeJson(unittest.TestCase):
    def setUp(self):
        self.examples = "examples"
        self.translations = "translations"
        
        if not os.path.exists(self.examples):
            os.mkdir(self.examples)
        if not os.path.exists(self.translations):
            os.mkdir(self.translations)
            
        example_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": {
                "key4": "value4",
                "key5": "value5"
            },
            "key10": {
                "key101": "value104",
                "key102": "value105"
            }
        }
        translation_data = {
            "key1": "value3",
            "obsolete": "obsolete",
            "key3": {
                "key4": "value14",
            },
            "key10": "str10"
        }
        self.expected_result = {
            "key1": "value3",
            "key2": "value2",
            "key3": {
                "key4": "value14",
                "key5": "value5"
            },
            "key10": {
                "key101": "value104",
                "key102": "value105"
            }
        }

        
        with open(os.path.join(self.examples, "file.json"), "w") as f:
            json.dump(example_data, f)
        with open(os.path.join(self.translations, "file.json"), "w") as f:
            json.dump(translation_data, f)
            
    def test_merge_json(self):
        from merge import merge_json
        merge_json(self.examples, self.translations)
        
        with open(os.path.join(self.translations, "file.json"), "r") as f:
            data = json.load(f)
            
        self.assertDictEqual(data, self.expected_result)
        
    def tearDown(self):
        os.remove(os.path.join(self.examples, "file.json"))
        os.remove(os.path.join(self.translations, "file.json"))
        os.rmdir(self.examples)
        os.rmdir(self.translations)
        
if __name__ == '__main__':
    unittest.main()
