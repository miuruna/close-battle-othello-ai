# 接戦を演出し最終的に勝利するAI-Othello
Minimax法を応用したBayes-Even法により評価値を定数に近づけるプログラム
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red?style=for-the-badge&logo=streamlit)

情報システム工学PBLという授業内で作成したオセロAIのソースコードです
ベイズ推定を用いて相手の強さを推定しながら指す手を選択します

## 開発者
[![Nanako-75-hub](https://img.shields.io/badge/Nanako-75-hub-121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nanako-75-hub)
[![nao0106](https://img.shields.io/badge/nao0106-121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nao0106)
[![miuruna](https://img.shields.io/badge/miuruna-121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/miuruna)

Othello Arena用のPythonプログラム: https://github.com/KousukeIshii/OthelloArenaPython

## [仕様書](docs/SPECIFICATION.md)

## 実行方法
インストールが必要なライブラリは`requirments.txt`にあるため仮想環境を作成してインストールすること

### オセロAIのみを実行する
```bash
python Play.py
```
### ダッシュボードのみを実行する
```bash
streamlit run dashboard/live.py
```
### オセロAIを実行しリアルタイムで実行状況を監視する
```bash
python run.py
```
