import sys
import re
import unicodedata

def bibkey_generator(author="", year="", title=""):
    """
    Generate a BibTeX key from author, year and title.
    
    Args:
        author (str): Author names, separated by 'and'
        year (str): Publication year
        title (str): Publication title
        
    Returns:
        str: Generated BibTeX key
    """
    # Configuration settings matching your Emacs Lisp customization
    config = {
        'autokey_names': 1,
        'autokey_name_case_convert_function': 'capitalize',
        'autokey_year_length': 4,
        'autokey_year_title_separator': '',
        'autokey_title_terminators': r'[.!?;]|--',
        'autokey_titlewords': 3,
        'autokey_titlewords_stretch': 0,
        'autokey_titleword_case_convert_function': 'capitalize',
        'autokey_titleword_length': None,  # None means no limit
        'autokey_titleword_separator': '',
        'autokey_titleword_ignore': [
            "A", "a", "An", "an", "On", "on", "The", "the", "Eine?", "Der", "Die", "Das", 
            "El", "La", "Lo", "Los", "Las", "Un", "Una", "Unos", "Unas", "el", "la", "lo", 
            "los", "las", "un", "una", "unos", "unas", "y", "o", "Le", "La", "L'", "Les", 
            "Un", "Une", "Des", "Du", "De la", "De l'", "Des", "le", "la", "l'", "les", 
            "un", "une", "des", "du", "de la", "de l'", "des", "Lo", "Il", "La", "L'", 
            "Gli", "I", "Le", "Uno", "lo", "il", "la", "l'", "gli", "i", "le", "uno"
        ]
    }
    
    # Helper functions
    def apply_case_conversion(text, method):
        """Apply case conversion based on method name."""
        if method == "capitalize":
            return text.capitalize()
        elif method == "downcase":
            return text.lower()
        elif method == "upcase":
            return text.upper()
        return text
    
    def remove_diacritics(text):
        """Remove diacritics from text."""
        return ''.join(c for c in unicodedata.normalize('NFD', text)
                        if unicodedata.category(c) != 'Mn')
    
    def clean_for_key(text):
        """Clean text for use in BibTeX key."""
        text = remove_diacritics(text)
        text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    # Process author names
    author_part = ""
    if author:
        authors = re.split(r'\s+and\s+', author, flags=re.IGNORECASE)
        last_names = []
        
        for author_name in authors:
            if ',' in author_name:  # "Lastname, Firstname" format
                last_name = author_name.split(',')[0].strip()
            else:  # "Firstname Lastname" format
                name_parts = author_name.strip().split()
                if name_parts:
                    last_name = name_parts[-1]
                else:
                    continue
            
            last_name = clean_for_key(last_name)
            if last_name:
                method = config['autokey_name_case_convert_function']
                last_name = apply_case_conversion(last_name, method)
                last_names.append(last_name)
                
                if len(last_names) >= config['autokey_names']:
                    break
        
        author_part = ''.join(last_names)
    
    # Process year
    year_part = ""
    if year:
        match = re.search(r'\d+', year)
        if match:
            year_digits = match.group(0)
            if config['autokey_year_length'] > 0:
                year_digits = year_digits[-config['autokey_year_length']:]
            year_part = year_digits
    
    # Process title
    title_part = ""
    if title:
        cleaned_title = clean_for_key(title)
        
        # Split by terminators if defined
        first_part = cleaned_title
        if config['autokey_title_terminators']:
            match = re.search(config['autokey_title_terminators'], cleaned_title)
            if match:
                first_part = cleaned_title[:match.start()].strip()
        
        words = first_part.split()
        title_words = []
        
        for word in words:
            if word not in config['autokey_titleword_ignore']:
                method = config['autokey_titleword_case_convert_function']
                word = apply_case_conversion(word, method)
                
                if config['autokey_titleword_length'] is not None:
                    word = word[:config['autokey_titleword_length']]
                
                title_words.append(word)
                
                word_count = config['autokey_titlewords'] + config['autokey_titlewords_stretch']
                if len(title_words) >= word_count:
                    title_words = title_words[:word_count]
                    break
        
        title_words = title_words[:max(len(title_words), config['autokey_titlewords'])]
        title_part = config['autokey_titleword_separator'].join(title_words)
    
    # Build the final key
    key_parts = []
    
    # Add author part
    if author_part:
        key_parts.append(author_part)
    
    # Add year part with separator if needed
    if year_part:
        if key_parts:  # If we have author part
            key_parts.append(config['autokey_year_title_separator'])
        key_parts.append(year_part)
    
    # Add title part
    if title_part:
        key_parts.append(title_part)
    
    # Join everything into a key
    return ''.join(key_parts)

# Command-line interface
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        author = sys.argv[1]
        year = sys.argv[2] if len(sys.argv) > 2 else ""
        title = sys.argv[3] if len(sys.argv) > 3 else ""
        key = bibkey_generator(author, year, title)
        print(key)
    else:
        # Run examples if no arguments provided
        print("Usage: python bibkey_generator.py 'Author Name' 'Year' 'Title'")
        print("\nExample results:")
        key = bibkey_generator("John Smith and Jane Doe", "2023", "The Great Analysis of Something Important: A Case Study")
        print(f"Generated BibTeX key: {key}")
