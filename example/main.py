#%%
import numpy as np
import matplotlib.pyplot as plt

from puzzleimage import SkeltonImage

%reload_ext autoreload
%autoreload 2

si = SkeltonImage(blank="")

# cell = np.array([
#     ["","サ","","ウ","ズ","ラ"],
#     ["カ","バ","ー","ニ","","イ"],
#     ["ジ","","","","","オ"],
#     ["キ","ツ","ネ","","","ン"],
#     ["","","コ","ア","ラ",""]
# ])
cell = np.full([15, 15], "a")
cell[:5, -10] = ""
cell[-5:, -3] = ""

uwords = np.array(["カジキ", "サバ", "キツネ", "カバーニ", "ウニ", "ウズラ", "ライオン", "コアラ"])
# %%
fig, [axl, axr] = plt.subplots(1, 2, figsize=(16, 7.5), gridspec_kw=dict(width_ratios=[9,7], wspace=-0.1))
axl = si.get_board(axl, cell, title="テストパズル", w_count=len(uwords), is_answer=True)
axr = si.get_wordlist(axr, uwords)
plt.show()
# %%
