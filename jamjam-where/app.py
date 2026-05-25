import time
import html
import urllib.parse
import streamlit as st

st.set_page_config(
    page_title="JAMJAM Where",
    page_icon="📍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #fff7ed 0%, #ffffff 45%, #f8fafc 100%);
    }

    .block-container {
        max-width: 560px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        padding: 1.4rem 1.2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #ff8a3d 0%, #ff4f7b 100%);
        color: white;
        box-shadow: 0 12px 30px rgba(255, 111, 97, 0.22);
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.95;
    }

    .mini-copy {
        padding: 0.75rem 0.9rem;
        border-radius: 16px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412;
        font-size: 0.92rem;
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
        font-weight: 700;
        color: #f97316;
        margin-bottom: 0.3rem;
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
        line-height: 1.8;
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
        font-weight: 800;
        background: linear-gradient(135deg, #ff8a3d 0%, #ff4f7b 100%);
        color: white;
        border: none;
        box-shadow: 0 10px 22px rgba(255, 79, 123, 0.25);
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(255, 79, 123, 0.28);
        color: white;
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
# Candidate data
# -----------------------------
SPOTS = [
    {
        "name": "大須商店街",
        "area": "大須",
        "min_budget": 800,
        "max_budget": 3000,
        "tags": ["ワイワイ系", "映え重視", "コスパ重視", "歩き回りたい", "食べ歩き"],
        "min_hours": 1.5,
        "max_hours": 5.0,
        "url": "https://osu.nagoya/",
        "points": [
            "食べ歩き・古着・雑貨・ゲームセンターなど、遊び方をその場で変えやすい",
            "予算が低めでも楽しみやすく、大学生グループと相性が良い",
            "1つの店に絞りにくい時でも、エリア全体で楽しめるため失敗しにくい"
        ],
        "best_for": "予定を細かく決めすぎず、ワイワイ歩きながら楽しみたいグループ"
    },
    {
        "name": "コンパル 大須本店",
        "area": "大須",
        "min_budget": 1000,
        "max_budget": 2500,
        "tags": ["落ち着いた系", "会話重視", "名古屋めし", "雨でも安心", "コスパ重視"],
        "min_hours": 1.0,
        "max_hours": 2.5,
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
        "min_budget": 1800,
        "max_budget": 3500,
        "tags": ["ワイワイ系", "名古屋めし", "食事重視", "定番", "観光感"],
        "min_hours": 1.0,
        "max_hours": 2.5,
        "url": "https://www.yabaton.com/",
        "points": [
            "名古屋名物として知名度が高く、初めて行くメンバーにも説明しやすい",
            "食事メインで予定を決めたい時に、目的がはっきりしていて迷いにくい",
            "大須・栄方面の遊びと組み合わせやすい"
        ],
        "best_for": "名古屋らしいご飯を中心に、分かりやすく行き先を決めたいグループ"
    },
    {
        "name": "オアシス21",
        "area": "栄",
        "min_budget": 0,
        "max_budget": 2500,
        "tags": ["映え重視", "駅近", "夜向き", "散歩", "コスパ重視", "会話重視"],
        "min_hours": 0.5,
        "max_hours": 2.5,
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
        "min_budget": 1000,
        "max_budget": 2500,
        "tags": ["映え重視", "夜向き", "非日常感", "駅近", "デート"],
        "min_hours": 1.0,
        "max_hours": 2.5,
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
        "min_budget": 400,
        "max_budget": 1500,
        "tags": ["落ち着いた系", "体験重視", "雨でも安心", "コスパ重視", "知的"],
        "min_hours": 1.5,
        "max_hours": 4.0,
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
        "min_budget": 2000,
        "max_budget": 4500,
        "tags": ["落ち着いた系", "雨でも安心", "映画", "会話重視", "駅近"],
        "min_hours": 2.5,
        "max_hours": 5.0,
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
        "min_budget": 2000,
        "max_budget": 4500,
        "tags": ["映え重視", "非日常感", "体験重視", "デート", "落ち着いた系"],
        "min_hours": 2.0,
        "max_hours": 5.0,
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
        "min_budget": 500,
        "max_budget": 2500,
        "tags": ["コスパ重視", "歩き回りたい", "体験重視", "昼向き", "落ち着いた系"],
        "min_hours": 2.0,
        "max_hours": 5.0,
        "url": "https://www.higashiyama.city.nagoya.jp/",
        "points": [
            "低予算で長時間楽しみやすく、大学生にも使いやすい",
            "動物園・植物園を歩きながら過ごせるため、自然に会話が生まれやすい",
            "昼の予定として組みやすく、カフェやご飯にもつなげやすい"
        ],
        "best_for": "昼からゆっくり遊びたい、コスパ重視のグループ"
    },
    {
        "name": "山本屋本店 栄本町通店",
        "area": "栄",
        "min_budget": 1500,
        "max_budget": 3500,
        "tags": ["落ち着いた系", "名古屋めし", "食事重視", "会話重視", "雨でも安心"],
        "min_hours": 1.0,
        "max_hours": 2.5,
        "url": "https://yamamotoyahonten.co.jp/",
        "points": [
            "名古屋めしとして分かりやすく、県外の友人にも提案しやすい",
            "食事を中心に予定を決めたい時に、目的が明確になる",
            "栄周辺の予定と組み合わせやすい"
        ],
        "best_for": "落ち着いて名古屋らしい食事をしたいグループ"
    },
    {
        "name": "ラウンドワン 千種店",
        "area": "千種",
        "min_budget": 1500,
        "max_budget": 4500,
        "tags": ["ワイワイ系", "体を動かしたい", "運動系", "雨でも安心", "長居したい", "グループ向き"],
        "min_hours": 2.0,
        "max_hours": 6.0,
        "url": "https://www.round1.co.jp/shop/tenpo/aichi-tikusa.html",
        "points": [
            "ボウリング・ビリヤード・ダーツ・卓球など、グループで盛り上がりやすい遊びがある",
            "屋内施設なので天候に左右されにくい",
            "会話だけでなく実際に体を動かせるため、初対面や距離感のあるグループでも使いやすい"
        ],
        "best_for": "体を動かしながら、みんなでワイワイ遊びたいグループ"
    },
    {
        "name": "名古屋グランドボウル",
        "area": "南大高",
        "min_budget": 1500,
        "max_budget": 4000,
        "tags": ["ワイワイ系", "体を動かしたい", "運動系", "グループ向き", "雨でも安心"],
        "min_hours": 1.5,
        "max_hours": 4.0,
        "url": "https://www.grandbowl.jp/nagoya/",
        "points": [
            "ボウリングを中心に、グループ全員で同じ体験を共有しやすい",
            "勝負やチーム分けができるため、自然に盛り上がりやすい",
            "飲食だけでは物足りない時に、遊びとしての満足感を作りやすい"
        ],
        "best_for": "ご飯だけでなく、体を動かす遊びを入れたいグループ"
    },
    {
        "name": "中スポーツセンター",
        "area": "伏見",
        "min_budget": 300,
        "max_budget": 1500,
        "tags": ["体を動かしたい", "運動系", "コスパ重視", "落ち着いた系", "健康的"],
        "min_hours": 1.0,
        "max_hours": 3.0,
        "url": "https://www.nespa.or.jp/facility/naka_sc/",
        "points": [
            "低予算で体を動かしやすく、学生でも利用しやすい",
            "伏見駅周辺から行きやすく、都心で運動したい時に使いやすい",
            "普通の外食やカフェとは違う、健康的な遊びとして提案できる"
        ],
        "best_for": "安く体を動かしたい、健康的な遊びをしたいグループ"
    }
]


def calculate_score(spot, area, budget, vibes, stay_hours):
    score = 0

    if area == spot["area"]:
        score += 35
    elif area == "その他":
        score += 10
    else:
        score += 4

    if spot["min_budget"] <= budget <= spot["max_budget"]:
        score += 30
    elif budget < spot["min_budget"]:
        score += max(0, 14 - int((spot["min_budget"] - budget) / 300))
    else:
        score += max(0, 18 - int((budget - spot["max_budget"]) / 400))

    matched_tags = set(vibes) & set(spot["tags"])
    score += len(matched_tags) * 12

    if spot["min_hours"] <= stay_hours <= spot["max_hours"]:
        score += 18
    else:
        center_hours = (spot["min_hours"] + spot["max_hours"]) / 2
        score += max(0, 10 - int(abs(stay_hours - center_hours) * 3))

    return score


def make_map_url(place_name):
    query = urllib.parse.quote(place_name + " 名古屋")
    return f"https://www.google.com/maps/search/?api=1&query={query}"


def choose_spot(area, custom_area, budget, vibes, stay_hours):
    scored_spots = []

    for spot in SPOTS:
        score = calculate_score(spot, area, budget, vibes, stay_hours)
        scored_spots.append((score, spot))

    scored_spots.sort(key=lambda x: x[0], reverse=True)
    best_spot = scored_spots[0][1]

    display_area = custom_area if area == "その他" and custom_area else area

    matched_vibes = [tag for tag in vibes if tag in best_spot["tags"]]
    if not matched_vibes:
        matched_vibes = vibes[:2] if vibes else ["今日の条件"]

    decision_summary = (
        f"今回の条件は「{display_area}周辺」「予算{budget:,}円くらい」"
        f"「滞在時間{stay_hours:g}時間」「{', '.join(vibes)}」。"
        f"この条件に対して、JAMJAMは「{best_spot['name']}」を最も相性が良い行き先として選びました。"
    )

    reason_points = [
        f"集合場所・移動のしやすさ：{display_area}周辺の条件をもとに選定",
        f"予算感：1人あたり{budget:,}円前後の条件で検討しやすい",
        f"雰囲気：{', '.join(matched_vibes)}という希望に合いやすい",
    ] + best_spot["points"]

    line_text = (
        f"【JAMJAM Whereからのおすすめ】\n"
        f"今回の行き先は「{best_spot['name']}」がおすすめです。\n\n"
        f"おすすめする理由\n"
        f"・集合場所や移動の条件をもとに選ばれている\n"
        f"・予算{budget:,}円くらいで検討しやすい\n"
        f"・{', '.join(matched_vibes)}という今回の雰囲気に合っている\n"
        f"・{best_spot['best_for']}\n\n"
        f"候補を増やして迷うより、今回はここで決めるのがよさそうです。"
    )

    return best_spot, decision_summary, reason_points, line_text


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
        JAMJAMは、人数・予算・雰囲気から、今日の行き先を1つに絞ります。
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
        "金山",
        "伏見",
        "名古屋港",
        "東山公園",
        "千種",
        "南大高",
        "大学周辺",
        "その他"
    ],
    index=0
)

custom_area = ""
if area == "その他":
    custom_area = st.text_input("集合場所を入力", placeholder="例：藤が丘、星ヶ丘、豊田市駅 など")

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
# Decision button
# -----------------------------
if st.button("この場所で決める！"):
    if area == "その他" and not custom_area.strip():
        st.warning("集合場所を入力してください。")
    elif not vibes:
        st.warning("遊びの雰囲気を1つ以上選んでください。")
    else:
        with st.spinner("AIマッチング中..."):
            time.sleep(3)

        best_spot, decision_summary, reason_points, line_text = choose_spot(
            area=area,
            custom_area=custom_area.strip(),
            budget=budget,
            vibes=vibes,
            stay_hours=stay_hours
        )

        points_html = "".join([f"<li>{html.escape(point)}</li>" for point in reason_points])

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">JAMJAMが出した、たった1つの答え</div>
                <div class="result-title">{html.escape(best_spot["name"])}</div>
                <div class="reason-box">
                    <b>JAMJAMがここに決めた理由</b><br>
                    {html.escape(decision_summary)}
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
            st.link_button("Googleマップで見る", make_map_url(best_spot["name"]), use_container_width=True)

        st.markdown("### グループに送る文章")
        st.text_area(
            "コピーしてLINEやInstagramのグループに送れます",
            value=line_text,
            height=220,
            label_visibility="collapsed"
        )

        st.caption("上の文章を選択してコピーできます。下のコード表示は右上のコピーアイコンからコピーできます。")
        st.code(line_text, language="text")

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
