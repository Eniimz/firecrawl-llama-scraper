from groq import Groq
from firecrawl import FirecrawlApp
import ollama
import json

api_key = "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"

# Function to process a chunk using an LLM
client = Groq(api_key=api_key)

app = FirecrawlApp(api_key="fc-6d74df6872c0461ebef360fce2f44ca0")


def split_markdown_into_chunks(markdown_content, max_lines_per_chunk=30):
    """
    Split the Markdown content into smaller chunks.
    Each chunk contains a maximum of `max_lines_per_chunk` lines.
    """

    markdown_content = markdown_content.replace('\\n', '\n')
    # Split the content into lines
    lines = markdown_content.split('\n')
    
    # Create chunks of `max_lines_per_chunk` lines each
    chunks = [
        '\n'.join(lines[i:i + max_lines_per_chunk])
        for i in range(0, len(lines), max_lines_per_chunk)
    ]
    
    return chunks

fields = ["title", "rating", "price", "description", "imageUrl", "link" ]



def process_chunk_with_llm(chunk):
    """
    Process a chunk of Markdown content using an LLM.
    """

    msgs = [
    {
        "role": "system",
        "content": f"""You are an intelligent text extraction and conversion assistant 
        Your task is to extract structured information from the given text and convert it into a pure JSON format. The JSON 
        should contain only the structured data extracted from the text,with no additional commentary, explanations, or 
        extraneous information.You could encounter cases where you can't find the data of the fields you have to extract or 
        the data will be in a foreign language.Please process the following text and provide the output in pure JSON format 
        with no words before or after the JSON: "" 
        
        Example:
                 "title": "Apple iPhone 16 Pro Max Clear Case with MagSafe and Camera Control",
                 "rating": "4.3",
                 "price": 699$,
                 "description": "Pro camera system with 12MP Ultra Wide, Wide and Telephoto cameras; 5x optical zoom range; Night mode, Deep Fusion, Smart HDR 3, Apple ProRAW, 4K Dolby Vision HDR recording ",
                 "imageUrl": "https://m.media-amazon.com/images/I/71MHTD3uL4L._AC_UY436_QL65_.jpg",
                 "link": "https://www.amazon.com/Apple-iPhone-Pacific-Carrier-Subscription/dp/B08L5PHJ2Y/ref=sr_1_1?crid=2NCP8DI16UYB2&dib=eyJ2IjoiMSJ9.aF_aTdaW_XC38oL_Kdy1_t3AkcjdLoopAJXoZRk9MFLq1FNDBoVrmFsVbRefXYf1qeev9tHYhhFxzKNWf5gL4kzd3fHIJoCnu9oDbb5jdTy9QNQnujfr1ArsO3dMhzYx4kSz21yl2mJNiPieOdqMQ4y07Oeo_oAPE9gzRy_HV2kLAxvLr8Mu0xM8f93nKZG-wZX3qJiWPxU3WHcoU5PNq1urmr9D1O_ZO3ulWe551U8.PAMKJ8He7PYBYa2WPwPKnofy6eFleGgHFNiXotPruP8&dib_tag=se&keywords=iphone&qid=1738372776&sprefix=ipho%2Caps%2C305&sr=8-1"
        
        """
    },
    {
        
        "role": "user",
        "content": f"Extract the following information from the provided text:\n\nPage Content:\n\n{chunk}\n\nInformation to extract: {fields}"
            
    }
    ]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages= msgs,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    print(completion.choices[0].message.content)
    with open(f"chunks/chunk_{i + 1}.json", 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(completion.choices[0].message.content)



# Example usage
if __name__ == "__main__":
    # Path to your Markdown file
    print("Starting scraping the url...")
# Scrape a website:
    scrape_result = app.scrape_url('https://amazon.com/s?k=iphone', params={'formats': ['markdown']})


    print("Url has been scraped...?")

    # Read the Markdown content
    # with open(markdown_file_path, 'r', encoding='utf-8') as file:
    #     markdown_content = file.read()

    if 'markdown' in scrape_result:
        markdown_content = scrape_result['markdown']
    else:
        raise ValueError("No Markdown content found in the scrape result.")

    # Split the Markdown content into chunks
    chunks = split_markdown_into_chunks(markdown_content, max_lines_per_chunk=50)

    # Process each chunk with the LLM
    for i in range(4):
        if i < len(chunks):
            chunk = chunks[i]
            print(f"Processing Chunk {i + 1}...")

            result = process_chunk_with_llm(chunk)
        else:
             break