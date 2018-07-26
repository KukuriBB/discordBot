導入手順
	discordの開発者モードをオンにする
		discordの設定->テーマ->開発者モード

	botの作成法
		https://qiita.com/PinappleHunter/items/af4ccdbb04727437477f)
		↑の、"Bot用のトークンを手に入れる"の通りに作業
	
	cygwinをインストール
		1.	https://www.cygwin.com/
			↑から、 setup-x86_64.exeをダウンロードして実行
		2.	ウィンドウのタイトルが
				Cygwin Setup - Select Packages
			になるまで「次へ」を押す
		3.	viewのプルダウンメニューをFullにする
			serchに python3 と入力
			Skipと表示されているところをクリックして、すべて数字に変更
				(ぶっちゃけ全部入れる必要はないけど、どれが必要なのかわからない)
		4	終わるまで「次へ」を押す
	
	プログラムの実行環境を整える
		1.	cygwinを起動して、
				python3 -m pip install -U discord.py
			と入力
		2.	cygwinを起動して、
				cygstart .
			と入力
		3.	エクスプローラーが開くので、teamDivider.pyをそこに入れる
		4.	teamDivider.pyをメモ帳か何かで開く
		5.	一番下の行に
				bot.run("NDcxNjU5MjgzNTU4MTcwNjI0.DjoTgQ.xZF_8mR26TPoCa1RFVwtkYH8Bvg")
			と書いてあるので、
				NDcxNjU5MjgzNTU4MTcwNjI0.DjoTgQ.xZF_8mR26TPoCa1RFVwtkYH8Bvg
			の部分を、自分のボットのトークンで置き換える
		
実行方法
	1.	cygwinを起動
	2.	python3 teamDivider.py
		と入力
	3.	画面に
			Logged in as
			teamDivider
		と表示され、discodeの鯖でteamDividerがオンラインになっていれば成功
	4.	メンバーの参加しているチャンネルのIDをコピーし、
		botの参加しているチャンネルで、
			roll コピーしたID
		を入力することで実行される
		