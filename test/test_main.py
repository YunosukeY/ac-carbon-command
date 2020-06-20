# -*- coding: utf-8 -*-

from unittest import TestCase
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.main import get_submission_id, get_soup, get_submission_code, get_language, get_lang_para, get_carbon_image, get_tweet_title

class TestFoo(TestCase):
  def test_get_submission_id(self):
    test_patterns = [
      ('https://atcoder.jp/contests/abc170/submissions/14465204', '14465204'),
      ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja', '14465204'),
      ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=en', '14465204'),
    ]
    for url, ans in test_patterns:
      with self.subTest(url=url, ans=ans):
        self.assertEqual(get_submission_id(url), ans)

  def test_get_submission_code(self):
    test_patterns = [
      ('https://atcoder.jp/contests/abc170/submissions/14465204'
      ,'''#include <bits/stdc++.h>\r
using namespace std;\r
#define rep(i, n) for (int i = 0, i##_cond = (n); i < i##_cond; ++i)\r
\r
int main() {\r
  rep(i, 5) {\r
    int a;\r
    cin >> a;\r
    if (a == 0)\r
      cout << i + 1 << endl;\r
  }\r
}''')
    ]
    for url, ans in test_patterns:
      with self.subTest(url=url, ans=ans):
        self.assertEqual(get_submission_code(get_soup(url), url), ans)

  def test_get_language(self):
    test_patterns = [
      ('https://atcoder.jp/contests/abc170/submissions/14386050', 'C (GCC 9.2.1)'),
      ('https://atcoder.jp/contests/abc170/submissions/14414384', 'C (Clang 10.0.0)'),
      ('https://atcoder.jp/contests/abc170/submissions/14465204', 'C++ (GCC 9.2.1)'),
      ('https://atcoder.jp/contests/abc170/submissions/14290048', 'C++ (Clang 10.0.0)'),
      ('https://atcoder.jp/contests/abc170/submissions/14298695', 'Java (OpenJDK 11.0.6)'),
      ('https://atcoder.jp/contests/abc170/submissions/14435034', 'Python (3.8.2)'),
      ('https://atcoder.jp/contests/abc170/submissions/14283850', 'Ruby (2.7.1)'),
      ('https://atcoder.jp/contests/abc170/submissions/14435215', 'C# (.NET Core 3.1.201)'),
      ('https://atcoder.jp/contests/abc170/submissions/14368206', 'PyPy3 (7.3.0)'),
      ('https://atcoder.jp/contests/abc170/submissions/14381674', 'Haskell (GHC 8.8.3)'),
      ('https://atcoder.jp/contests/abc170/submissions/14435774', 'Rust (1.42.0)')
    ]
    for url, ans in test_patterns:
      with self.subTest(url=url, ans=ans):
        self.assertEqual(get_language(get_soup(url), url), ans)

  def test_get_lang_para(self):
    test_patterns = [
      ('C (GCC 9.2.1)', 'text/x-csrc'),
      ('C (Clang 10.0.0)', 'text/x-csrc'),
      ('C++ (GCC 9.2.1)', 'text/x-c++src'),
      ('C++ (Clang 10.0.0)', 'text/x-c++src'),
      ('Java (OpenJDK 11.0.6)', 'text/x-java'),
      ('Python (3.8.2)', 'python'),
      ('Ruby (2.7.1)', 'ruby'),
      ('C# (.NET Core 3.1.201)', 'text/x-csharp'),
      ('PyPy3 (7.3.0)', 'python'),
      ('Haskell (GHC 8.8.3)', 'haskell'),
      ('Rust (1.42.0)', 'rust')
    ]
    for lang, ans in test_patterns:
      with self.subTest(lang=lang, ans=ans):
        self.assertEqual(get_lang_para(lang), ans)

  def test_get_tweet_title(self):
    test_patterns = [
      ('https://atcoder.jp/contests/abc170/submissions/14465204'
      ,'Submission #14465204 - AtCoder Beginner Contest 170 https://atcoder.jp/contests/abc170/submissions/14465204?lang=en'),
      ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja'
      ,'提出 #14465204 - AtCoder Beginner Contest 170 https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja'),
      ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=en'
      ,'Submission #14465204 - AtCoder Beginner Contest 170 https://atcoder.jp/contests/abc170/submissions/14465204?lang=en')
    ]
    for url, ans in test_patterns:
      with self.subTest(url=url, ans=ans):
        self.assertEqual(get_tweet_title(get_soup(url), url), ans)
