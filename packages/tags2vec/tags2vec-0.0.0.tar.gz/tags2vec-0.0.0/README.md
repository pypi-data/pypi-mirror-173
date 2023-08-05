# json_stock

下の方に日本語の説明があります

## Overview
- A tool that converts information such as tags in multiple strings into features in the form of vectors with 1s and 0s as elements

## Usage
```python
import tags2vec

# Convert training data
train_tags = [
	["Spicy", "Red", "Delicious"],
	["Sweet", "Green"]
]
# Convert training data Tag info -> Vector (training) [tags2vec]
train_x, tags_info = tags2vec.train_tr(train_tags)
"""
train_x (numpy array):
[[1. 1. 1. 0. 0.]
 [0. 0. 0. 1. 1.]]

tags_info: ["Spicy", "Red", "Delicious", "Sweet", "Green"]
"""

# Convert test data
test_tags = [
	["Sweet", "Red", "Delicious"],
	["Spicy", "Yellow"],
]
# Tag info -> Vector (prediction) [tags2vec]
test_x = tags2vec.pred_tr(test_tags, tags_info)
"""
test_x (numpy array):
[[0. 1. 1. 1. 0.]
 [1. 0. 0. 0. 0.]]
"""
```

## detailed explanation
- This tool is designed for pre-processing of supervised learning.
	- The vector output is therefore a numpy matrix.
- During the training phase, a list of tag information is output in the form of tags_info variables
- During the prediction phase, a vector is generated based on the tags_info information (list of tags and their order)
	- This ensures that prediction is consistent with the training phase
- If a tag appears during prediction that was not present during training, it is ignored



## 概要
- タグ情報をベクトル特徴量に変換するツール
- 具体的には、複数の文字列のタグのような情報を、1と0を要素として持つベクトルの形の特徴量に変換するツール

## 使用例
```python
import tags2vec

# 学習データの変換
train_tags = [
	["Spicy", "Red", "Delicious"],
	["Sweet", "Green"]
]
# タグ情報 -> ベクトル (学習時) [tags2vec]
train_x, tags_info = tags2vec.train_tr(train_tags)
"""
train_x (numpy array):
[[1. 1. 1. 0. 0.]
 [0. 0. 0. 1. 1.]]

tags_info: ["Spicy", "Red", "Delicious", "Sweet", "Green"]
"""

# 推論データの変換
test_tags = [
	["Sweet", "Red", "Delicious"],
	["Spicy", "Yellow"],
]
# タグ情報 -> ベクトル (推論時) [tags2vec]
test_x = tags2vec.pred_tr(test_tags, tags_info)
"""
test_x (numpy array):
[[0. 1. 1. 1. 0.]
 [1. 0. 0. 0. 0.]]
"""
```

## 詳細説明
- このツールは教師あり学習の前処理を想定して作られています
	- そのため、ベクトルの出力はnumpy行列で出力されます
- 学習のフェーズでタグ情報の一覧がtags_info変数の形で出力されます
- 推論フェーズでは、tags_infoの情報 (タグ一覧とその順序) にもとづいてベクトルが生成されます
	- これによって、学習時と一貫した推論を行うことができます
- 学習時に存在しなかったタグが推論時に現れた場合は、そのタグは無視されます
