window.STATS_DATA = {
  "generated_at": "2026-08-23T02:51:59Z",
  "rules": {
    "count": 1,
    "chars": 540
  },
  "candidates": {
    "count": 5,
    "chars": 5336
  },
  "incidents": {
    "count": 1,
    "chars": 499
  },
  "total_chars": 6375,
  "history": [
    {
      "date": "2026-08-23T00:58:47Z",
      "summary": "記録を開始しました(既存 7件)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 5415
    },
    {
      "date": "2026-08-23T01:02:27Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 5415
    },
    {
      "date": "2026-08-23T01:06:05Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 5448
    },
    {
      "date": "2026-08-23T01:19:48Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 5474
    },
    {
      "date": "2026-08-23T01:27:42Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6246
    },
    {
      "date": "2026-08-23T01:46:45Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T01:55:34Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T01:55:48Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T01:56:36Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T01:58:28Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T02:12:59Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T02:25:28Z",
      "summary": "記録を開始しました(既存 7件)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T02:28:31Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T02:29:47Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    },
    {
      "date": "2026-08-23T02:51:59Z",
      "summary": "新しい記録なし(数値のみ再集計)",
      "rules_count": 1,
      "candidates_count": 5,
      "incidents_count": 1,
      "total_chars": 6375
    }
  ],
  "items": {
    "rules": [
      {
        "filename": "godot-optimization.md",
        "title": "Godot 4 最適化ルール",
        "content": "# Godot 4 最適化ルール\n\nstatus: confirmed\npromoted_from: candidates/2026-06-multimesh-discovery.md\nconfirmed_in: [RESODIVE, DEPTH//]\nconfirmed_count: 2\ntags: [godot, ゲーム開発, パフォーマンス最適化]\nskill: godot-optimization\n\n## ルール\n敵や弾丸など同一メッシュの大量インスタンスは、個別の Node ではなく\nMultiMeshInstance3D を使う。個別 Node は 200 体を超えたあたりから\n_process のオーバーヘッドで明確にフレームが落ちる。\n\n## 判断基準\n- 「同じ見た目のオブジェクトが同時に50体以上存在しうるか」で判定する\n- 存在しうるなら最初から MultiMeshInstance3D 設計にする\n  (後から個別Node実装を移行するコストの方が高い)\n\n## 根拠になった事例\n- incidents/2026-05-resodive-enemy-lag.md\n- incidents/2026-06-depth-bullet-lag.md\n",
        "tags": [
          "godot",
          "ゲーム開発",
          "パフォーマンス最適化"
        ],
        "projects": [],
        "days_old": null,
        "stale": false,
        "problem_summary": null,
        "solution_summary": "敵や弾丸など同一メッシュの大量インスタンスは、個別の Node ではなく MultiMeshInstance3D を使う。個別 Node は 200 体を超えたあたりから _pro…",
        "skill_name": "godot-optimization",
        "skill_installed": true
      }
    ],
    "candidates": [
      {
        "filename": "2026-08-example-candidate.md",
        "title": "AudioStreamPlayerのバス切り替えタイミング",
        "content": "# [候補] AudioStreamPlayerのバス切り替えタイミング\n\nstatus: candidate\nobserved_count: 1\nobserved_in: [DEPTH//]\ntags: [godot, オーディオ, ゲーム開発]\ndate: 2026-08-20\n\n## 何が起きたか\nシーン切り替えの直前に音声のバス(出力先)を切り替えると、音が一瞬途切れることがある。\n\n## わかったこと・今の対応\nシーン切り替えが終わってから切り替えれば発生しない。今のところこの回避策のみで、根本原因(別の現象「OGG/PhaseLoopMusicの音切れ」と同じ原因かどうか)は未確認。\n\n## まだ確認できていないこと\n- Polypulseの時にあった「OGG/PhaseLoopMusicの音切れ」と同一原因か未確認\n- 他のプロジェクトでも再現するか未確認\n\n## 昇格の条件\n別のプロジェクトでも同じ現象が確認されたら rules/ に昇格し、\nincidents/ に詳細ログを残す。\n",
        "tags": [
          "godot",
          "オーディオ",
          "ゲーム開発"
        ],
        "projects": [
          "DEPTH//"
        ],
        "days_old": 3,
        "stale": false,
        "problem_summary": "シーン切り替えの直前に音声のバス(出力先)を切り替えると、音が一瞬途切れることがある。",
        "solution_summary": "シーン切り替えが終わってから切り替えれば発生しない。今のところこの回避策のみで、根本原因(別の現象「OGG/PhaseLoopMusicの音切れ」と同じ原因かどうか)は未確認。"
      },
      {
        "filename": "2026-08-23-windows-python3-stub-broken.md",
        "title": "Windows Git Bashでの`python3`コマンドはMicrosoft Storeスタブに化ける",
        "content": "# [候補] Windows Git Bashでの`python3`コマンドはMicrosoft Storeスタブに化ける\n\nstatus: candidate\nobserved_count: 1\nobserved_in: [ai-dev-knowledge-system]\ntags: [windows, python, 環境構築]\ndate: 2026-08-23\n\n## 何が起きたか\nWindows(Git Bash)で`python3`と入力すると、本物のPythonではなく壊れたMicrosoft Storeの案内役が呼ばれてしまい、エラーで止まる。\n\n## わかったこと・今の対応\n本物のPythonは別の場所(`Python312`フォルダ)にあるので、そこにPATHを通すか、`python3`という名前のコピーを作ることで回避できる。\n\n## 詳しい経緯\nこのマシン(Windows + Git Bash環境)で `python3` を実行すると、\n実際のPythonではなく `C:\\Users\\owner\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe`\n(Microsoft Store の AppInstallerPythonRedirector.exe へのシンボリックリンク)が\n呼ばれてしまい、正常に動作しない(`print()`すら実行できず、意味不明な\n出力とexit code 49で終了する)。\n\n一方 `python`(3ではなく)コマンドも同じWindowsAppsのstubを指しているが、\n`py`ランチャーは正常に動作する。実体のPythonは\n`C:\\Users\\owner\\AppData\\Local\\Programs\\Python\\Python312\\python.exe` にあり、\nこれを直接PATHに通す(またはシムスクリプトを作る)ことで回避できる。\n\nシェルスクリプト(bashやhookコマンド)内で `python3` をハードコードしていると、\nこのマシン・この手のWindows環境では静かに失敗する、または不可解な出力になる\n点に注意。\n\n## まだ確認できていないこと\n- 他のWindowsマシン/ユーザー環境でも同じスタブ配置になっているか未確認\n  (Microsoft Store版Pythonのインストール有無に依存する可能性)\n- `python3` を直接使わず `py -3` や絶対パス指定に統一するのが\n  一般的な回避策として十分か未検証\n\n## 昇格の条件\n別のプロジェクト、または別セッションでも同じ現象(`python3`がスタブに\n化けて動かない)が確認されたら rules/ に昇格する。\n",
        "tags": [
          "windows",
          "python",
          "環境構築"
        ],
        "projects": [
          "ai-dev-knowledge-system"
        ],
        "days_old": 0,
        "stale": false,
        "problem_summary": "Windows(Git Bash)で`python3`と入力すると、本物のPythonではなく壊れたMicrosoft Storeの案内役が呼ばれてしまい、エラーで止まる。",
        "solution_summary": "本物のPythonは別の場所(`Python312`フォルダ)にあるので、そこにPATHを通すか、`python3`という名前のコピーを作ることで回避できる。"
      },
      {
        "filename": "2026-08-23-small-crop-color-sampling-alignment-sensitivity.md",
        "title": "小さいクロップ窓での代表色抽出は数px のズレで背景色に汚染される",
        "content": "# [候補] 小さいクロップ窓での代表色抽出は数px のズレで背景色に汚染される\n\nstatus: candidate\nobserved_count: 1\nobserved_in: [pokemon-champions-BattleAI]\ntags: [画像処理, 座標校正]\ndate: 2026-08-23\n\n## 何が起きたか\n小さいアイコン(40×30px程度)から色を抽出するとき、切り取る位置が数pxずれているだけで、背景色に汚染されて誤判定が起きた。\n\n## わかったこと・今の対応\n切り取る範囲を実測して正確な位置に直したら解消した。対象が小さいほど、数pxのズレが致命的になりやすい。\n\n## 詳しい経緯\nゲーム画面のUIバッジ(性別アイコン等、40x30px程度の小さい円)から\n「中間輝度の画素だけを残して中央値を取る」方式で代表色を抽出する処理を、\n別レイアウトの画面向けに新しい座標で再校正していたところ、目分量で\n決めた座標(本来のアイコン位置から左に約12px、上下にも数px分の余分な\nマージンを含む窓)では、既知で女性のはずのアイコンが軒並み「男性」と\n誤判定される現象が起きた。\n\n原因を調べたところ、窓が実際のアイコン位置からズレていたことで、\n背景色(カードの紫グラデーション)の割合がアイコン自体の画素数を\n上回り、中央値の計算結果が背景色にほぼ支配されていた(背景の紫が\nたまたま「男性=青系」の参照色に近い色味だったため、誤判定として\n現れた)。窓を実測(10px刻みの目盛りを焼き込んだ拡大画像で目視確認)\nした正確な範囲に絞り込んだところ解消した。\n\n大きい領域(100px角以上等)であれば数px のズレは全体に対する割合が\n小さく吸収されるが、40x30px程度の小さいバッジ/アイコンを対象にした\n色抽出・テンプレートマッチングでは、同じ数px のズレが致命的な誤判定を\n生む。小さい対象への座標校正は「だいたい合っている」では不十分で、\n実測ベースでピクセル単位まで詰める必要がある。\n\n## まだ確認できていないこと\n- 「小さい対象では座標ズレの影響が非線形に大きくなる」という一般化が、\n  色抽出以外の手法(テンプレートマッチング等)にも同程度に当てはまるか\n  は定量的には未検証(テンプレートマッチングは窓が多少広くても内部で\n  スケール探索するため、色抽出ほど脆弱ではない可能性がある)\n- 対象サイズと許容ズレ量の関係(例: 対象の何%以内のズレなら安全か)を\n  定量化した基準は未確立\n\n## 昇格の条件\n別のプロジェクトでも「小さいUI要素の色/特徴抽出が数pxの座標ズレで\n破綻する」ケースが確認されたら rules/ に昇格する。\n",
        "tags": [
          "画像処理",
          "座標校正"
        ],
        "projects": [
          "pokemon-champions-BattleAI"
        ],
        "days_old": 0,
        "stale": false,
        "problem_summary": "小さいアイコン(40×30px程度)から色を抽出するとき、切り取る位置が数pxずれているだけで、背景色に汚染されて誤判定が起きた。",
        "solution_summary": "切り取る範囲を実測して正確な位置に直したら解消した。対象が小さいほど、数pxのズレが致命的になりやすい。"
      },
      {
        "filename": "2026-08-23-easyocr-small-kana-confusion-not-fixable-by-preprocessing.md",
        "title": "EasyOCRの小さい仮名(ゃ/や等)混同は前処理では直らない",
        "content": "# [候補] EasyOCRの小さい仮名(ゃ/や等)混同は前処理では直らない\n\nstatus: candidate\nobserved_count: 1\nobserved_in: [pokemon-champions-BattleAI]\ntags: [OCR, 画像処理]\ndate: 2026-08-23\n\n## 何が起きたか\nEasyOCRで、小さい「ゃ」「や」のような拗音の仮名を、大きい仮名と読み間違える。\n\n## わかったこと・今の対応\n画質を上げても二値化(白黒に変換する処理)を変えても直らなかった。前処理では直せない、モデル自体の限界の可能性が高い。他のOCRエンジンを試すか、辞書で後から補正する方法はまだ試せていない。\n\n## 詳しい経緯\nEasyOCR(`[\"ja\",\"en\"]`)でゲーム画面のニックネームテキスト(通常フォント、\n装飾なし)を読ませたところ、「かあちゃん」が「かあちやん」に、\n「マスカーニャ」が「マスカーニヤ」になるなど、拗音を表す小さい仮名\n(ゃ/や、ャ/ヤ)を大きい仮名と混同する誤読が発生した。\n\n二値化+複数閾値探索(`ocr_best_of_thresholds`)、アップスケール2〜5倍を\n一通り試したが、いずれも改善しなかった(誤読結果は同じ「や/ヤ」の\nまま、信頼度だけが0.99台まで上がった=モデルは高い自信を持って\n間違えている)。このことから、この種の誤読は画質・二値化・解像度の\n問題ではなく、EasyOCRの認識モデル自体が小さい仮名と大きい仮名の\nサイズ差(字形はほぼ同じで大きさだけが違う)を安定して区別できない\nという、モデルレベルの限界である可能性が高いと判断した。\n\n前処理をいくら工夫しても直らないタイプの誤読がある、という切り分けの\n基準として: 複数の閾値・複数の拡大率を試しても常に「同じ」誤読結果に\n高信頼度で収束する場合、それは画質側の問題ではなくモデルの限界を\n疑うべき。\n\n## まだ確認できていないこと\n- PaddleOCR/Tesseract等、別のOCRエンジンであれば小さい仮名を正しく\n  区別できるかは未検証(このプロジェクトではEasyOCR以外を実機比較して\n  いない)\n- 小さい仮名が含まれる単語をあらかじめ辞書(既知のニックネーム/技名\n  リスト等)と照合して補正する、という後処理的な回避策の有効性は\n  未検証\n\n## 昇格の条件\n別のプロジェクトでもEasyOCRの小さい仮名混同が確認され、かつ前処理では\n直らないことが再確認されたら rules/ に昇格する。\n",
        "tags": [
          "OCR",
          "画像処理"
        ],
        "projects": [
          "pokemon-champions-BattleAI"
        ],
        "days_old": 0,
        "stale": false,
        "problem_summary": "EasyOCRで、小さい「ゃ」「や」のような拗音の仮名を、大きい仮名と読み間違える。",
        "solution_summary": "画質を上げても二値化(白黒に変換する処理)を変えても直らなかった。前処理では直せない、モデル自体の限界の可能性が高い。他のOCRエンジンを試すか、辞書で後から補正する方法はまだ試せ…"
      },
      {
        "filename": "2026-08-23-cv2-tm-ccorr-normed-bright-template-bias.md",
        "title": "cv2.TM_CCORR_NORMEDは明るい/淡色テンプレートが無関係な領域にも高スコアを出しやすい",
        "content": "# [候補] cv2.TM_CCORR_NORMEDは明るい/淡色テンプレートが無関係な領域にも高スコアを出しやすい\n\nstatus: candidate\nobserved_count: 1\nobserved_in: [pokemon-champions-BattleAI]\ntags: [OpenCV, 画像処理, テンプレートマッチング]\ndate: 2026-08-23\n\n## 何が起きたか\nOpenCVの`TM_CCORR_NORMED`という比較方法を使うと、明るい画像は内容と無関係な場所にも高い一致スコアを出してしまう。\n\n## わかったこと・今の対応\n別の比較方法(`TM_CCOEFF_NORMED`)に切り替えると、既存の検証済みケースの精度が落ちてしまったため、今回は不採用。切り替えを検討する際は、既知の正解データで必ず事前確認が必要。\n\n## 詳しい経緯\nOpenCVの`cv2.matchTemplate`で`cv2.TM_CCORR_NORMED`(平均値を減算しない\n正規化相関)を使ってポケモンのアイコン(128x128、アルファマスク付き)を\n複数種族の中から一致度で当てるテンプレートマッチングを行っていたところ、\n明度の高い/淡い配色のテンプレート(白いネズミの集団のアイコン、暗色だが\nコントラストが高いアイコン等)が、内容と無関係な複数の背景領域に対しても\n不自然に高い(かつ複数の異なる入力でほぼ同一値になる)スコアを返す現象が\n見つかった。実測では、全く異なる3つの入力領域に対して同じテンプレートが\n判で押したように同一スコア(0.946)を返していた。\n\n原因として、`TM_CCORR_NORMED`は平均値を減算しない正規化相関のため、\nテンプレート自体が明るい(または高コントラストな)場合、内容の一致度に\n関わらず明るい/コントラストの強い背景と広く相関してしまう性質がある\nと推測される。\n\n対策として`cv2.TM_CCOEFF_NORMED`(平均値減算あり)への切り替えを試したが、\n既存の検証済み6種の的中精度(6/6が1位)のうち3種(ヤドラン・ガブリアス・\nオーロンゲ)が1位から陥落する明確な精度低下が確認できたため不採用とした。\nつまり「CCOEFFの方が理論的に望ましい」という一般論だけで安易に切り替える\nと、既存の検証済みケースを壊すリスクがある。切り替えを検討する際は必ず\n既知の正解セットに対する回帰テストを実測すること。\n\n## まだ確認できていないこと\n- 他のテンプレートマッチング用途(ポケモン以外のアイコン認識、UI要素検出等)\n  でも同様の「明るいテンプレートの広範囲高スコア」現象が再現するか未確認\n- マスク付きTM_CCOEFF_NORMEDではなく、テンプレート側だけ事前に平均値を\n  引く、あるいはTM_CCORR_NORMEDのままテンプレートの明度分散でスコアを\n  正規化する等、精度を落とさずにこの偏りだけを抑える方法は未検証\n- 全テンプレート(このプロジェクトでは1000種近い)を総当たりでこの現象の\n  有無をスクリーニングする調査はまだ行っていない(2種のみ発見済み)\n\n## 昇格の条件\n別のプロジェクト(ポケモン以外のアイコン/スプライト認識用途)でも\nTM_CCORR_NORMEDの明るいテンプレート偏りが確認されたら rules/ に昇格する。\n",
        "tags": [
          "OpenCV",
          "画像処理",
          "テンプレートマッチング"
        ],
        "projects": [
          "pokemon-champions-BattleAI"
        ],
        "days_old": 0,
        "stale": false,
        "problem_summary": "OpenCVの`TM_CCORR_NORMED`という比較方法を使うと、明るい画像は内容と無関係な場所にも高い一致スコアを出してしまう。",
        "solution_summary": "別の比較方法(`TM_CCOEFF_NORMED`)に切り替えると、既存の検証済みケースの精度が落ちてしまったため、今回は不採用。切り替えを検討する際は、既知の正解データで必ず事前…"
      }
    ],
    "incidents": [
      {
        "filename": "2026-06-depth-bullet-lag.md",
        "title": "DEPTH// 弾丸大量発生時のフレーム低下",
        "content": "# [事例] DEPTH// 弾丸大量発生時のフレーム低下\n\ndate: 2026-06-15\nproject: DEPTH//\nrelated_rule: rules/godot-optimization.md\n\n## 何が起きたか\n雑魚敵を30体以上同時に倒すと、弾丸ノードが同時に150個近く発生し、\nフレームレートが60→22まで落ちた。\n\n## 原因\n弾丸を個別の RigidBody3D ノードとして生成していたため、\n_physics_process のオーバーヘッドが線形に増加していた。\n\n## 解決\nMultiMeshInstance3D + 独自の当たり判定計算に置き換え、\n150個発生時でも58fps以上を維持できるようになった。\n\n## 汎用化できそうな知見\n「同一見た目のインスタンスが50体を超えうる設計」は\n最初からMultiMeshInstance3Dを前提にすべき、という判断基準が立った。\n→ RESODIVEの敵AI実装(同様の課題)でも同じ判断が有効だった。\n→ 2案件で確認されたため rules/godot-optimization.md に昇格。\n",
        "tags": [],
        "projects": [],
        "days_old": 69,
        "stale": false,
        "problem_summary": "雑魚敵を30体以上同時に倒すと、弾丸ノードが同時に150個近く発生し、 フレームレートが60→22まで落ちた。",
        "solution_summary": "MultiMeshInstance3D + 独自の当たり判定計算に置き換え、 150個発生時でも58fps以上を維持できるようになった。"
      }
    ]
  },
  "promotion_suggestions": null,
  "skills": [
    {
      "folder_name": "godot-optimization",
      "name": "godot-optimization",
      "description": "Godot 4でのゲーム開発中、敵・弾丸・アイテムなど見た目が同じオブジェクトを大量に生成する設計や実装を相談されたら必ず使うこと。個別のNode(CharacterBody3D等)で大量インスタンスを扱おうとしている相談、パフォーマンス低下(フレームレート低下・カクつき)の相談、大量スポーン・弾幕システムの実装、MultiMeshInstance3Dに関する質問では特に必ず参照する。「敵が大量に出る」「弾がたくさん飛ぶ」「同じメッシュを何百個も並べる」といった話が出たら発動すること。",
      "linked_to_rule": true,
      "usage_count": 1
    }
  ],
  "stale_count": 0
};
