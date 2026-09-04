# -*- coding: utf-8 -*-
"""绘制精确的 LCS 动态规划示意图（数字全部来自真实算法计算）"""
from PIL import Image, ImageDraw, ImageFont

X = 'ABCBDAB'
Y = 'BDCABA'
m, n = len(X), len(Y)

# 真实 DP 计算
c = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        c[i][j] = c[i - 1][j - 1] + 1 if X[i - 1] == Y[j - 1] else max(c[i - 1][j], c[i][j - 1])

# 真实回溯路径
match, path = set(), set()
i, j = m, n
while i > 0 and j > 0:
    path.add((i, j))
    if X[i - 1] == Y[j - 1]:
        match.add((i, j)); i -= 1; j -= 1
    elif c[i - 1][j] >= c[i][j - 1]:
        i -= 1
    else:
        j -= 1
# 还原 LCS 文本（按匹配格顺序）
lcs = ''.join(X[i - 1] for i, j in sorted(match))

W, H = 1920, 1080
img = Image.new('RGB', (W, H), '#ffffff')
d = ImageDraw.Draw(img)

CW, CH = 130, 96
x0 = (W - (n + 1) * CW) // 2
y0 = 100

def F(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

f_title = F(r'C:\Windows\Fonts\msyh.ttc', 34)   # 微软雅黑（中文标题）
f_bold  = F(r'C:\Windows\Fonts\arialbd.ttf', 34)
f_num   = F(r'C:\Windows\Fonts\arial.ttf', 32)
f_lab   = F(r'C:\Windows\Fonts\arialbd.ttf', 42)
f_lcs   = F(r'C:\Windows\Fonts\arialbd.ttf', 84)

# 顶部说明
d.text((W // 2, 36), '求序列 X = ABCBDAB 与 Y = BDCABA 的最长公共子序列',
       font=f_title, fill='#6e6e73', anchor='ma')

# 绘制单元格
for row in range(m + 1):          # row 对应 X 前缀长度 i
    for col in range(n + 1):      # col 对应 Y 前缀长度 j
        x, y = x0 + col * CW, y0 + row * CH
        if row == 0 or col == 0:  # 标签行列
            d.rectangle([x, y, x + CW, y + CH], fill='#f5f5f7', outline='#e5e5ea', width=2)
            if row == 0 and col > 0:
                d.text((x + CW // 2, y + CH // 2), Y[col - 1], font=f_lab, fill='#1d1d1f', anchor='mm')
            elif col == 0 and row > 0:
                d.text((x + CW // 2, y + CH // 2), X[row - 1], font=f_lab, fill='#1d1d1f', anchor='mm')
        else:
            ism = (row, col) in match
            isp = (row, col) in path
            if ism:
                d.rectangle([x, y, x + CW, y + CH], fill='#007aff', outline='#007aff', width=2)
            elif isp:
                d.rectangle([x, y, x + CW, y + CH], fill='#e8f1ff', outline='#e5e5ea', width=2)
            else:
                d.rectangle([x, y, x + CW, y + CH], fill='#ffffff', outline='#e5e5ea', width=2)
            fill = '#ffffff' if ism else '#1d1d1f'
            d.text((x + CW // 2, y + CH // 2), str(c[row][col]),
                   font=f_bold if ism else f_num, fill=fill, anchor='mm')

# 底部结果
d.text((W // 2, y0 + (m + 1) * CH + 78), 'LCS = ' + lcs,
       font=f_lcs, fill='#007aff', anchor='mm')

out = r'E:\Portfolio\portfolio-site\assets\lcs-diagram.png'
img.save(out)
print('saved:', out, '| LCS =', lcs, '| matches:', sorted(match))
