#! python3
# removeCsvHeader.py - カレントディレクトリの全CSVファイルから見出しを削除する

import csv, os
import sys
sys.path.append('/Users/HOgishima/.pyenv/versions/3.7.1/lib/python3.7/site-packages')
import pandas as pd

os.chdir('./python/rl_clean/data') # ここでフォルダを選択
#os.makedirs('clean', exist_ok=True)

# CSVファイルのみを探して変数に格納
for (folder, subfolders, files) in os.walk('/Users/HOgishima/Box Sync/Code/python/rl_clean/data'):
    os.chdir('{}'.format(folder))
    for file in files:
        if not file.endswith('.csv'):
            continue # CSVファイルでなければスキップ

        print('データクリーニング中 ' + file + '...')

        # データの整理
        file_delete = pd.read_csv(file,
            usecols=['stim1_posx', 'stim1_posy',
            'stim2_posx','stim2_posy','correctAns', 'faulseAns',
            'key_resp_correct.keys','key_resp_faulse.keys'])
        file_delete = file_delete.dropna(how='all') # 全行空白削除
        file_delete = file_delete.drop([1,2]) # 最初の２行削除

        # 座標をベクトルに
        file_delete.loc[(file_delete['stim1_posx'] == 0) & (file_delete['stim1_posy'] == 200), 'stim1'] = 'up'
        file_delete.loc[(file_delete['stim1_posx'] == 400) & (file_delete['stim1_posy'] == 0), 'stim1'] = 'right'
        file_delete.loc[(file_delete['stim1_posx'] == -400) & (file_delete['stim1_posy'] == 0), 'stim1'] = 'left'
        file_delete.loc[(file_delete['stim1_posx'] == 0) & (file_delete['stim1_posy'] == -200), 'stim1'] = 'down'
        file_delete.loc[(file_delete['stim2_posx'] == 0) & (file_delete['stim2_posy'] == 200), 'stim2'] = 'up'
        file_delete.loc[(file_delete['stim2_posx'] == 400) & (file_delete['stim2_posy'] == 0), 'stim2'] = 'right'
        file_delete.loc[(file_delete['stim2_posx'] == -400) & (file_delete['stim2_posy'] == 0), 'stim2'] = 'left'
        file_delete.loc[(file_delete['stim2_posx'] == 0) & (file_delete['stim2_posy'] == -200), 'stim2'] = 'down'

        # subjIDとtrialの定義
        file_delete['subjID'] = '{}'.format(folder)
        file_delete['trial'] = list(file_delete.reset_index(drop=True).index+1)

        # choiceを定義
        file_delete.loc[(file_delete['stim1'] == file_delete['key_resp_correct.keys']) |
            (file_delete['stim1'] == file_delete['key_resp_faulse.keys']), 'choice'] = 1
        file_delete.loc[(file_delete['stim2'] == file_delete['key_resp_correct.keys']) |
            (file_delete['stim2'] == file_delete['key_resp_faulse.keys']), 'choice'] = 2

        # outcomeを定義
        file_delete.loc[file_delete['key_resp_correct.keys'] == 'up', 'outcome'] = 1
        file_delete.loc[file_delete['key_resp_correct.keys'] == 'right', 'outcome'] = 1
        file_delete.loc[file_delete['key_resp_correct.keys'] == 'left', 'outcome'] = 1
        file_delete.loc[file_delete['key_resp_correct.keys'] == 'down', 'outcome'] = 1
        file_delete.loc[file_delete['key_resp_correct.keys'] == 'None', 'outcome'] = -1

        # 書き出すファイルを作成
        file_delete.to_csv('/Users/HOgishima/Box Sync/Code/python/clean/ri_clean.csv',
        columns=['subjID', 'trial', 'choice', 'outcome'],header=False, index=False, mode='a')

        print(file_delete[['subjID', 'trial', 'choice', 'outcome']])
    print('整理が完了しました')
