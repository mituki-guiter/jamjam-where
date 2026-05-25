import time
import html
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

    .share-box {
        padding: 1rem;
        border-radius: 18px;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        line-height: 1.7;
        margin-top: 0.8rem;
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
# Candidate data
# -----------------------------
SPOTS = [
    {
        "name": "大須商店街 食べ歩き＆古着めぐり",
        "area": "大須",
        "min_budget": 800,
        "max_budget": 3000,
        "tags": ["ワイワイ系", "映え重視", "コスパ重視", "歩き回りたい"],
        "min_hours": 1.5,
        "max_hours": 5.0,
        "description": "食べ歩き、古着、雑貨、ゲームセンターなどをまとめて楽しめるため、グループでも会話が続きやすい遊び先です。"
    },
    {
        "name": "栄・オアシス21周辺 カフェ＆夜景さんぽ",
        "area": "栄",
        "min_budget": 1000,
        "max_budget": 3500,
        "tags": ["落ち着いた系", "映え重視", "会話重視", "駅近"],
        "min_hours": 1.0,
        "max_hours": 4.0,
        "description": "アクセスが良く、カフェ・ショッピング・夜景を組み合わせやすいため、初めて行くメンバーでも外しにくい場所です。"
    },
    {
        "name": "名古屋駅周辺 カフェ＆地下街ぶらり",
        "area": "名古屋駅",
        "min_budget": 1200,
        "max_budget": 4000,
        "tags": ["駅近", "落ち着いた系", "会話重視", "雨でも安心"],
        "min_hours": 1.0,
        "max_hours": 4.0,
        "description": "集合しやすく、天気に左右されにくい地下街やカフェが多いため、予定が固まりきっていない日にも使いやすい選択です。"
    },
    {
        "name": "金山駅周辺 ごはん＆ゆったり二次会",
        "area": "金山",
        "min_budget": 1500,
        "max_budget": 4500,
        "tags": ["ワイワイ系", "駅近", "会話重視", "夜向き"],
        "min_hours": 2.0,
        "max_hours": 5.0,
        "description": "複数路線から集まりやすく、ごはん後の二次会にも移りやすいため、グループでの予定に向いています。"
    },
    {
        "name": "大学周辺 カラオケ＆ファミレス作戦",
        "area": "大学周辺",
        "min_budget": 1000,
        "max_budget": 3000,
        "tags": ["ワイワイ系", "コスパ重視", "長居したい", "近場"],
        "min_hours": 2.0,
        "max_hours": 6.0,
        "description": "移動コストを抑えつつ、カラオケやファミレスで長く過ごせるため、急に決まった遊びにも対応しやすいプランです。"
    },
    {
        "name": "ボウリング＆ゲームセンターで軽く勝負",
        "area": "名古屋駅",
        "min_budget": 1500,
        "max_budget": 4000,
        "tags": ["ワイワイ系", "体験重視", "雨でも安心", "グループ向き"],
        "min_hours": 1.5,
        "max_hours": 4.0,
        "description": "会話だけでなく一緒に遊ぶ体験があるため、まだ距離感のあるメンバー同士でも盛り上がりやすい選択です。"
    },
    {
        "name": "映画館＋カフェで感想会プラン",
        "area": "栄",
        "min_budget": 2200,
        "max_budget": 5000,
        "tags": ["落ち着いた系", "会話重視", "雨でも安心", "非日常感"],
        "min_hours": 3.0,
        "max_hours": 6.0,
        "description": "映画を見たあとにカフェで感想を話せるため、話題に困りにくく、落ち着いた遊びに向いています。"
    },
    {
        "name": "大須カフェ巡り＆写真スポット散歩",
        "area": "大須",
        "min_budget": 1200,
        "max_budget": 3500,
        "tags": ["映え重視", "落ち着いた系", "歩き回りたい", "コスパ重視"],
        "min_hours": 2.0,
        "max_hours": 5.0,
        "description": "カフェ、雑貨、写真スポットをゆるく回れるため、予定を詰めすぎずに楽しみたい日に合っています。"
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
        score += max(0, 10 - int(abs(stay_hours - ((spot["min_hours"] + spot["max_hours"]) / 2)) * 3))

    return score


def choose_spot(area, custom_area, budget, vibes, stay_hours):
    scored_spots = []

    for spot in SPOTS:
        score = calculate_score(spot, area, budget, vibes, stay_hours)
        scored_spots.append((score, spot))

    scored_spots.sort(key=lambda x: x[0], reverse=True)
    best_spot = scored_spots[0][1]

    display_area = custom_area if area == "その他" and custom_area else area

    matched_vibes = list(set(vibes) & set(best_spot["tags"]))
    if not matched_vibes:
        matched_vibes = vibes[:2] if vibes else ["今日の条件"]

    reason = (
        f"今回は「{display_area}周辺」「予算{budget:,}円くらい」「滞在時間{stay_hours:g}時間」"
        f"という条件に加えて、{', '.join(matched_vibes)}という雰囲気が重視されていました。"
        f"{best_spot['name']}は、条件に対して移動・予算・過ごしやすさのバランスが良く、"
        f"グループ内で説明しやすい理由もあるため、JAMJAMはこの1つに決めました。"
        f"{best_spot['description']}"
    )

    line_text = (
        f"今日の行き先、JAMJAMで見たら「{best_spot['name']}」が一番合ってそう！\n\n"
        f"理由は、{display_area}周辺で集まりやすくて、予算{budget:,}円くらいに収まりやすいのと、"
        f"{', '.join(matched_vibes)}っていう今日の雰囲気に合ってるから。\n\n"
        f"候補を増やすより、今回はここで決めちゃうのが良さそう！どう？"
    )

    return best_spot, reason, line_text


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
    ["名古屋駅", "栄", "大須", "金山", "大学周辺", "その他"],
    index=0
)

custom_area = ""
if area == "その他":
    custom_area = st.text_input("集合場所を入力", placeholder="例：藤が丘、星ヶ丘、豊田市駅 など")

budget = st.slider(
    "1人あたりの予算",
    min_value=500,
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
        "体験重視"
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
        with st.spinner("AIが最適な場所を吟味中..."):
            time.sleep(3)

        best_spot, reason, line_text = choose_spot(
            area=area,
            custom_area=custom_area.strip(),
            budget=budget,
            vibes=vibes,
            stay_hours=stay_hours
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">JAMJAMが出した、たった1つの答え</div>
                <div class="result-title">{html.escape(best_spot["name"])}</div>
                <div class="reason-box">
                    <b>なぜここにしたのか</b><br>
                    {html.escape(reason)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### そのままLINEで送る文章")
        st.text_area(
            "コピーしてグループに送れます",
            value=line_text,
            height=170,
            label_visibility="collapsed"
        )

        escaped_line_text = html.escape(line_text).replace("\n", "\\n")

        st.components.v1.html(
            f"""
            <div style="margin-top: -4px;">
                <button
                    onclick="navigator.clipboard.writeText(`{escaped_line_text}`).then(() => {{
                        const msg = document.getElementById('copy-message');
                        msg.innerText = 'コピーしました！そのままLINEに送れます。';
                    }})"
                    style="
                        width: 100%;
                        border: none;
                        border-radius: 999px;
                        padding: 13px 18px;
                        font-size: 15px;
                        font-weight: 800;
                        cursor: pointer;
                        background: linear-gradient(135deg, #22c55e 0%, #14b8a6 100%);
                        color: white;
                        box-shadow: 0 10px 22px rgba(20, 184, 166, 0.22);
                    "
                >
                    LINE用文章をコピー
                </button>
                <div id="copy-message" style="
                    margin-top: 8px;
                    text-align: center;
                    color: #047857;
                    font-size: 13px;
                    font-family: sans-serif;
                "></div>
            </div>
            """,
            height=72
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
