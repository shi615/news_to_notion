# 概要
自分の見たい記事・ニュースなどをNotionのデータベースにまとめてくれる自動化ツールである。

## 実際のNotionデータベース画面
![alt text](images/notion_database.png)

# 目的
- 毎日に記事・ニュースを見る習慣をつけたい
- 気になる記事・ニュースだけを見たい

# 使い方
## pythonの仮想環境venvの構築
1. 本リポジトリのホームディレクトリに移動する。
2. `python -m venv env`を実行する。
3. `source env/bin/activate`を実行して仮想環境を起動する。
4. `pip install feedparser requests`を実行して必要なライブラリをインストールする。

## ジョブスケジューリングツールcrontabの時間設定
定時で自動的に記事・ニュースを取ってくれるための設定である。

1. `crontab -e`を実行する。
2. 表示してくれたファイルの一番下に以下の1行を追加する。
    ```
    0 7 * * * /bin/bash /path_to_your_repository/run_script.sh
    ```
    
    「分 時 日 月 曜日 bashパス コマンド」

    ここでは、毎日の`7`時`0`分に自動的に`bash`で`run_script.sh`を実行するとなっている。
3. 保存する。

## その他
後ほど更新する。