import streamlit as st
import pandas as pd
import re

conversion_list = [
    ("有り", "あり"), ("有る", "ある"), ("貴方", "あなた"), ("此方", "こちら"), ("其方", "そちら"),
    ("言う", "いう"), ("致す", "いたす"), ("頂く", "いただく"), ("頂き", "いただき"),
    ("ウィルス", "ウイルス"), ("ウエルカムデイ", "ウェルカムデイ"), ("伺う", "うかがう"),
    ("お話し", "お話"), ("及び", "および"), ("形", "かたち"), ("頑張る", "がんばる"),
    ("下さい", "ください"), ("下さる", "くださる"), ("事", "こと"), ("子供", "子ども"),
    ("頃", "ころ"), ("様々", "さまざま"), ("更に", "さらに"), ("全て", "すべて"),
    ("する様", "するよう"), ("但し", "ただし"), ("達", "たち"), ("為", "ため"),
    ("出来る", "できる"), ("通り", "とおり"), ("時", "とき"), ("所", "ところ"),
    ("兎に角", "とにかく"), ("友達", "友だち"), ("共に", "ともに"),
    ("取組む", "取り組む"), ("取組み", "取り組み"), ("無い", "ない"),
    ("尚", "なお"), ("等", "など"), ("並びに", "ならびに"),
    ("一人一人", "一人ひとり"), ("ひとりひとり", "一人ひとり"),
    ("方", "ほう"), ("欲しい", "ほしい"), ("先ず", "まず"), ("又", "また"),
    ("又は", "または"), ("全く", "まったく"), ("自ら", "みずから"),
    ("無駄", "むだ"), ("無理矢理", "むりやり"), ("若しくは", "もしくは"),
    ("持つ", "もつ"), ("最も", "もっとも"), ("の元", "のもと"), ("の下", "のもと"),
    ("者", "もの"), ("物", "もの"), ("良い", "よい"), ("良かった", "よかった"),
    ("宜しく", "よろしく"), ("分かる", "わかる"), ("zoom", "Zoom"),
    ("父兄", "保護者"), ("兄弟", "兄弟姉妹")
]

exceptions = {
    "事": "『自分事』『出来事』などは例外の可能性があります。",
    "時": "名詞としての『時』は漢字が適切な場合があります。",
    "方": "方角を表す場合は漢字、比較の場合はひらがなが望ましいです。"
}

st.title("表記ゆれチェックツール")
st.write("文章を下のボックスに貼り付けて、表記のゆれ・数字表記・注意語をチェックしましょう。")

text_input = st.text_area("文章を入力：", height=300)

if st.button("チェック"):
    if not text_input.strip():
        st.warning("文章が空です！")
    else:
        hits = []
        highlighted = text_input

        # 表記ゆれチェック
        for wrong, correct in conversion_list:
            if wrong in text_input:
                hits.append((wrong, correct))
                highlighted = re.sub(f"({re.escape(wrong)})", r"<mark>\1</mark>", highlighted)

        st.markdown("#### 🔍 ハイライト結果")
        st.markdown(highlighted, unsafe_allow_html=True)

        if hits:
            st.markdown("#### ✅ 該当表記一覧")
            df = pd.DataFrame(hits, columns=["間違い", "正しい表記"])
            st.dataframe(df, use_container_width=True)
        else:
            st.success("表記ゆれは見つかりませんでした！")


        if digit_issues:
    st.markdown("#### 🔢 数字表記ルール違反")
    for msg in digit_issues:
        st.warning(msg)


        # 数字ルールチェック
        digit_issues = []
        man_digit_issues = []

# 1桁は全角、2桁以上は半角チェック
for match in re.finditer(r'[0-9０-９]+', text_input):
    num = match.group()
    if len(num) == 1:
        if num.isascii():  # 半角1桁はNG
            digit_issues.append(f"{num} は1桁なので全角が望ましいです。")
    elif len(num) >= 2:
        if not num.isascii():  # 全角2桁以上はNG
            digit_issues.append(f"{num} は2桁以上なので半角が望ましいです。")


# ⬇ ここから追加！OK！
def zenkaku_to_hankaku(s):
    z2h = str.maketrans("０１２３４５６７８９", "0123456789")
    return s.translate(z2h)

text_input = zenkaku_to_hankaku(text_input)

wrong_big_numbers = []
for match in re.finditer(r'\d{5,}', text_input):
    num = match.group()
    wrong_big_numbers.append(f"「{num}」は万以上なので、漢数字をつけた表記（例：十六万8000円）が望ましいです。")

if wrong_big_numbers:
    st.markdown("### ⚠️ 万以上の数字表記ルール")
    for msg in wrong_big_numbers:
        st.warning(msg)


        # 1桁は全角、2桁以上は半角
        for match in re.finditer(r'\d+', text_input):
            num = match.group()
            if len(num) == 1:
                digit_issues.append(f"1桁の数字「{num}」は全角が望ましいです。")
            elif len(num) >= 2 and any(c in "０１２３４５６７８９" for c in num):
                digit_issues.append(f"2桁以上の数字「{num}」は半角が望ましいです。")

        # 万以上の数は漢数字が望ましい
        for match in re.finditer(r'(\d+)万([０-９\d]{1,4})', text_input):
            man = match.group()
            if re.match(r'\d+', match.group(1)):
                man_digit_issues.append(f"「{man}」の『{match.group(1)}万』は漢数字での表記（例：十六万）が望ましいです。")

        if digit_issues or man_digit_issues:
            st.markdown("### ⚠️ 数字ルールの指摘")
            for msg in digit_issues + man_digit_issues:
                st.warning(msg)

        # 例外語チェック
        st.markdown("### ⚠️ 注意が必要な語")
        for word, note in exceptions.items():
            if word in text_input:
                st.warning(f"『{word}』が含まれています：{note}")
