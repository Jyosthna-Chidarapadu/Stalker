# Stalker
## 📷 Instagram Profile Sentiment Analyzer

A Streamlit-based web application that performs sentiment analysis on Instagram profile captions and comments using the **VADER Sentiment Analyzer**. Supports both **public and private profiles** by logging in through `instaloader`.

## 🧠 Features

- 🔓 Analyze **Public & Private** Instagram profiles  
- 📈 Perform sentiment analysis using **VADER**  
- 🖼️ View profile picture, full name, and recent post details  
- 📊 Get visual breakdown of **Positive**, **Neutral**, **Negative**, and **Overall** sentiment  
- 📆 Display post-wise likes, dates, and image previews  

## 🛠️ Technologies Used

- Streamlit
- Instaloader
- VADER Sentiment Analyzer
- NumPy
- Pillow
- Requests

## ⚙️ Setup Instructions

```bash
git clone https://github.com/yourusername/instagram-sentiment-analyzer.git
cd instagram-sentiment-analyzer
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Login Requirement

To access **private profiles**, you must provide valid Instagram credentials.

## 📁 Folder Structure

```
instagram-sentiment-analyzer/
├── app.py
├── requirements.txt
└── README.md
```

## ✅ Future Improvements

- Add keyword cloud from captions/comments  
- Store past analysis results  
- Login via OAuth instead of plain text  
- Export sentiment report as PDF


