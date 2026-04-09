PROBLEM = {
    "title": "Longest Substring Without Repeating Characters",
    "description": "給定一個字串 s，請找出不含重複字元的最長子字串的長度。",
    "examples": [
        {
            "input": "abcabcbb",
            "output": 3,
            "explanation": '最長不重複子字串為 "abc"，長度為 3',
        },
        {
            "input": "bbbbb",
            "output": 1,
            "explanation": '最長子字串為 "b"，長度為 1',
        },
        {
            "input": "pwwkew",
            "output": 3,
            "explanation": '最長不重複子字串為 "wke"，長度為 3',
        },
    ],
    "starter_code": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 在此撰寫你的解法
        pass
""",
}

TEST_CASES = [
    # 基本測試
    {"index": 1,  "input": "abcabcbb",                   "expected": 3,  "is_stress": False},
    {"index": 2,  "input": "bbbbb",                      "expected": 1,  "is_stress": False},
    {"index": 3,  "input": "pwwkew",                     "expected": 3,  "is_stress": False},
    # 邊界條件
    {"index": 4,  "input": "",                           "expected": 0,  "is_stress": False},
    {"index": 5,  "input": "a",                          "expected": 1,  "is_stress": False},
    {"index": 6,  "input": "au",                         "expected": 2,  "is_stress": False},
    {"index": 7,  "input": "aa",                         "expected": 1,  "is_stress": False},
    # 進階測試
    {"index": 8,  "input": "abcdefg",                    "expected": 7,  "is_stress": False},
    {"index": 9,  "input": "dvdf",                       "expected": 3,  "is_stress": False},
    {"index": 10, "input": "anviaj",                     "expected": 5,  "is_stress": False},
    {"index": 11, "input": "tmmzuxt",                    "expected": 5,  "is_stress": False},
    {"index": 12, "input": "abba",                       "expected": 2,  "is_stress": False},
    {"index": 13, "input": "aab",                        "expected": 2,  "is_stress": False},
    # 特殊字元
    {"index": 14, "input": "a b",                        "expected": 3,  "is_stress": False},
    {"index": 15, "input": "!@#$%",                      "expected": 5,  "is_stress": False},
    {"index": 16, "input": " ",                          "expected": 1,  "is_stress": False},
    # 壓力測試
    {"index": 17, "input": "a" * 50000,                  "expected": 1,  "is_stress": True},
    {"index": 18, "input": "abcdefghijklmnopqrstuvwxyz", "expected": 26, "is_stress": False},
]
