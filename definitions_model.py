import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

# 1. STRATEGIC DEFINITIONS (from your requirements)
category_definitions = {
    "Climate Change": {
        "direct": "Climate change threatens livelihoods through environmental degradation, rising sea levels, and extreme weather events. Direct links include reforms explicitly designed to anticipate, absorb, and adapt to climate impacts, such as adaptive social protection, climate risk insurance, anticipatory cash transfers, and resilience-focused public works.",
        "indirect": "Indirect links include reforms that strengthen households' coping capacity under climate stress, such as food security programmes during crop failures, social insurance expansion for informal workers exposed to heat stress, and infrastructure-oriented public works in vulnerable areas.",
        "keywords": ["climate adaptation", "resilience", "environmental", "extreme weather", "sea levels", "drought", "flood", "displacement", "climate insurance", "anticipatory", "adaptive social protection"]
    },

    "Demographic Change": {
        "direct": "Ageing populations, migration, and changing family structures create new social protection pressures. Direct measures include pension reforms, long-term care insurance (LTCI), schemes covering refugees and migrants, and systems that track ageing and migration flows.",
        "indirect": "Indirect measures include formalizing migrant employment, developing the care economy, promoting intergenerational solidarity and gender-balanced caregiving, extending working lives, and reskilling older workers.",
        "keywords": ["ageing", "migration", "dependency", "pension", "long-term care", "refugees", "fertility", "urbanization", "displaced", "intergenerational"]
    },

    "Digital Technology": {
        "direct": "Direct digital social protection reforms include deployment of chatbots and virtual assistants, single-window services, digital ID and eKYC rollout, mobile G2P payments, interoperable MIS and registries, and use of AI/ML for targeting, deduplication, fraud detection, and case management.",
        "indirect": "Indirect reforms include stronger data protection and privacy rules, algorithmic governance (fairness, explainability, and audits), trust infrastructure such as verifiable credentials or blockchain, and digital inclusion policies to prevent exclusion and inequality.",
        "keywords": ["digital ID", "mobile payments", "interoperable", "AI", "data protection", "privacy", "cybersecurity", "algorithmic", "digital inclusion", "blockchain"]
    },

    "Shifting Nature of Work": {
        "direct": "Direct policy changes target new forms of employment, including social security extension to platform and gig workers, portable benefits, digital contribution mechanisms, regulation of digital labor platforms, and remote work legislation.",
        "indirect": "Indirect measures include recognition of new worker categories (crowd workers and freelancers), active labor market policies for reskilling and upskilling, integration of digital literacy into education, remote work visa programmes, and curriculum reforms aligned to emerging job profiles.",
        "keywords": ["gig work", "platform workers", "remote work", "portable benefits", "reskilling", "upskilling", "labor platforms", "freelancers", "digital skills", "future of work"]
    },

    "Public Debt Expansion": {
        "direct": "Direct reforms strengthen the architecture and financial sustainability of social security systems. Measures include expanding contributory coverage to excluded workers and groups, improving fraud detection in social security contributions, strengthening governance and investment strategies of reserve funds to improve funding ratios, improving financing forecasts, and adopting adaptive social protection financing that anticipates demographic and economic shocks.",
        "indirect": "Indirect reforms improve the enabling environment for participation and financing. Measures include simplifying administrative procedures, enabling contribution and tax payments through single portals or mobile applications, providing enrollment subsidies such as Monotributo or Monotax schemes, promoting formalization, increasing tax revenues, reducing illicit financial flows, and using environmental taxes (carbon taxes, fuel excise, emissions trading revenues) to generate fiscal space.",
        "keywords": ["public debt", "fiscal space", "social protection financing", "contributory schemes", "reserve funds", "funding ratio", "fraud detection", "monotributo", "monotax", "formalization", "tax revenue", "illicit financial flows", "carbon tax", "fuel excise", "emissions trading"]
    },

    "Changes in Global Order": {
        "direct": "Direct reforms in a fragmented geopolitical context focus on continuity of social protection operations despite weaker multilateral engagement. Measures include strengthening domestic and UN-local coordination mechanisms, reducing dependency on external implementation support, and improving inter-agency operational frameworks.",
        "indirect": "Indirect reforms sustain financing and cooperation by adapting to geopolitical fragmentation through diversified bilateral, regional, and plurilateral partnerships, and expanded strategic alliances beyond traditional development partners.",
        "keywords": ["geopolitical fragmentation", "global order", "multilateralism", "bilateral cooperation", "regional partnerships", "plurilateral", "strategic alliances", "implementation capacity", "coordination mechanisms", "development partners"]
    },

    "Regional Conflicts": {
        "direct": "Direct reforms in conflict contexts strengthen the humanitarian-development-peace (HDP) nexus and continuity of protection. Measures include aligning humanitarian and social protection actors, investing in anticipatory capacity, establishing early warning systems, deploying scalable cash transfer programmes, and using pre-agreed financing triggers for rapid expansion during conflict-induced displacement. Long-term forced migration strategies aligned with human rights standards are also included.",
        "indirect": "Indirect reforms strengthen the broader governance ecosystem in fragile settings through stronger intergovernmental and multi-agency coordination across security, humanitarian, development, and social sectors, and partnerships with civil society and international organizations to maintain service delivery when institutions are weakened.",
        "keywords": ["regional conflict", "forced displacement", "forced migration", "HDP nexus", "humanitarian", "anticipatory action", "early warning", "scalable cash transfers", "financing triggers", "fragile contexts", "multi-agency coordination", "civil society partnerships"]
    }
}

# 2. Load model
model = SentenceTransformer("all-mpnet-base-v2")  # More powerful model for better semantic understanding

# 3. Encode definitions
category_embeddings = {}
for category, details in category_definitions.items():
    # Combine direct/indirect text plus keywords for stronger semantic anchors
    keywords_text = " ".join(details.get("keywords", []))
    full_definition = f"{details['direct']} {details['indirect']} Keywords: {keywords_text}"
    category_embeddings[category] = model.encode(full_definition, convert_to_tensor=True)

# 4. Enhanced classification function
def classify_reform_strategically(text, threshold=0.3):
    """
    Classify reform text based on strategic definitions with confidence scoring
    
    Parameters:
    text: Reform description
    threshold: Minimum similarity score to assign category (0-1)
    
    Returns:
    Dictionary with category, confidence score, and whether it's direct/indirect match
    """
    if pd.isna(text) or not text.strip():
        return {
            "category": "Unclassified",
            "confidence": 0.0,
            "link_type": "None",
            "match_details": {},
            "all_scores": {cat: 0.0 for cat in category_definitions.keys()}
        }
    
    # Encode the reform text
    text_embedding = model.encode(text, convert_to_tensor=True)
    
    # Calculate similarities with all category definitions
    similarities = {}
    for category, cat_embedding in category_embeddings.items():
        similarity = util.cos_sim(text_embedding, cat_embedding).item()
        similarities[category] = similarity
    
    # Find best match
    best_category = max(similarities, key=similarities.get)
    best_score = similarities[best_category]
    
    # Determine if direct or indirect link based on semantic similarity
    direct_embedding = model.encode(category_definitions[best_category]["direct"], convert_to_tensor=True)
    indirect_embedding = model.encode(category_definitions[best_category]["indirect"], convert_to_tensor=True)
    
    direct_sim = util.cos_sim(text_embedding, direct_embedding).item()
    indirect_sim = util.cos_sim(text_embedding, indirect_embedding).item()
    
    # Determine link type
    if direct_sim > indirect_sim and direct_sim > 0.5:
        link_type = "Direct"
        link_score = direct_sim
    elif indirect_sim > 0.4:
        link_type = "Indirect"
        link_score = indirect_sim
    else:
        link_type = "Weak/Unclear"
        link_score = max(direct_sim, indirect_sim)
    
    # Only assign if above threshold
    if best_score < threshold:
        final_category = "Unclassified"
        confidence = best_score
    else:
        final_category = best_category
        confidence = best_score
    
    return {
        "category": final_category,
        "confidence": round(confidence, 3),
        "link_type": link_type,
        "link_strength": round(link_score, 3),
        "all_scores": {cat: round(score, 3) for cat, score in similarities.items()}
    }
# 5. Multi-label classification (reforms can belong to multiple categories)
def classify_reform_multi_label(text, threshold=0.25):
    """
    Classify reform into potentially multiple categories based on strategic definitions
    """
    if pd.isna(text) or not text.strip():
        return []
    
    text_embedding = model.encode(text, convert_to_tensor=True)
    
    matches = []
    for category, cat_embedding in category_embeddings.items():
        similarity = util.cos_sim(text_embedding, cat_embedding).item()
        
        if similarity >= threshold:
            # Check for direct/indirect
            direct_embedding = model.encode(category_definitions[category]["direct"], convert_to_tensor=True)
            indirect_embedding = model.encode(category_definitions[category]["indirect"], convert_to_tensor=True)
            
            direct_sim = util.cos_sim(text_embedding, direct_embedding).item()
            indirect_sim = util.cos_sim(text_embedding, indirect_embedding).item()
            
            link_type = "Direct" if direct_sim > indirect_sim else "Indirect"
            link_score = max(direct_sim, indirect_sim)
            
            matches.append({
                "category": category,
                "overall_similarity": round(similarity, 3),
                "link_type": link_type,
                "link_similarity": round(link_score, 3)
            })
    
    # Sort by similarity score
    matches.sort(key=lambda x: x["overall_similarity"], reverse=True)
    return matches

# 6. Load and process reforms
def analyze_reforms_strategically(input_file="reforms.xlsx", output_file="strategic_classification.xlsx"):
    """
    Complete analysis pipeline with strategic classification
    """
    # Load data
    df = pd.read_excel(input_file)

        # Remove rows with empty/null summary (no information)
    df = df.dropna(subset=['summary'])
    df = df[df['summary'].str.strip() != '']
    
    # Reset index after dropping rows
    df = df.reset_index(drop=True)
    

    
    
    # Apply single best classification
    df["strategic_classification"] = df["summary"].apply(
        lambda x: classify_reform_strategically(x)["category"]
    )
    
    # Apply multi-label classification
    df["multi_label_classification"] = df["summary"].apply(
        lambda x: [m["category"] for m in classify_reform_multi_label(x, threshold=0.25)]
    )
    
    # Get detailed scores for analysis
    classification_details = df["summary"].apply(classify_reform_strategically)
    
    # Expand details into separate columns
    df["classification_confidence"] = classification_details.apply(lambda x: x["confidence"])
    df["link_type"] = classification_details.apply(lambda x: x["link_type"])
    df["link_strength"] = classification_details.apply(
        lambda x: x.get("link_strength") if isinstance(x, dict) else None
    )
    # Calculate which definitions are most relevant
    df["climate_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Climate Change", 0) if isinstance(x, dict) else 0
    )
    df["demographic_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Demographic Change", 0) if isinstance(x, dict) else 0
    )
    df["digital_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Digital Technology", 0) if isinstance(x, dict) else 0
    )
    df["work_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Shifting Nature of Work", 0) if isinstance(x, dict) else 0
    )
    df["public_debt_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Public Debt Expansion", 0) if isinstance(x, dict) else 0
    )
    df["global_order_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Changes in Global Order", 0) if isinstance(x, dict) else 0
    )
    df["regional_conflicts_score"] = classification_details.apply(
        lambda x: (x.get("all_scores") or {}).get("Regional Conflicts", 0) if isinstance(x, dict) else 0
    )
    
    # Flag reforms that address multiple trends
    df["addresses_multiple_trends"] = df["multi_label_classification"].apply(len) > 1
    
    # Save results
    df.to_excel(output_file, index=False)
    
    # Generate summary report
    generate_summary_report(df)
    
    return df

def generate_summary_report(df):
    """
    Generate strategic insights report
    """
    print("\n" + "="*80)
    print("STRATEGIC REFORM ANALYSIS REPORT")
    print("="*80)
    
    # 1. Overall classification distribution
    print(f"\n1. REFORM DISTRIBUTION BY MEGATREND:")
    trend_counts = df["strategic_classification"].value_counts()
    for trend, count in trend_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {trend}: {count} reforms ({percentage:.1f}%)")
    
    # 2. Link type analysis
    print(f"\n2. DIRECT VS INDIRECT LINKAGES:")
    direct_count = len(df[df["link_type"] == "Direct"])
    indirect_count = len(df[df["link_type"] == "Indirect"])
    print(f"   Direct anticipatory measures: {direct_count}")
    print(f"   Indirect/coping measures: {indirect_count}")
    
    # 3. Confidence analysis
    print(f"\n3. CLASSIFICATION CONFIDENCE:")
    print(f"   Average confidence: {df['classification_confidence'].mean():.2f}")
    high_confidence = len(df[df["classification_confidence"] >= 0.5])
    print(f"   High-confidence classifications (≥0.5): {high_confidence}")
    
    # 4. Multi-trend reforms
    multi_trend = len(df[df["addresses_multiple_trends"]])
    print(f"\n4. MULTI-TREND REFORMS:")
    print(f"   Reforms addressing multiple megatrends: {multi_trend}")
    
    # 5. Top examples for each trend
    print(f"\n5. EXEMPLARY REFORMS BY TREND (Highest Confidence):")
    for trend in category_definitions.keys():
        trend_reforms = df[df["strategic_classification"] == trend]
        if len(trend_reforms) > 0:
            top_reform = trend_reforms.nlargest(1, "classification_confidence").iloc[0]
            print(f"\n   {trend} (Confidence: {top_reform['classification_confidence']:.2f}):")
            print(f"   '{top_reform['summary'][:150]}...'")
    
    print("\n" + "="*80)
    print("Analysis complete. Detailed results saved to Excel.")
    print("="*80)

# 7. Batch analysis with strategic scoring
def batch_strategic_analysis(df):
    """
    Process all reforms with strategic scoring
    """
    # Remove rows with empty/null summary
    df = df.dropna(subset=['summary'])
    df = df[df['summary'].str.strip() != '']
    df = df.reset_index(drop=True)

    results = []
    
    for idx, row in df.iterrows():
        reform_text = row["summary"]
        reform_id = row.get("reform_id", idx)
        
        # Get classification
        classification = classify_reform_strategically(reform_text)
        
        # Get multi-label classification
        multi_labels = classify_reform_multi_label(reform_text, threshold=0.25)
        
        # Calculate strategic score (weighted by confidence and link strength, with safe fallback)
        link_strength = classification.get("link_strength", 0.0) or 0.0
        strategic_score = classification["confidence"] * link_strength
        
        results.append({
            "reform_id": reform_id,
            "summary": reform_text[:200] + "..." if len(str(reform_text)) > 200 else reform_text,
            "primary_trend": classification["category"],
            "confidence": classification["confidence"],
            "link_type": classification["link_type"],
            "link_strength": link_strength,
            "strategic_score": round(strategic_score, 3),
            "all_trends": ", ".join([m["category"] for m in multi_labels]),
            "climate_relevance": classification["all_scores"].get("Climate Change", 0),
            "demographic_relevance": classification["all_scores"].get("Demographic Change", 0),
            "digital_relevance": classification["all_scores"].get("Digital Technology", 0),
            "work_relevance": classification["all_scores"].get("Shifting Nature of Work", 0),
            "public_debt_relevance": classification["all_scores"].get("Public Debt Expansion", 0),
            "global_order_relevance": classification["all_scores"].get("Changes in Global Order", 0),
            "regional_conflicts_relevance": classification["all_scores"].get("Regional Conflicts", 0),
            "is_anticipatory": "Yes" if classification["link_type"] == "Direct" else "No"
        })
    
    return pd.DataFrame(results)

# 8. Usage
if __name__ == "__main__":
    # Load your reforms data
    df = pd.read_excel("reforms.xlsx")
    
    # Option 1: Full strategic analysis
    analyzed_df = analyze_reforms_strategically("reforms.xlsx", "strategic_analysis.xlsx")
    
    # Option 2: Get detailed strategic scores
    strategic_scores = batch_strategic_analysis(df)
    strategic_scores.to_excel("reform_strategic_scores.xlsx", index=False)
    
    print("\n✅ Strategic classification complete!")
    print("   - Full analysis: strategic_analysis.xlsx")
    print("   - Strategic scores: reform_strategic_scores.xlsx")


def enhanced_analysis_with_area(df):
    """
    Enhanced analysis that includes area/region identification
    """
    # Add area identification (you'll need to have area/region data)
    # This assumes you have a 'country' column
    
    # Example mapping (you should replace with your actual data)
    country_to_region = {
        # Add your country-region mappings here
        # 'USA': 'North America',
        # 'Germany': 'Europe',
        # etc.
    }
    
    if 'country' in df.columns:
        df['region'] = df['country'].map(country_to_region)
    
    # Calculate area statistics
    if 'region' in df.columns:
        # Count reforms by region and link type
        region_stats = pd.crosstab(
            df['region'],
            df['link_type'],
            margins=True,
            margins_name='Total'
        )
        
        # Save region statistics
        region_stats.to_excel("region_analysis.xlsx")
    
    return df