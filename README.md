# meeting-booking-fastapi-streamlit-ecs
# Ride Share
 
一般人のドライバーと車にのせてほしい人をマッチングするアプリケーションです。
 
## URL
https://ride-share-2021.herokuapp.com/
 
***テスト用アカウント***
- ドライバー用
    - メールアドレス：test@gmail.com  
    - パスワード：laraveltest
- 相乗り者用
    - メールアドレス：test02@gmail.com  
    - パスワード：phptest2
 
## 利用方法
ドライバー側：  
ログインをして、「ドライバー登録」にて、送迎開始時刻や現在地、車の情報を登録します。「乗せて」一覧から、リクエストを承認すると、「これからのドライブ一覧」にて詳細確認とメッセージができます。　

相乗り者側：  
ログインをして、「ドライバー検索」から、出発時刻、出発地と目的地を入力すると、出発地から20km以内のドライバーの一覧が表示され、詳細ページへ遷移し、申請ができます。申請情報は、「リクエスト送信履歴」から確認できます。

## 目指した課題解決

地方の交通の便の改善。地方の人口に対する自動車所有率の高さから、席が絶対に余っていることに目をつけ、ライドシェアサービスによって有効活用できると考えました。
 
## 機能
 
- ドライバー検索
- マイページ（編集、詳細）
- リクエスト送信履歴一覧
- 「乗せて」一覧
- これからのドライブ一覧
- 過去のドライブ一覧
- メッセージ（作成、削除）
- ドライバー登録（作成、編集、詳細、削除）
- ドライバー登録履歴
- Google Maps API

## 使用技術
 
- PHP 7.3.31
- Laravel Framework 6.20.43
- MariaDB  Ver 15.1 Distrib 10.2.38-MariaDB
- AWS
    - Cloud9
    - S3
- Google Maps API
    - Maps JavaScript API
    - Places API
    - Directions API
    - Distance Matrix API
    - Geocoding API

## 注力した機能：ドライバー検索機能

- 機能詳細 
    - Distance Matrix APIを用いて、DB上に登録していて、近くにいるドライバーの場所を表示。
    - 結果テーブルの行をクリックするとルート表示（Directions APIを使用）。
- 作成背景  
タクシーアプリのように、自分の近くにいるドライバーをマップ上に可視化した方が、距離感を実感しやすいと考えたため。
- 工夫点
    - ドライバー登録をする段階で現在地の緯度と経度を取得しておくことで、計算過程を省略しました。
    - 結果テーブルは、Distance Matrix APIの結果を所要時間が少ない順で並び替え、jsから表示させています。それにともない、jsから「詳細ボタン」のクリックを発火にして、詳細ページへ検索結果をPOST送信しています。
    - Distance Matrix APIは一度に25個の目的地しか計算できないので、callbackしてそれ以上のドライバー数にも対応しています。

![image](https://user-images.githubusercontent.com/92006553/148695162-5378309a-281c-412e-a8cb-8cfa5f51acd9.png)







## 作者
 
Ibuki Narukawa  
mail to: ibuki0212job@gmail.com
