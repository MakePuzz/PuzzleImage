import matplotlib.patches as mpatches
import numpy as np


class WordList:
    def __init__(self, words, char_max_per_row=21):
        self.words = np.array(sorted(words, key=lambda word: (len(word), word)))
        self.w_lens = np.vectorize(len)(words)
        self.char_max_per_row = char_max_per_row
        self.w_num = len(self.words)

    def draw_wordlist(self, ax):
        ax.axis("off")
        if self.w_num <= 40:
            col_num = 2
        if self.w_num > 40:
            col_num = 3
        self.row_num = np.ceil(self.w_num / col_num).astype(int)

        char_num_per_row = self._get_char_num_per_row(self.row_num, col_num)
        # penetrate check
        pene_words_count, peneall = self._check_penetrate(self.row_num, col_num, char_num_per_row)
        # overflow because of 2 columns and many penetration
        if col_num == 2 and (self.w_num / 2 + pene_words_count) > 18:
            col_num = 3
            self.row_num = np.ceil(self.w_num / col_num).astype(int)
            char_num_per_row = self._get_char_num_per_row(self.row_num, col_num)
            pene_words_count, peneall = self._check_penetrate(self.row_num, col_num, char_num_per_row)

        # # define row space
        # no penetration
        if pene_words_count == 0:
            # row spacing
            if self.row_num <= 10:
                row_spacing = 0.05 + 0.05
            if self.row_num <= 15:
                row_spacing = 0.015 + 0.05
            if self.row_num > 15:
                row_spacing = 0.05
            self.row_num_at_col_1 = self.row_num
            self.row_num_at_col_3 = self.w_num - 2 * self.row_num
        # penetration
        if pene_words_count > 0:
            if peneall:  # all penetration
                # row spacing
                self.row_num_plus_pene_num = self.row_num + pene_words_count
                if self.row_num_plus_pene_num <= 10:
                    row_spacing = 0.05 + 0.05
                if self.row_num_plus_pene_num <= 15:
                    row_spacing = 0.015 + 0.05
                if self.row_num_plus_pene_num > 15:
                    row_spacing = 0.05

                if pene_words_count > (20 - self.row_num):  # self.row_num adjust
                    self.row_num = 20 - pene_words_count
                self.row_num_at_col_1 = self.row_num
                self.row_num_at_col_3 = self.w_num - 2 * self.row_num - pene_words_count
            if not peneall:  # Penetration appears in the right two columns
                row_spacing = 0.05
                if pene_words_count > (20 - self.row_num):
                    self.row_num = 20 - pene_words_count  # self.row_num adjust
                self.row_num_at_col_1 = 20
                self.row_num_at_col_3 = self.w_num - 20 - self.row_num - pene_words_count
        # 1st column
        first_w = 0
        last_w = self.row_num_at_col_1
        col_spacing = 0.02
        ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=col_spacing)
        if col_num == 2:
            # 2nd column
            first_w = self.row_num_at_col_1
            last_w = self.w_num - pene_words_count
            col_spacing = 0.25 + (self.w_lens[self.row_num_at_col_1] - 3) * 0.05
            ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=col_spacing)
            # penetrating column
            if pene_words_count > 0 and peneall:
                first_w = self.w_num - pene_words_count
                last_w = self.w_num
                ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=0.02,
                                       y_offset=0.97 - row_spacing * (self.row_num) - 0.025)
        if col_num == 3:
            # 2nd column
            first_w = self.row_num_at_col_1
            last_w = self.row_num_at_col_1 + self.row_num
            col_spacing = 0.25 + (self.w_lens[self.row_num_at_col_1] - 3) * 0.05
            ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=col_spacing)
            # 3rd column
            first_w = self.row_num_at_col_1 + self.row_num
            last_w = self.row_num_at_col_1 + self.row_num + self.row_num_at_col_3
            col_spacing += (self.w_lens[self.row_num_at_col_1 + self.row_num]) * 0.05 + 0.08
            ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=col_spacing)
            # penetrating column
            if pene_words_count > 0:
                first_w = self.row_num_at_col_1 + self.row_num + self.row_num_at_col_3
                last_w = self.row_num_at_col_1 + self.row_num + self.row_num_at_col_3 + pene_words_count
                if peneall:
                    ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=0.02,
                                           y_offset=0.97 - row_spacing * (self.row_num) - 0.025, separate_space=True)
                if not peneall:
                    col_spacing = (self.w_lens[self.row_num_at_col_1] - 3) * 0.05
                    ax = self._draw_column(ax, self.words[first_w:last_w], row_spacing, label_x=0.25 + col_spacing,
                                           y_offset=0.97 - row_spacing * (self.row_num) - 0.025, separate_space=True)
        # copyright
        if col_num == 3:
            x_text = 0.95
        elif col_num == 2 and not peneall:
            x_text = 0.25 + (self.w_lens[self.row_num_at_col_1] - 3) * 0.05 + (self.w_lens[self.w_num - 1] + 1) * 0.05
        elif col_num == 2 and peneall:
            x_text = (self.w_lens[self.w_num - 1]) * 0.05
        ax.text(x_text, -0.01, '© MakePuzz', size=18, ha='right', fontname='Yu Gothic', alpha=0.5, fontweight='bold')

    def _get_char_num_per_row(self, row_num, col_num):
        if col_num == 2:
            char_num_per_row = self.w_lens[self.row_num - 1] + self.w_lens[self.w_num - 1] + 2
        if col_num == 3:
            char_num_per_row = self.w_lens[self.row_num - 1] + self.w_lens[2 * self.row_num - 1] + self.w_lens[
                self.w_num - 1] + 2 + 4
        return char_num_per_row

    def _check_penetrate(self, row_num, col_num, char_num_per_row):
        pene_words_count = 0
        peneall = False
        if char_num_per_row > self.char_max_per_row:
            if col_num == 2:
                peneall = True
                while char_num_per_row > self.char_max_per_row:
                    pene_words_count += 1
                    char_num_per_row = self.w_lens[self.row_num - 1] + self.w_lens[
                        self.w_num - 1 - pene_words_count] + 2
            if col_num == 3:
                char_num_at_row_2to3 = (self.char_max_per_row - 2 - self.w_lens[
                    self.row_num - 1])  # Subtract the left column from the whole
                peneall = bool(char_num_at_row_2to3 < self.w_lens[self.w_num - 1])
                while char_num_per_row > self.char_max_per_row:
                    pene_words_count += 1
                    char_num_per_row = self.w_lens[self.row_num - 1] + self.w_lens[2 * self.row_num - 1] + self.w_lens[
                        self.w_num - 1 - pene_words_count] + 2 + 4
        return pene_words_count, peneall

    def _draw_column(self, ax, words, row_spacing, label_x=0.02, y_offset=0.97, separate_space=False,
                     label_labelline_spacing=0.01, label_box_spacing=0.027, label_word_spacing=0.06,
                     label_color="dimgray", box_size=0.015, box_fc="#f5efe6", box_ec="darkgray", box_pad=0.005,
                     labelline_color="lightgray"):
        """draw word columns on the matplotlib.pyplot.axes"""
        if separate_space:
            ax.axhline(y=y_offset + 0.038, color=labelline_color, xmin=label_x - 0.02, xmax=0.99, lw=2, ls=':')
        nwords = len(words)
        w_lens = np.vectorize(len)(words)
        labelline_x = label_x + label_labelline_spacing
        box_x = label_x + label_box_spacing
        word_x = label_x + label_word_spacing
        ymax = y_offset + 0.01
        boxstyle = mpatches.BoxStyle("Round", pad=box_pad)
        for n, word in enumerate(words):
            # checkbox
            box_y = y_offset - row_spacing * n - box_pad
            fancybox = mpatches.FancyBboxPatch((box_x, box_y), box_size, box_size, boxstyle=boxstyle, fc=box_fc,
                                               ec=box_ec, alpha=1)
            ax.add_patch(fancybox)
            # word
            word_y = box_y + box_pad
            ax.text(word_x, word_y, word, size=18, ha='left', va='center')
            # label
            if n == 0 or w_lens[n] > w_lens[n - 1]:
                ax.text(label_x, word_y, str(w_lens[n]), fontsize=10, color=label_color, ha='right')
            # label line
            if w_lens[n] > w_lens[n - 1]:
                ax.axvline(x=labelline_x, color=labelline_color, ymin=y_offset - 0.01 - row_spacing * (n - 1),
                           ymax=ymax, lw=2)
                ymax = y_offset + 0.01 - row_spacing * n
        # label line to lower edge
        ax.axvline(x=labelline_x, color=labelline_color, ymin=y_offset - 0.01 - row_spacing * n, ymax=ymax, lw=2)
        return ax
