__fname = 'sort_books'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
import os
import shutil
from openai import OpenAI
from _env import env

 # replace with your openAI account API key
OPENAI_API_KEY = env.OPENAI_KEY

# Function to retrieve file and folder names from a directory
def get_titles_from_folder(directory):
    print(f'\n1) getting books from {directory} folder ...')
    # Initialize an empty list to store titles
    titles = []
    
    # Traverse the directory
    for item in os.listdir(directory):
        # Check if the item is a file or a folder
        title_path = directory+'/'+item
        print(f' found title_path: {title_path}')
        titles.append(title_path)
        # if os.path.isfile(os.path.join(directory, item)):
        #     # Add file name to titles list
        #     titles.append(os.path.splitext(item)[0])  # Ignore file extension
        # elif os.path.isdir(os.path.join(directory, item)):
        #     # Add folder name to titles list
        #     titles.append(item)
    
    return titles

# Function to call OpenAI API and process book titles
def process_titles(book_titles):
    print('\n2) getting genre analysis from openAI ... ')
    # Initialize OpenAI API key
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Define the instruction to be sent to ChatGPT
    instruction = """
    Hey ChatGPT!

    I need your help with mapping book titles to genres.
    I will be providing a list of book titles.
    They titles are in file path format.
    This means they do indeed contain file extensions.
    Please process the list of file path titles provided below and suggest a genre for each title. 
    NOTE: these titles are actually file names with paths and extensions. These paths and extsension are VERY important to my integrationn. Please DO NOT alter these paths.
    You can expect to receive 500 to 1000 titles at a time for efficient processing.

    Once you're done, please output a JSON text format containing the mapping of titles (WITH their file extensions) to genres.

    Example JSON Output Format:
    "{
      "filepath w/ (dot)ext": "Fantasy",
      "filepath w/ (dot)ext": "Mystery",
      "filepath w/ (dot)ext": "Science Fiction",
    }"

    Here is your Input:
    %s

    Thanks for your assistance! 📚
    """ % (book_titles)

    # Call the OpenAI API
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=instruction,
    #     max_tokens=500
    # )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": instruction},
        ],
        max_tokens=4000,  # Adjust the token limit as necessary.
        temperature=0.7,
        presence_penalty=0.6,
        # stop=["}"]  # Adjusted stop sequences to ensure proper response termination.
    )

    # Parse the response and return the mapping of titles to genres
    resp_json = response.choices[0].message.content.strip() if response.choices else "Hmm, it seems I need a moment to ponder this."
    print(' openAI output json: \n' + resp_json + '\n')
    return resp_json

# Function to copy titles to genre-specific directories
def copy_titles_to_genre_directories(titles_to_genres):
    print('\n3) copying e-book files to openAI selected genre folder ...')
    # Create the "output" directory if it doesn't exist
    output_directory = "output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate over the titles and their corresponding genres
    for title, genre in titles_to_genres.items():
        print(f' working ... {title} : {genre}')
        # Create the genre directory if it doesn't exist
        genre_directory = os.path.join(output_directory, genre)
        if not os.path.exists(genre_directory):
            os.makedirs(genre_directory)
        
        # Copy the title (file or folder) to the genre directory
        shutil.copy(title, genre_directory)

if __name__ == "__main__":
    # Example starting directory path
    starting_directory = "./books"
    
    # Get the list of file and folder names from the starting directory
    book_titles = get_titles_from_folder(starting_directory)
    
    # Call the function to process the titles
    output = process_titles(book_titles)

    # Convert the output to a dictionary
    titles_to_genres = eval(output)
    
    # Call the function to copy titles to genre-specific directories
    copy_titles_to_genre_directories(titles_to_genres)
    
    print("\nDONE!\nYour welcome")
