# 🔍 Web Content Question Answering System

A Streamlit-based application that allows users to extract and analyze content from multiple web pages and ask questions about the aggregated information.

<!-- Insert your application screenshot here -->
<!--
![Web Content QA System](https://github.com/yourusername/web-content-qa/raw/main/screenshots/app-demo.png)
-->

## 🌟 Features

- **URL Content Extraction**: Fetch and parse content from multiple web pages simultaneously
- **Smart Text Processing**: Clean and normalize text content for better analysis
- **AI-Powered Question Answering**: Use OpenAI's GPT models to generate answers based on extracted content
- **Source Attribution**: All answers include references to their source URLs
- **Parallel Processing**: Process multiple URLs simultaneously for faster results
- **User-Friendly Interface**: Intuitive chat-like interface with clear visual feedback

## 📋 Requirements

- Python 3.7+
- Streamlit
- OpenAI API key
- Beautiful Soup 4
- Requests
- python-dotenv

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-content-qa.git
   cd web-content-qa
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 💻 Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Paste URLs containing content you want to analyze:
   ```
   https://example.com/article1
   https://example.com/article2
   ```

4. Ask questions about the extracted content:
   ```
   What are the main points discussed in these articles?
   ```

5. View answers with source citations indicating which URL provided the information

## 🔧 How It Works

1. **Content Extraction**: The `ContentFetcher` class extracts text from web pages using Beautiful Soup, removing unnecessary elements like scripts and navigation.

2. **Parallel Processing**: URLs are processed simultaneously using ThreadPoolExecutor for faster results.

3. **Context Management**: The `QuestionAnswerer` class maintains the extracted content as context for answering questions.

4. **Answer Generation**: When a question is asked, the system sends the extracted content and the question to OpenAI's API, instructing it to answer based only on the provided context.

5. **User Interface**: Streamlit provides a responsive and interactive interface with real-time updates.

## ⚙️ Configuration

You can modify the following constants in the `ContentFetcher` class:

- `MAX_WORDS`: Maximum number of words to extract from each URL (default: 2000)
- `MAX_URLS`: Maximum number of URLs to process in a single request (default: 5)

## 🛠️ Customization

### Adding a Requirements File

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.26.0
openai>=0.28.0
python-dotenv>=1.0.0
requests>=2.28.0
beautifulsoup4>=4.12.0
```

### Using a Different Language Model

To use a different model from OpenAI or another provider, modify the `answer_question` method in the `QuestionAnswerer` class:

```python
response = openai.ChatCompletion.create(
    model="gpt-4",  # Change to your preferred model
    messages=messages,
    temperature=0.7,
    max_tokens=800
)
```

### Adding Advanced Text Processing

You can enhance the text extraction by modifying the `clean_text` method in the `ContentFetcher` class:

```python
@staticmethod
def clean_text(text):
    # Add your custom text processing here
    return processed_text
```

## ⚠️ Limitations

- The system can only process a limited number of URLs at once (default: 5)
- Content extraction may not work perfectly on all websites, especially those with complex layouts
- The quality of answers depends on the quality of the extracted content
- Some websites may block automated access

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for their powerful language models
- [Streamlit](https://streamlit.io/) for the interactive web application framework
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

---

## 📝 Example Session

```
User: https://en.wikipedia.org/wiki/Artificial_intelligence https://en.wikipedia.org/wiki/Machine_learning

System: 📚 Content extracted from URLs:

Source: Artificial intelligence - Wikipedia
Preview: Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of human beings or animals. AI applications include advanced web search...

Source: Machine learning - Wikipedia
Preview: Machine learning (ML) is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and genera...

User: What is the relationship between AI and machine learning?

System: Based on the extracted content, machine learning is a subset of artificial intelligence. 

[Source 2] states that "Machine learning (ML) is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize from it."

[Source 1] mentions that machine learning is one of the approaches to AI, along with others like knowledge-based systems, and explains that it involves using data to teach computers how to perform tasks rather than programming them with specific rules.

In essence, machine learning is a technique or methodology within the broader field of artificial intelligence that focuses on creating systems that can learn from and make decisions based on data.