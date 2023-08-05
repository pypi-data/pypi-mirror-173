
# タグ情報をベクトル特徴量に変換 [tags2vec]

import sys
import numpy as np
from sout import sout

# 全タグの列挙
def listup_tags(train_tags):
	tags_dic = {}
	for rec in train_tags:
		for tag in rec:
			# 登録
			tags_dic[tag] = True
	# リストに変換
	tags_info = list(tags_dic)
	return tags_info

# タグ情報 -> ベクトル (学習時) [tags2vec]
def train_tr(train_tags):
	# 全タグの列挙
	tags_info = listup_tags(train_tags)
	# 学習時の変換もここからは推論時と同様
	train_x = pred_tr(train_tags, tags_info)	# タグ情報 -> ベクトル (推論時) [tags2vec]
	return train_x, tags_info

# タグ情報 -> ベクトル (推論時) [tags2vec]
def pred_tr(test_tags, tags_info):
	# タグをidxに直す辞書を作成 (高速な引き当てのため)
	tag_idx_dic = {tag: idx
		for idx, tag in enumerate(tags_info)}
	# 規模の確定
	data_n = len(test_tags)
	tags_n = len(tags_info)
	# ベースとなるゼロ行列の作成
	test_x = np.zeros((data_n, tags_n))
	# 「1」値を登録
	for rec_idx, rec in enumerate(test_tags):
		for tag in rec:
			# 学習時に存在しなかったタグは無視する
			if tag not in tag_idx_dic: continue
			# タグidxを引き当て・登録
			tag_idx = tag_idx_dic[tag]
			test_x[rec_idx, tag_idx] = 1
	return test_x
