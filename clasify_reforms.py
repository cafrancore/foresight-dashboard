

import pandas as pd
from sentence_transformers import SentenceTransformer, util


# 1. Define categories and keywords (as above)
categories = {
    "Climate Change": [
        "tipping","adaptation","warming","drought","flooding","displacement",
        "conflict","mortality","desertification","food","security","famine",
        "agriculture","heatwaves","vulnerability","resilience","oceans",
        "ice","melting","sea","levels"
    ],
    "Demographic Change": [
        "mental","health","gender","equality","backlash","youth","migration",
        "population","cohesion","instability"
    ],
    "Labour Market": [
        "work","visas","skills","training","education","employment","jobs",
        "unemployment","investment","markets","talent","opportunities",
        "collaboration","reskilling"
    ],
    "Digital Technology": [
        "privacy","exclusion","bias","AI","bots","platforms","superapps",
        "blockchain","NFTs","cryptocurrencies","philanthropy","donors",
        "impact","infrastructure","cybersecurity","trust"
    ],
    "Biotech": [
        "biotech","biology","digitalisation","genomics","innovation",
        "health","ethics"
    ],
    "Global Governance": [
        "debt","distress","financing","conflict","framework","eligibility",
        "suspension","default","burden","expenditure"
    ],
    "Misinformation": [
        "misinformation","disinformation","deepfakes","conspiracy","trust",
        "media","literacy","confusion","ecosystem"
    ],
    "Economic Pressures": [
        "public","debt","spending","education","health","investment","fiscal",
        "development","services"
    ],
    "Inequality": [
        "inequality","collapse","ecosystems","distribution","access","income","poverty"
    ]
}

# 2. Flatten into keyword → category mapping
keywords = []
keyword_to_category = {}
for cat, kw_list in categories.items():
    for kw in kw_list:
        keywords.append(kw)
        keyword_to_category[kw.lower()] = cat   # lowercase for consistency

# 3. Load Excel (replace with your actual file)
df = pd.read_excel("reforms.xlsx")  # must contain a 'summary' column

# 4. Load model
model = SentenceTransformer("all-MiniLM-L6-v2")
keyword_embeddings = model.encode(keywords, convert_to_tensor=True)

# 5. Function to classify
def classify_text(text):
    if pd.isna(text):
        return None, None
    text_embedding = model.encode(text, convert_to_tensor=True)
    similarities = util.cos_sim(text_embedding, keyword_embeddings)
    best_match_idx = similarities.argmax().item()
    best_keyword = keywords[best_match_idx]
    best_category = keyword_to_category[best_keyword.lower()]
    return best_keyword, best_category

# 6. Apply classification
df[["foresight_keyword", "foresight_category"]] = df["summary"].apply(
    lambda x: pd.Series(classify_text(x))
)

# 7. Save results
df.to_excel("classified_reforms.xlsx", index=False)

print("✅ Classification complete! Check classified_reforms.xlsx")
