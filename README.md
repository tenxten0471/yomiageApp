# yomiageApp
yomiageAppはweb上のテキスト(小説、ニュース)を[COEIROINK](https://coeiroink.com/)に読み上げてもらうアプリです。
動作確認はしていませんがapiはVOICEBOXと同様なはずなので、apiのurlのポート番号を変更することでVOICEBOXでも同様に使えるはずです。

## 使い方
アプリを起動させる前に[COEIROINK](https://coeiroink.com/)を起動させてください。
### アプリの起動
以下のコマンドを実行すると google chrome ブラウザ上で操作画面が立ち上がります。
```
python ./yomiageApp.py
```
### オプション
実行時にコマンドライン引数を設定することが出来ます。

##### min_block_length
取得したテキストを分割して音声を取得する際の最低文字数です。テキストは`min_block_length`以降の改行コードで分割されます。`-b`,`--min_block_length`で指定できます。デフォルトは200です。

##### window_size
アプリケーションモードで立ち上がるgoogle chromeのウィンドウサイズです。`-s <width> <height>`,`--window_size <width> <height>`で指定できます。デフォルトは、<width> = 768,<height> = 1024です。

##### port
[Eel](https://github.com/python-eel/Eel)で立ち上げるサーバーのポート番号です。`-p`,`--port`で指定できます。デフォルトは8000です。

##### mode
[Eel](https://github.com/python-eel/Eel)のオプションで使用するブラウザを指定できます。`-m`,`--mode`で指定できます。

### 操作画面
##### 設定画面
対象のurlやselector、speakerの設定を行います。
- url、読み上げる対象のurlです。
- text_selector、対象のurlからテキストを取得するselectorです。ブラウザの開発者ツール等で確認できます。setボタンを押すとurlに対するtext_selectorが設定され、プレビューが表示されます。
- next_url_selector、対象のurlから次に読み込むページのurlを取得するselectorです。ブラウザの開発者ツール等で確認できます。setボタンを押すとurlに対するnext_url_selectorが設定され、プレビューが表示されます。
- auto_next、チェックをつけた場合、ページから取得したテキストの読み上げが完了したときに自動で次のページの読み上げを開始します。
- volume、読み上げの音量を設定します。
- speaker、COEIROINKのspeakerを設定します。

##### 再生画面
再生中のテキスト、再生予定のテキストを表示します。画面下のボタンで音量と自動再生を設定や一時停止、次/前のテキストに移る、次のページに移動等ができます。



