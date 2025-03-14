# BibTeX Key Generator 

A simple Python utility that generates BibTeX citation keys using the same rules as Emacs’s `[bibtex-mode](https://github.com/emacs-mirror/emacs/blob/master/lisp/textmodes/bibtex.el))`.

## Features 

-   Generates BibTeX keys from author, year, and title information
-   Handles special cases like diacritics, author name formats, and ignored words
-   Customized to match specific BibTeX key preferences

## Installation 

No external dependencies required - the script only uses Python\'s standard library.

Simply download `bibkey_generator.py` to your project directory.

## Usage 


### As a Python module 

``` {.src .src-python}
from bibkey_generator import bibkey_generator

# Basic usage with author, year, and title
key = bibkey_generator("John Smith", "2023", "The Great Analysis of Something Important")
print(key)  # Output: Smith2023GreatAnalysisSomething
```

### With multiple authors (only uses first author by default) 

``` {.src .src-python}
key = bibkey_generator("John Smith and Jane Doe", "2023", "The Great Analysis")
print(key)  # Output: Smith2023GreatAnalysis
```

### With different author format 

``` {.src .src-python}
key = bibkey_generator("Smith, John", "2023", "The Great Analysis")
print(key)  # Output: Smith2023GreatAnalysis
```

### Missing arguments are handled gracefully 

``` {.src .src-python}
key = bibkey_generator("Einstein, Albert", "1905")  # No title
print(key)  # Output: Einstein1905
```

### From the command line 

``` {.src .src-bash}
python bibkey_generator.py "John Smith" "2023" "The Great Analysis of Something Important"
# Output: Smith2023GreatAnalysisOf
```

## Configuration 

The generator is configured to use these specific settings:

-   Uses the first author\'s last name (`autokey_names = 1`)
-   Capitalizes author names (`autokey_name_case_convert_function = 'capitalize'`)
-   Uses full 4-digit year (`autokey_year_length = 4`)
-   No separator between year and title (`autokey_year_title_separator = ''`)
-   Terminates title at first punctuation (`autokey_title_terminators = "[.!?;]|--"`)
-   Uses up to 3 significant words from title (`autokey_titlewords = 3`)
-   Capitalizes title words (`autokey_titleword_case_convert_function = 'capitalize'`)
-   No separator between title words (`autokey_titleword_separator = ''`)
-   Ignores common articles and prepositions in multiple languages
