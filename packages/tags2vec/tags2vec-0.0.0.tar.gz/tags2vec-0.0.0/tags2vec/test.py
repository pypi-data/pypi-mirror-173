
# タグ情報をベクトル特徴量に変換 [tags2vec]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
# タグ情報をベクトル特徴量に変換 [tags2vec]
tags2vec = load_develop("tags2vec", "../", develop_flag = True)

# 学習データの変換
train_tags = [
	["Spicy", "Red", "Delicious"],
	["Sweet", "Green"]
]
# タグ情報 -> ベクトル (学習時) [tags2vec]
train_x, tags_info = tags2vec.train_tr(train_tags)
# debug
sout(train_x)
sout(tags_info)

# 推論データの変換
test_tags = [
	["Sweet", "Red", "Delicious"],
	["Spicy", "Yellow"],
]
# タグ情報 -> ベクトル (推論時) [tags2vec]
test_x = tags2vec.pred_tr(test_tags, tags_info)
# debug
sout(test_x)
