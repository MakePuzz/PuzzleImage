#%%
import numpy as np
import matplotlib.pyplot as plt

from puzzleimage import SkeltonImage


si = SkeltonImage()

cell = np.array([
    [" ","サ"," ","ウ","ズ","ラ"],
    ["カ","バ","ー","ニ"," ","イ"],
    ["ジ"," "," "," "," ","オ"],
    ["キ","ツ","ネ"," "," ","ン"],
    [" "," ","コ","ア","ラ"," "]
])
uwords = np.array(["カジキ", "サバ", "キツネ", "カバーニ", "ウニ", "ウズラ", "ライオン", "コアラ"])
# %%
fig, [axl, axr] = plt.subplots(1,2)
axl = si.get_board(axl, cell)
axr = si.get_wordlist(axr, uwords)

# %%
