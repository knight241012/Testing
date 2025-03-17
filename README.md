# 🔍 Web Content Question Answering System

An interactive web application that extracts content from URLs and answers questions about them using AI.

![Web Content QA System Demo](https://user-images.githubusercontent.com/your-username/your-repo/assets/demo.gif)

## ✨ Features

- **URL Content Extraction**: Extract and analyze content from any website
- **AI-Powered Question Answering**: Ask questions about the extracted content
- **Source Citations**: Get answers with references to the source material
- **Special Wikipedia Handling**: Optimized extraction for Wikipedia articles
- **Interactive UI**: Clean, user-friendly interface built with Streamlit

## 🚀 Live Demo

Try the live demo at: [https://web-content-qa.streamlit.app/](https://web-content-qa.streamlit.app/)

## 📋 How It Works

1. **Paste URLs**: Enter one or more website URLs to analyze
2. **Process Content**: The system extracts and processes the content
3. **Ask Questions**: Ask questions in natural language about the content
4. **Get Answers**: Receive AI-generated answers with source citations

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- OpenAI API key

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/web-content-qa.git
cd web-content-qa
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**

Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

4. **Run the application**

```bash
streamlit run app.py
```

## 📝 Usage Examples

### Analyzing a Wikipedia Article

1. Paste the URL: `https://en.wikipedia.org/wiki/Artificial_intelligence`
2. Ask: "What are the main applications of AI?"
3. The system will extract content and answer with cited sources

### Comparing Multiple Sources

1. Paste multiple URLs related to the same topic
2. Ask: "What are the different perspectives on this topic?"
3. Get a comprehensive answer with sources cited

### Technical Research

1. Paste URLs from technical documentation or research papers
2. Ask specific technical questions
3. Receive detailed, accurate answers with citations

## 🧩 How to Deploy

### Streamlit Cloud (Recommended)

1. Push this code to a GitHub repository
2. Add a `requirements.txt` file
3. Sign up at [share.streamlit.io](https://share.streamlit.io/)
4. Deploy your app and add your OpenAI API key as a secret

## 🔧 Configuration

You can modify the following settings in the `ContentFetcher` class:

- `MAX_WORDS`: Maximum number of words to extract per URL (default: 2000)
- `MAX_URLS`: Maximum number of URLs to process (default: 5)

## 📊 System Architecture

The application consists of three main components:

1. **ContentFetcher**: Extracts and cleans content from URLs
2. **QuestionAnswerer**: Uses OpenAI to generate answers based on the content
3. **Streamlit UI**: Provides the interactive web interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the web app framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

## 📬 Contact

- **Email**: thakuraarush2786@gmail.com

---

Made by Aarush
