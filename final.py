import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os
import openai  # Import the older version of openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')  # Set API key in the older style

class ContentFetcher:
    MAX_WORDS = 2000
    MAX_URLS = 5
    
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def clean_text(text):
        """Clean and normalize text content."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text

    @staticmethod
    def extract_text_from_url(url):
        """Extract and clean text content from a URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unwanted elements
            for tag in ['script', 'style', 'nav', 'footer', 'header', 'aside']:
                for element in soup.find_all(tag):
                    element.decompose()
                    
            # Special handling for Wikipedia
            if 'wikipedia.org' in url:
                # For Wikipedia pages, focus on the main content
                main_content = soup.find(id="mw-content-text")
                if main_content:
                    # Remove reference sections and tables that might contain irrelevant data
                    for ref in main_content.find_all('sup', class_='reference'):
                        ref.decompose()
                    for table in main_content.find_all('table'):
                        table.decompose()
                    
                    # Get text from main content paragraphs and headings
                    content_tags = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol'])
                else:
                    content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article'])
            else:
                # Get text from paragraphs and headings for non-Wikipedia sites
                content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article'])

            # Get text from paragraphs and headings
            text_content = ' '.join(tag.get_text(strip=True) for tag in content_tags)
            
            # Clean and normalize text
            cleaned_text = ContentFetcher.clean_text(text_content)
            
            # Truncate if too long
            words = cleaned_text.split()
            if len(words) > ContentFetcher.MAX_WORDS:
                cleaned_text = ' '.join(words[:ContentFetcher.MAX_WORDS])
            
            return {
                'url': url,
                'content': cleaned_text,
                'title': soup.title.string if soup.title else url
            }
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None

class QuestionAnswerer:
    def __init__(self):
        self.context = []
        self.current_urls = set()

    def search_and_extract(self, query):
        """Find relevant URLs for the query and extract their content."""
        # Extract URLs from the query
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', query)
        
        if not urls:
            return "Please provide URLs to search through for answering questions."

        # Limit number of URLs
        urls = urls[:ContentFetcher.MAX_URLS]
        
        # Create a progress bar
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        progress_text.text(f"Processing {len(urls)} URLs...")
        
        # Process URLs in parallel
        results = []
        valid_urls = [url for url in urls if ContentFetcher.is_valid_url(url)]
        total_urls = len(valid_urls)
        
        if total_urls == 0:
            progress_text.empty()
            progress_bar.empty()
            return "No valid URLs found. Please provide valid URLs that include both scheme (http/https) and domain."
        
        completed = 0
        
        # Process each URL sequentially for better error handling
        for url in valid_urls:
            result = ContentFetcher.extract_text_from_url(url)
            completed += 1
            progress_bar.progress(completed / total_urls)
            progress_text.text(f"Processed {completed}/{total_urls} URLs...")
            
            if result:
                results.append(result)
                self.current_urls.add(result['url'])

        # Clean up progress indicators
        progress_text.empty()
        progress_bar.empty()
        
        if not results:
            return "Could not extract content from any of the provided URLs. Please check that the URLs are accessible."

        # Update context with new content
        self.context = results
        return self.format_content_summary(results)

    def format_content_summary(self, results):
        """Format a summary of the extracted content."""
        summary = "📚 Content extracted from URLs:\n\n"
        for i, result in enumerate(results, 1):
            title = result.get('title', result['url'])
            content_preview = result['content'][:200] + "..."
            summary += f"Source {i}: {title}\nPreview: {content_preview}\n\n"
        return summary

    def answer_question(self, question):
        """Answer a question using the extracted content."""
        if not self.context:
            return "Please provide URLs first so I can search for answers to your questions."
            
        if question.lower() == "what is this url about" or "what is url about" in question.lower():
            # Special handling for URL summary requests
            summary = "Here's what I found about these URLs:\n\n"
            for i, result in enumerate(self.context, 1):
                title = result.get('title', 'Untitled')
                url = result.get('url', 'Unknown URL')
                
                summary += f"**Source {i}: {title}**\n"
                summary += f"URL: {url}\n"
                    
                # Add a brief content summary
                if result['content']:
                    content_preview = " ".join(result['content'].split()[:50])
                    summary += f"Content begins with: {content_preview}...\n\n"
            
            return summary

        # Prepare content for the model
        combined_content = "\n\n".join(
            f"Source {i+1} ({result['url']}):\n{result['content'][:1000]}"
            for i, result in enumerate(self.context)
        )

        try:
            with st.spinner("Generating answer..."):
                # Create a prompt for the model
                messages = [
                    {
                        "role": "system",
                        "content": ("You are a helpful assistant that answers questions based on provided content. "
                                  "Always cite your sources using [Source X] notation when providing information. "
                                  "If the answer cannot be found in the sources, say so clearly.")
                    },
                    {
                        "role": "user",
                        "content": f"Here is the content to search through:\n\n{combined_content}\n\nQuestion: {question}\n\n"
                                  "Please answer the question using only the information provided above. "
                                  "Cite sources as [Source X] where X is the source number."
                    }
                ]

                # Use the older OpenAI API format
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800
                )

                return response.choices[0].message['content']

        except Exception as e:
            return f"Error generating answer: {str(e)}"

def process_input(user_input):
    # Check if input contains URLs
    if 'http' in user_input.lower():
        with st.spinner("🔍 Crawling websites and extracting content..."):
            response = st.session_state.qa_system.search_and_extract(user_input)
        st.session_state.initialized = True
    else:
        # Handle questions
        if not st.session_state.initialized:
            response = "⚠️ Please provide some URLs first so I can search for answers to your questions."
        else:
            response = st.session_state.qa_system.answer_question(user_input)
    
    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

def display_chat_history():
    # Create chat container with custom styling
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You**: {message['content']}")
                st.write("---")
            else:
                st.markdown(f"**Assistant**: {message['content']}")
                st.write("---")
    
    # Add a visual indicator that the system is ready for questions after URLs are processed
    if st.session_state.initialized and len(st.session_state.chat_history) > 0:
        st.success("✅ Content processed! You can now ask questions about the extracted content.")

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Web Content QA System",
        page_icon="🔍",
        layout="wide"
    )
    
    # Title and description
    st.title("🔍 Web Content Question Answering System")
    st.markdown("""
    1. Paste URLs containing content you want to analyze
    2. Ask questions about the content
    3. Get answers with source citations
    
    Example: Paste some URLs, then ask "What are the main topics discussed?"
    """)
    
    # Initialize session state for chat history and QA system
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = QuestionAnswerer()
        st.session_state.initialized = False
    
    # Initialize input state properly
    if 'input_value' not in st.session_state:
        st.session_state.input_value = ""
    
    # Callback functions for the submit button
    def submit_clicked():
        if st.session_state.input_value:
            process_input(st.session_state.input_value)
            # Clear the input value for next use
            st.session_state.input_value = ""
    
    # Callback for reset button
    def reset_system():
        st.session_state.qa_system = QuestionAnswerer()
        st.session_state.initialized = False
        st.session_state.chat_history = []
        st.session_state.input_value = ""
        st.success("System reset. Please provide new URLs to analyze.")
    
    # Display chat history first so it stays at the top
    display_chat_history()
    
    # Status indicator
    status_container = st.container()
    if st.session_state.initialized:
        with status_container:
            st.info("System is ready for questions. You can paste more URLs or ask questions about the content.")
    else:
        with status_container:
            st.warning("Please paste URLs to begin analyzing content.")
    
    # Define columns for chat interface
    col1, col2 = st.columns([4, 1])
    
    # Input area - use session state to manage the value
    with col1:
        st.text_area(
            "URLs or Questions",
            placeholder="Paste URLs or ask questions about the content...",
            height=100,
            key="input_value"  # This links the widget to session state
        )
    
    # Buttons with callbacks
    with col2:
        st.button("Send 🚀", on_click=submit_clicked, use_container_width=True)
        st.button("Reset System 🔄", on_click=reset_system, use_container_width=True)

if __name__ == "__main__":
    main()