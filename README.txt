導入手順
    cygwinをインストール
        1.インストーラの実行
            https://www.cygwin.com/
            ↑から、 setup-x86_64.exeをダウンロードして実行
        2.いじる必要のないところを無視
            ウィンドウのタイトルが
                Cygwin Setup - Choose Download Site(s)
            になるまで「次へ」を押す
        3.適当なサイトを選んで「次へ」を押す
        4.ウィンドウのタイトルが
              Cygwin Setup - Select Packages
          になるまで待つ
        5.python3のインストール設定
            viewのプルダウンメニューをCategoryにする
            searchに python3 と入力
            Pythonの右隣のDefaultをクリックして、Installにする
        6.gitのインストール設定
            searchに git と入力
            Develの右隣のDefaultをクリックして、Installにする
        7.いじる必要のないところを無視
            終わるまで「次へ」を押す
            ※時間がかかるので、待ち時間でbotの作成まで進めてしまうとよい
            
    discordの開発者モードをオンにする
        discordの設定->テーマ->開発者モード
    
    botの作成法
        https://qiita.com/PinappleHunter/items/af4ccdbb04727437477f)
        ↑の、"Bot用のトークンを手に入れる"の通りに作業
        Tokenは繰り返し使うので、どこかに保存しておくとよい
    
    プログラムの実行環境を整える
        1.cygwinを起動
        2.discord.pyのインストール
            python3 -m pip install -U discord.py
            と入力
        3.プログラムのダウンロード
            git clone https://github.com/KukuriBB/discordBot.git
            と入力
    
実行方法
    1.cygwinを起動
    2.ディレクトリを移動
        cd discordBot
        と入力
    3.プログラムの更新を確認
        git pull
        と入力
    4.ボットを起動
        python3 teamDivider.py <token>
        と入力
        ただし、<token>はボットの作成時に取得した、自分のトークンに置き換えること
        
        画面に
            Logged in as
              name: <bot name>
        と表示され、discordの鯖でボットがオンラインになっていれば成功
    5.チャンネルのIDをコピー
        参加者の待機しているボイスチャンネルを右クリックし、
        「IDをコピー」を選択
    6.ボットに命令
        botの参加している鯖のテキストチャンネルで、コマンドを入力する
        コマンド一覧は、botの参加している鯖のテキストチャンネルでhelpと入力することで表示される
    
