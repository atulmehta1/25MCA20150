import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Curated financial training corpus with sentiment labels
# 1 = Bullish / Positive, 0 = Bearish / Negative, 2 = Neutral
FINANCIAL_CORPUS = [
    ("Company reports record fourth quarter revenue beating analyst estimates", 1),
    ("Earnings per share surged 45% year over year driven by cloud demand", 1),
    ("Board approves $10 billion share buyback program and raises quarterly dividend", 1),
    ("Secures massive multi-year artificial intelligence infrastructure contract", 1),
    ("FDA approves breakthrough medical device; shares jump 12%", 1),
    ("Operating profit margins expanded by 320 basis points as efficiencies kick in", 1),
    ("Upgrades stock rating to Strong Buy with significantly raised price target", 1),
    ("Strong cash flow generation enables aggressive capital reinvestment", 1),
    ("Strategic partnership expected to accelerate top-line expansion in global markets", 1),
    ("Gross margins improved dramatically due to declining input and supply costs", 1),
    ("Quarterly revenue beats forecasts by wide margin on explosive retail growth", 1),
    ("Subscription recurring revenue grew 60% with customer churn at record lows", 1),
    
    ("Company slashes full year sales guidance citing weakening consumer demand", 0),
    ("Net loss widens significantly as production bottlenecks and inflation persist", 0),
    ("SEC launches formal regulatory investigation into corporate accounting practices", 0),
    ("Downgraded to Sell due to decelerating growth and severe margin compression", 0),
    ("CEO abruptly resigns amid board dispute and declining operational performance", 0),
    ("Cuts 15% of global workforce to conserve liquidity and reduce cash burn", 0),
    ("Major client terminates contract; future revenue outlook materially impaired", 0),
    ("Free cash flow turns negative as debt servicing obligations soar", 0),
    ("Supply chain shortages and logistics disruptions cause widespread factory shutdowns", 0),
    ("Product recall and warranty liabilities trigger substantial litigation reserves", 0),
    ("Misses consensus revenue expectations by wide margin, shares plummet", 0),
    ("Heavy competition forces steep price discounts eroding operating profits", 0),
    
    ("Company will host its annual shareholder meeting and webcast next Tuesday", 2),
    ("Management announces scheduled transition of Chief Technology Officer next quarter", 2),
    ("Federal Reserve holds interest rates steady following two-day policy summit", 2),
    ("Quarterly filings submitted on schedule in accordance with regulatory filing guidelines", 2),
    ("Board appoints new independent director with extensive audit committee background", 2),
    ("Treasury yields trade in narrow band ahead of upcoming inflation report release", 2),
    ("Company expands retail distribution to five additional regional metropolitan markets", 2),
    ("Trading volume remained moderate across major domestic exchange indexes today", 2)
]

SAMPLE_MARKET_HEADLINES = [
    {"symbol": "AAPL", "headline": "Apple reports record iPhone and Services revenue beating Wall Street targets", "source": "Reuters", "time": "1 hour ago"},
    {"symbol": "MSFT", "headline": "Microsoft Cloud Azure revenue accelerates 33% powered by enterprise AI adoption", "source": "Bloomberg", "time": "3 hours ago"},
    {"symbol": "TSLA", "headline": "Tesla expands full self-driving rollouts while navigating global EV pricing pressures", "source": "CNBC", "time": "4 hours ago"},
    {"symbol": "NVDA", "headline": "Nvidia announces next-generation Blackwell AI chip architecture with unprecedented computing power", "source": "Wall Street Journal", "time": "6 hours ago"},
    {"symbol": "AMZN", "headline": "Amazon AWS margins rebound strongly following disciplined cost optimization measures", "source": "Financial Times", "time": "8 hours ago"},
    {"symbol": "GOOGL", "headline": "Google unveils enhanced Gemini enterprise reasoning models integrated with Google Workspace", "source": "TechCrunch", "time": "12 hours ago"}
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class SentimentEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', min_df=1)
        self.texts = [item[0] for item in FINANCIAL_CORPUS]
        self.labels = [item[1] for item in FINANCIAL_CORPUS]
        
        # Train both models
        self.nb_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('clf', MultinomialNB(alpha=0.5))
        ])
        self.nb_pipeline.fit(self.texts, self.labels)
        
        self.lr_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('clf', LogisticRegression(C=2.0, max_iter=300))
        ])
        self.lr_pipeline.fit(self.texts, self.labels)
        
    def analyze_text(self, text, model_choice='logistic_regression'):
        if not text or not text.strip():
            return {'label': 'Neutral', 'sentiment': 'Neutral', 'score': 0.0, 'confidence': 50.0}
            
        clean = clean_text(text)
        pipeline = self.lr_pipeline if model_choice == 'logistic_regression' else self.nb_pipeline
        
        pred = pipeline.predict([clean])[0]
        probs = pipeline.predict_proba([clean])[0]
        
        classes = pipeline.classes_
        prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}
        
        p_bear = prob_dict.get(0, 0.0)
        p_bull = prob_dict.get(1, 0.0)
        p_neut = prob_dict.get(2, 0.0)
        
        # Calculate sentiment polarity score (-1.0 to +1.0)
        polarity_score = float(p_bull - p_bear)
        
        if pred == 1:
            label = 'Bullish'
            confidence = round(p_bull * 100, 1)
        elif pred == 0:
            label = 'Bearish'
            confidence = round(p_bear * 100, 1)
        else:
            label = 'Neutral'
            confidence = round(p_neut * 100, 1)
            
        # Extract prominent keywords from headline
        tfidf = pipeline.named_steps['tfidf']
        feature_names = np.array(tfidf.get_feature_names_out())
        vec = tfidf.transform([clean])
        nz_indices = vec.nonzero()[1]
        word_scores = [(feature_names[i], round(float(vec[0, i]), 3)) for i in nz_indices]
        word_scores = sorted(word_scores, key=lambda x: -x[1])[:6]
        
        return {
            'text': text,
            'model_used': 'Logistic Regression' if model_choice == 'logistic_regression' else 'Multinomial Naive Bayes',
            'sentiment': label,
            'confidence': confidence,
            'polarity_score': round(polarity_score, 3),
            'probabilities': {
                'bullish': round(p_bull * 100, 1),
                'bearish': round(p_bear * 100, 1),
                'neutral': round(p_neut * 100, 1)
            },
            'top_keywords': word_scores
        }

    def get_sample_sentiment(self):
        analyzed = []
        for item in SAMPLE_MARKET_HEADLINES:
            res = self.analyze_text(item['headline'], model_choice='logistic_regression')
            analyzed.append({
                'symbol': item['symbol'],
                'headline': item['headline'],
                'source': item['source'],
                'time': item['time'],
                'sentiment': res['sentiment'],
                'confidence': res['confidence'],
                'score': res['polarity_score']
            })
        return analyzed

# Global singleton
nlp_engine = SentimentEngine()
