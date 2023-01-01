
from textblob import TextBlob

if __name__ == '__main__':

    error_file = open("realword_error.txt", "r+")
    corrected_file = open("realword_BaseCorrection.txt", "w+")

    for line in error_file:
        corrected_lines = TextBlob(line).correct().raw_sentences
        corrected_file.write(" ".join(corrected_lines)) 
        corrected_file.write("\n") 
      
    error_file.close()
    corrected_file.close() 
