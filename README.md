# meeting-booking-fastapi-streamlit-ecs

 会議室を予約するアプリケーション。
 
## URL
https://meeting-booking.net/
 
 
## 利用方法
サイドバーから、行いたい機能 （Create or Read(index) or Read(show) or Update or Delete）と、ターゲット（ユーザー or 会議室 or 予約）を選択する。
 
## 機能
 
- Create: 作成
- Read(index): 一覧を取得
- Read(show): 指定されたidのデータを取得
- Upadate: 指定されたidのデータを編集
- Delete: 指定されたidのデータを削除

## 使用技術
 
- Python 3.8.5
- FastAPI 0.78.0
- Streamlit 1.9.0
- SQLite
- Docker
- AWS
    - CDK（Infrastructure as Code）
    - ECS
    - ECR
    - EFS
    - ALB（ロードバランサー）
    - Route53

## インフラ構成図

<p align="center">
 <img src="https://user-images.githubusercontent.com/92006553/173228636-e42b096c-f1cc-41ce-a1b3-beecf9ea3f19.jpg" />
</p>

## 作者
 
Ibuki Narukawa  
mail to: ibuki0212job@gmail.com
