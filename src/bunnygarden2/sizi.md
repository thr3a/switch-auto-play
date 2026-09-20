bunnygarden2
最初は

home_first.jpg 「バニーガーデンへ入室します」の文字があるはず　なければそうするように指示して終了

右ボタンを3回おす
home_gyanburu.jpg ギャンブルに挑戦します とでるはず
Aボタン

しばらく時間かかるので待機

gyanburu_left.jpg 「安心して楽しく遊べるレートです」とでるはず

でたら右に2回 

gyanburu_right.jpg 「本気で勝負したいときのレートです」とでるはず

Aボタン

しばらく時間かかるので待機

gyanburu_win.jpg
gyanburu_win2.jpg
gyanburu_win3.jpg WINの文字は取得できなかった 「+○○円」が取得できればOK？

gyanburu_lose.jpg LOSEの文字は取れない 「-***円」が取得できればOK？ ex.-6,900円

WINもLOSEもBボタンで止める

【条件分岐】
【WIN】
かったらセーブして再挑戦
下2回でセーブロードへ移動する
home_saveload.jpg  「セーブとロードが行えます」

Aボタン4回 1秒間隔で
Bキャンセル 2回 home_saveload.jpgに行くはず

上2回でギャンブル選択へ　以下ループ

【LOSE】
セーブ戻して損失なかったことにする
下2回でセーブロードへ移動する
home_saveload.jpg  「セーブとロードが行えます」

A1回でhome_saveload_save.jpgにいく
下1押してロードへ　Aボタン3回

しばらく時間かかるので待機
home_first.jpg 「バニーガーデンへ入室します」の文字があるはずの最初に戻る　以下ループ
