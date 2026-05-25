import time
import html
import urllib.parse
import streamlit as st
from st_copy_button import st_copy_button

st.set_page_config(
    page_title="JAMJAM Where",
    page_icon="📍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Design
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #fff7ed 0%, #ffffff 48%, #f8fafc 100%);
    }

    .block-container {
        max-width: 560px;
        padding-top: 1.3rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        padding: 1.4rem 1.15rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #ff8a3d 0%, #ff4f7b 100%);
        color: white;
        box-shadow: 0 12px 30px rgba(255, 79, 123, 0.22);
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 850;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.96;
    }

    .mini-copy {
        padding: 0.8rem 0.9rem;
        border-radius: 16px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412;
        font-size: 0.92rem;
        line-height: 1.65;
        margin-bottom: 1.2rem;
    }

    .result-card {
        padding: 1.25rem 1.1rem;
        border-radius: 24px;
        background: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
        margin-top: 1.2rem;
    }

    .result-label {
        font-size: 0.85rem;
        font-weight: 750;
        color: #f97316;
        margin-bottom: 0.35rem;
    }

    .result-title {
        font-size: 1.65rem;
        font-weight: 850;
        line-height: 1.25;
        color: #111827;
        margin-bottom: 0.8rem;
    }

    .reason-box {
        padding: 1rem;
        border-radius: 18px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        color: #374151;
        line-height: 1.75;
        margin-top: 0.8rem;
    }

    .point-list {
        margin-top: 0.8rem;
        padding-left: 1.2rem;
        line-height: 1.85;
    }

    .best-for {
        margin-top: 1rem;
        padding: 0.8rem;
        border-radius: 14px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412;
        line-height: 1.65;
    }

    .small-note {
        color: #6b7280;
        font-size: 0.82rem;
        line-height: 1.6;
        margin-top: 0.7rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 999px;
        height: 3.2rem;
        font-size: 1.05rem;
        font-weight: 850;
        background: linear-gradient(135deg, #ff8a3d 0%, #ff4f7b 100%);
        color: white;
        border: none;
        box-shadow: 0 10px 22px rgba(255, 79, 123, 0.25);
    }

    div.stButton > button:hover {
        color: white;
        box-shadow: 0 14px 28px rgba(255, 79, 123, 0.28);
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.65;
    }

    @media (max-width: 640px) {
        .hero-title {
            font-size: 1.75rem;
        }

        .result-title {
            font-size: 1.42rem;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Spot data
# category と tags を分けて、項目と店がズレないようにする
# -----------------------------
SPOTS = [
    {
        "name": "ラウンドワン 千種店",
        "area": "千種",
        "category": "スポーツ・運動",
        "min_budget": 1500,
        "max_budget": 4500,
        "min_hours": 2.0,
        "max_hours": 6.0,
        "tags": ["ワイワイ系", "体を動かしたい", "運動系", "雨でも安心", "長居したい", "グループ向き"],
        "url": "https://www.round1.co.jp/shop/tenpo/aichi-tikusa.html",
        "points": [
            "ボウリング・ビリヤード・ダーツ・卓球など、体を動かせる遊びが多い",
            "屋内施設なので、雨の日でも予定を立てやすい",
            "会話だけでなく一緒に遊ぶ体験があるため、グループで盛り上がりやすい"
        ],
        "best_for": "体を動かしながら、みんなでワイワイ遊びたいグループ"
    },
    {
        "name": "名古屋グランドボウル",
        "area": "南大高",
        "category": "スポーツ・運動",
        "min_budget": 1500,
        "max_budget": 4000,
        "min_hours": 1.5,
        "max_hours": 4.0,
        "tags": ["ワイワイ系", "体を動かしたい", "運動系", "雨でも安心", "グループ向き"],
        "url": "https://www.grandbowl.jp/nagoya/",
        "points": [
            "ボウリングを中心に、グループ全員で同じ体験を共有しやすい",
            "勝負やチーム分けができるため、自然に盛り上がりやすい",
            "ご飯だけでは物足りない時に、遊びとしての満足感を作りやすい"
        ],
        "best_for": "飲食だけでなく、体を動かす遊びを入れたいグループ"
    },
    {
        "name": "中スポーツセンター",
        "area": "伏見",
        "category": "スポーツ・運動",
        "min_budget": 300,
        "max_budget": 1500,
        "min_hours": 1.0,
        "max_hours": 3.0,
        "tags": ["体を動かしたい", "運動系", "コスパ重視", "健康的", "雨でも安心"],
        "url": "https://www.nagoya-naka-sc.jp/",
        "points": [
            "低予算で体を動かしやすく、学生でも利用しやすい",
            "伏見周辺から行きやすく、都心で運動したい時に使いやすい",
            "普通の外食やカフェとは違う、健康的な遊びとして提案できる"
        ],
        "best_for": "安く体を動かしたい、健康的な遊びをしたいグループ"
    },
    {
        "name": "大須商店街",
        "area": "大須",
        "category": "街歩き・散策",
        "min_budget": 800,
        "max_budget": 3000,
        "min_hours": 1.5,
        "max_hours": 5.0,
        "tags": ["ワイワイ系", "映え重視", "コスパ重視", "歩き回りたい", "食べ歩き"],
        "url": "https://osu.nagoya/",
        "points": [
            "食べ歩き・古着・雑貨など、遊び方をその場で変えやすい",
            "予算が低めでも楽しみやすく、大学生グループと相性が良い",
            "1つの店に絞りにくい時でも、エリア全体で楽しめるため失敗しにくい"
        ],
        "best_for": "予定を細かく決めすぎず、ワイワイ歩きながら楽しみたいグループ"
    },
    {
        "name": "オアシス21",
        "area": "栄",
        "category": "街歩き・散策",
        "min_budget": 0,
        "max_budget": 2500,
        "min_hours": 0.5,
        "max_hours": 2.5,
        "tags": ["映え重視", "駅近", "夜向き", "散歩", "コスパ重視", "会話重視"],
        "url": "https://www.sakaepark.co.jp/",
        "points": [
            "栄駅周辺で集合しやすく、短時間でも立ち寄りやすい",
            "写真を撮る・散歩する・周辺でご飯に行くなど、次の行動につなげやすい",
            "予算を抑えたい時でも使いやすく、軽い遊びに向いている"
        ],
        "best_for": "お金をかけすぎず、栄周辺で軽く遊びたいグループ"
    },
    {
        "name": "中部電力 MIRAI TOWER",
        "area": "栄",
        "category": "街歩き・散策",
        "min_budget": 1000,
        "max_budget": 2500,
        "min_hours": 1.0,
        "max_hours": 2.5,
        "tags": ["映え重視", "夜向き", "非日常感", "駅近", "デート"],
        "url": "https://www.nagoya-tv-tower.co.jp/",
        "points": [
            "栄の中心にあり、集合場所として分かりやすい",
            "景色や写真映えを楽しめるため、普段の外食とは違う体験になる",
            "周辺に飲食店や商業施設が多く、次の予定にもつなげやすい"
        ],
        "best_for": "栄で少し特別感のある遊びをしたいグループ"
    },
    {
        "name": "名古屋市科学館",
        "area": "伏見",
        "category": "屋内体験",
        "min_budget": 400,
        "max_budget": 1500,
        "min_hours": 1.5,
        "max_hours": 4.0,
        "tags": ["落ち着いた系", "体験重視", "雨でも安心", "コスパ重視", "知的"],
        "url": "https://www.ncsm.city.nagoya.jp/",
        "points": [
            "屋内施設なので天候に左右されにくい",
            "展示やプラネタリウムなど、会話のきっかけになる要素が多い",
            "比較的低予算で、普通の外食とは違う体験ができる"
        ],
        "best_for": "雨の日や、ただのご飯以外の遊びを探しているグループ"
    },
    {
        "name": "ミッドランドスクエア シネマ",
        "area": "名古屋駅",
        "category": "映画・エンタメ",
        "min_budget": 2000,
        "max_budget": 4500,
        "min_hours": 2.5,
        "max_hours": 5.0,
        "tags": ["落ち着いた系", "雨でも安心", "映画", "会話重視", "駅近"],
        "url": "https://www.midland-sq-cinema.jp/",
        "points": [
            "名古屋駅周辺で集合しやすく、雨の日でも予定を立てやすい",
            "映画の後に感想を話せるため、会話の流れが自然に生まれる",
            "遊びの目的がはっきりするので、グループ内で合意を取りやすい"
        ],
        "best_for": "名駅集合で、落ち着いた遊びをしたいグループ"
    },
    {
        "name": "名古屋港水族館",
        "area": "名古屋港",
        "category": "水族館・動植物園",
        "min_budget": 2000,
        "max_budget": 4500,
        "min_hours": 2.0,
        "max_hours": 5.0,
        "tags": ["映え重視", "非日常感", "体験重視", "デート", "落ち着いた系"],
        "url": "https://nagoyaaqua.jp/",
        "points": [
            "水族館という非日常感があり、普段の外食とは違う体験になる",
            "展示を見る流れがあるため、会話が途切れにくい",
            "デート・友人グループのどちらにも使いやすい"
        ],
        "best_for": "少し特別感のある遊びにしたいグループ"
    },
    {
        "name": "東山動植物園",
        "area": "東山公園",
        "category": "水族館・動植物園",
        "min_budget": 500,
        "max_budget": 2500,
        "min_hours": 2.0,
        "max_hours": 5.0,
        "tags": ["コスパ重視", "歩き回りたい", "体験重視", "昼向き", "落ち着いた系"],
        "url": "https://www.higashiyama.city.nagoya.jp/",
        "points": [
            "低予算で長時間楽しみやすく、大学生にも使いやすい",
            "動物園・植物園を歩きながら過ごせるため、自然に会話が生まれやすい",
            "昼の予定として組みやすく、カフェやご飯にもつなげやすい"
        ],
        "best_for": "昼からゆっくり遊びたい、コスパ重視のグループ"
    },
    {
        "name": "コンパル 大須本店",
        "area": "大須",
        "category": "ご飯・カフェ",
        "min_budget": 1000,
        "max_budget": 2500,
        "min_hours": 1.0,
        "max_hours": 2.5,
        "tags": ["落ち着いた系", "会話重視", "名古屋めし", "雨でも安心", "コスパ重視"],
        "url": "https://www.konparu.co.jp/shop/",
        "points": [
            "名古屋らしい喫茶店体験ができ、県外の友人にも紹介しやすい",
            "会話しながら過ごしやすく、短時間の外食・カフェ利用に向いている",
            "大須散策と組み合わせやすく、遊びの前後にも使いやすい"
        ],
        "best_for": "落ち着いて話したいけど、名古屋らしさも少し入れたいグループ"
    },
    {
        "name": "矢場とん 矢場町本店",
        "area": "大須",
        "category": "ご飯・カフェ",
        "min_budget": 1800,
        "max_budget": 3500,
        "min_hours": 1.0,
        "max_hours": 2.5,
        "tags": ["ワイワイ系", "名古屋めし", "食事重視", "定番", "観光感"],
        "url": "https://www.yabaton.com/",
        "points": [
            "名古屋名物として知名度が高く、初めて行くメンバーにも説明しやすい",
            "食事メインで予定を決めたい時に、目的がはっきりしていて迷いにくい",
            "大須・栄方面の遊びと組み合わせやすい"
        ],
        "best_for": "名古屋らしいご飯を中心に、分かりやすく行き先を決めたいグループ"
    },
    {
        "name": "山本屋本店 栄本町通店",
        "area": "栄",
        "category": "ご飯・カフェ",
        "min_budget": 1500,
        "max_budget": 3500,
        "min_hours": 1.0,
        "max_hours": 2.5,
        "tags": ["落ち着いた系", "名古屋めし", "食事重視", "会話重視", "雨でも安心"],
        "url": "https://yamamotoyahonten.co.jp/",
        "points": [
            "名古屋めしとして分かりやすく、県外の友人にも提案しやすい",
            "食事を中心に予定を決めたい時に、目的が明確になる",
            "栄周辺の予定と組み合わせやすい"
        ],
        "best_for": "落ち着いて名古屋らしい食事をしたいグループ"
    }
]


def map_url(place_name):
    query = urllib.parse.quote(place_name + " 名古屋")
    return f"https://www.google.com/maps/search/?api=1&query={query}"


def calculate_score(spot, area, category, budget, vibes, stay_hours):
    score = 0

    # 1. 遊びジャンルを最優先
    if category != "おまかせ":
        if spot["category"] == category:
            score += 220
        else:
            score -= 140

    # 2. 運動系を選んだ場合は、運動スポットを強制的に優遇
    sports_words = {"体を動かしたい", "運動系", "アクティブ", "グループ向き"}
    wants_sports = any(v in sports_words for v in vibes)

    if wants_sports:
        if spot["category"] == "スポーツ・運動":
            score += 180
        else:
            score -= 160

    # 3. エリア
    if area == spot["area"]:
        score += 45
    elif area == "その他":
        score += 5
    else:
        score += 0

    # 4. 予算
    if spot["min_budget"] <= budget <= spot["max_budget"]:
        score += 35
    elif budget < spot["min_budget"]:
        score += max(0, 18 - int((spot["min_budget"] - budget) / 250))
    else:
        score += max(0, 18 - int((budget - spot["max_budget"]) / 350))

    # 5. 雰囲気タグ
    matched = set(vibes) & set(spot["tags"])
    score += len(matched) * 14

    # 6. 滞在時間
    if spot["min_hours"] <= stay_hours <= spot["max_hours"]:
        score += 25
    else:
        center = (spot["min_hours"] + spot["max_hours"]) / 2
        score += max(0, 12 - int(abs(stay_hours - center) * 4))

    return score


def choose_spot(area, custom_area, category, budget, vibes, stay_hours):
    ranked = []

    for spot in SPOTS:
        score = calculate_score(spot, area, category, budget, vibes, stay_hours)
        ranked.append((score, spot))

    ranked.sort(key=lambda item: item[0], reverse=True)
    best_score, best_spot = ranked[0]

    display_area = custom_area.strip() if area == "その他" and custom_area.strip() else area

    matched_vibes = [v for v in vibes if v in best_spot["tags"]]
    if not matched_vibes:
        matched_vibes = ["今回の条件"]

    reason_points = [
        f"遊びジャンル：{category}の希望に合うスポットとして選定",
        f"予算感：1人あたり{budget:,}円前後で検討しやすい",
        f"滞在時間：{stay_hours:g}時間の予定に合わせやすい",
        f"雰囲気：{', '.join(matched_vibes)}という希望と相性が良い",
    ] + best_spot["points"]

    summary = (
        f"今回の条件は「{display_area}周辺」「{category}」「予算{budget:,}円くらい」"
        f"「滞在時間{stay_hours:g}時間」「{', '.join(vibes)}」。"
        f"JAMJAMは、この条件に最も合う1つの行き先として「{best_spot['name']}」を選びました。"
    )

    share_text = (
        f"【JAMJAM Whereからのおすすめ】\n"
        f"今回の行き先は「{best_spot['name']}」がおすすめです。\n\n"
        f"おすすめする理由\n"
        f"・今回の遊びジャンル「{category}」に合っている\n"
        f"・予算{budget:,}円くらいで検討しやすい\n"
        f"・{stay_hours:g}時間くらいの予定に合わせやすい\n"
        f"・{', '.join(matched_vibes)}という雰囲気に合っている\n"
        f"・{best_spot['best_for']}\n\n"
        f"候補を増やして迷うより、今回はここで決めるのがよさそうです。"
    )

    return best_spot, summary, reason_points, share_text


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">JAMJAM Where</div>
        <div class="hero-subtitle">
            大学生の「どこ行く？」を、AIがたった1つの答えに変える。<br>
            探すアプリではなく、決めるアプリ。
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="mini-copy">
        友達と遊ぶ予定はある。でも場所が決まらない。<br>
        JAMJAMは、条件に合う遊び先を候補一覧ではなく「1つの答え」として提案します。
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Inputs
# -----------------------------
st.subheader("今日の条件を入力")

area = st.selectbox(
    "集合場所",
    [
        "名古屋駅",
        "栄",
        "大須",
        "伏見",
        "名古屋港",
        "東山公園",
        "千種",
        "南大高",
        "その他"
    ],
    index=0
)

custom_area = ""
if area == "その他":
    custom_area = st.text_input("集合場所を入力", placeholder="例：藤が丘、星ヶ丘、金山 など")

category = st.selectbox(
    "遊びジャンル",
    [
        "おまかせ",
        "スポーツ・運動",
        "ご飯・カフェ",
        "街歩き・散策",
        "屋内体験",
        "映画・エンタメ",
        "水族館・動植物園"
    ],
    index=0
)

budget = st.slider(
    "1人あたりの予算",
    min_value=0,
    max_value=5000,
    value=2000,
    step=500,
    format="%d円"
)

vibes = st.multiselect(
    "遊びの雰囲気",
    [
        "ワイワイ系",
        "落ち着いた系",
        "映え重視",
        "コスパ重視",
        "会話重視",
        "駅近",
        "雨でも安心",
        "歩き回りたい",
        "長居したい",
        "非日常感",
        "体験重視",
        "体を動かしたい",
        "運動系",
        "アクティブ",
        "グループ向き",
        "名古屋めし",
        "食事重視",
        "夜向き",
        "昼向き",
        "デート",
        "健康的"
    ],
    default=["ワイワイ系", "コスパ重視"]
)

stay_hours = st.number_input(
    "滞在時間",
    min_value=0.5,
    max_value=8.0,
    value=2.0,
    step=0.5,
    format="%.1f"
)

st.markdown("")

# -----------------------------
# Result
# -----------------------------
if st.button("この場所で決める！"):
    if area == "その他" and not custom_area.strip():
        st.warning("集合場所を入力してください。")
    elif not vibes:
        st.warning("遊びの雰囲気を1つ以上選んでください。")
    else:
        with st.spinner("AIマッチング中..."):
            time.sleep(3)

        best_spot, summary, reason_points, share_text = choose_spot(
            area=area,
            custom_area=custom_area,
            category=category,
            budget=budget,
            vibes=vibes,
            stay_hours=stay_hours
        )

        points_html = "".join(
            [f"<li>{html.escape(point)}</li>" for point in reason_points]
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">JAMJAMが出した、たった1つの答え</div>
                <div class="result-title">{html.escape(best_spot["name"])}</div>
                <div class="reason-box">
                    <b>JAMJAMがここに決めた理由</b><br>
                    {html.escape(summary)}
                    <ul class="point-list">
                        {points_html}
                    </ul>
                    <div class="best-for">
                        <b>特におすすめのグループ</b><br>
                        {html.escape(best_spot["best_for"])}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 詳細を見る")
        col1, col2 = st.columns(2)

        with col1:
            st.link_button("公式サイトを見る", best_spot["url"], use_container_width=True)

        with col2:
            st.link_button("Googleマップで見る", map_url(best_spot["name"]), use_container_width=True)

st.markdown("### グループに送る文章")

st.text_area(
    "LINEやInstagramのグループに送れる文章です",
    value=share_text,
    height=230
)

st_copy_button(
    text=share_text,
    before_copy_label="📋 グループ共有文をコピー",
    after_copy_label="✅ コピーしました",
    show_text=False
)

st.markdown(
    """
    <div class="small-note">
        ※これはビジネスコンテスト用MVPです。実際のサービスでは、口コミ・距離・混雑・予約可否・クーポンなども加味して精度を高めます。
    </div>
    """,
    unsafe_allow_html=True
)

else:
    st.markdown(
        """
        <div class="small-note">
            条件を入力してボタンを押すと、JAMJAMが候補を並べずに1つだけ決めます。
        </div>
        """,
        unsafe_allow_html=True
    )
