import time
import enchant
import matplotlib.pyplot as plt
from copy import deepcopy
from memory_profiler import profile
import requests



class Spell_Checker:
    """ Spell_Checker class for:

    - Loading dictionary of words
    - Storing this dictionary in a suitable data structure
    - Taking an input word and return the nearest 4 words if this word is not in the dictionary
    - Taking an input word and add this word to the dictionary
    - Removing an input word from the dictionary
    - specify the time and space complexity for each operation



    Attributes:
        dictionary_fname (str) the name of the dictionary file
        password (str) the admin. password for adding and removing form dictionary

    """
    def __init__(self, dictionary_fname = "dictionary.txt"):
        self.dictionary = dictionary_fname
        self.password = "authenticated_1"
        # self.punctuation = ["!", "?", "@", "#", "$", "%", "^", "&", "*", "/", "(", ")", "_", "-"]




    #@profile(precision = 4)
    def read_text_dictionary(self):
        """Function to read the dictionary file and stores it in a list.
        Args:
            None
        Returns:
            a_to_z (list): contains the dictionary keys form [a-Z]
            unique_dictionary (list): contains all the words form [a-z]
        """
        with open(self.dictionary) as f:
            dictionary = f.read().split('\n')[:-1]
        unique_dictionary = list(sorted(set(dictionary)))

        a_to_z = [letter for letter in unique_dictionary if len(letter) == 1]
        return a_to_z, unique_dictionary




    #@profile(precision = 4)
    def words_per_letter(self, letter_to_words):
        """counts the total words in the dictionary, also the number of words
           for each letter.
        Args:
            None
        Returns:
            dict_of_words_num (dict): number of words corresponding to each starting letter
            words_count (int): total number of words
        """
        words_count = 0
        dict_of_words_num = {}

        for k in letter_to_words:
            # print(letter_to_words[k][:2])
            dict_of_words_num[k] = len(letter_to_words[k])
            words_count += len(letter_to_words[k])

        print(f"words_per_letter: {dict_of_words_num}")
        print(f"total_words_count: {words_count}")
        return dict_of_words_num, words_count




    #@profile(precision = 4)
    def plotting_letters_num(self, letter_to_words):
        """plot each letter and the number of letters corresponding to it in bars.
        Args:
            letter_to_words (dict): number of words corresponding to each starting letter
        Returns:
            None
        """
        letters = list(letter_to_words.keys())
        num_of_words = list(letter_to_words.values())

        plt.bar(range(len(letter_to_words)), num_of_words, tick_label = letters)
        plt.show()




    #@profile(precision = 4)
    def create_dictionary_of_words(self, print_status = False, plot = False):
        """create the dictionary where each key is letter from [a-z] and the value
           for each of them is a list of all the words starts with this letter.
        Optional Args:
            print_status (bool): prints the number of words corresponding to each starting letter
                                 (default = False)
            plot (bool): works only when print_status is set to (True)
                         plot each letter and the number of letters corresponding to it in bars.
                         (default = False)
        Returns:
            None
        """
        a_to_z, dictionary = self.read_text_dictionary()
        sorted_lst_of_words = sorted(dictionary)
        letter_to_words = {}
        for letter in a_to_z:
            container = []
            for word in dictionary:
                if word.startswith(letter) and word != letter:
                    container.append(word)
            # print(container)
            letter_to_words[letter] = container
        if print_status:
            start = time.time()
            dict_of_words_num, _ = self.words_per_letter(letter_to_words)
            print(f"Execution Time for function (words_per_letter): {time.time() - start}\n\n")
            if plot:
                start = time.time()
                self.plotting_letters_num(dict_of_words_num)
                print(f"Execution Time for function (plotting_letters_num): {time.time() - start}\n\n")
        return letter_to_words




    #@profile(precision = 4)
    def spell_checking(self, letter_to_words):
        """check if the input word(s) is in the dictionary, else it prints the most
           similar 4 words to it.
        Args:
            letter_to_words (list): list of input word(s)
        Returns:
            general_similarity (list): most similar 4 words to the inputted word(s)
        """
        search_words = input("Enter the word(s) you want to search for: ").split(",")
        search_words = [word.lower().strip() for word in search_words]
        print(f"you entered: {search_words}")

        # letter_to_words = self.create_dictionary_of_words()
        general_similarity = []
        for search_word in search_words:
            if search_word in letter_to_words[search_word[0]]:
                print(f"Word ({search_word}) already found in the dictionary in the ({letter_to_words[search_word[0]].index(search_word) + 1}) postition of letter ({search_word[0]})\n\n")
            else:
                all_similar_words = []
                for i in range(1, 5):
                    similar_words = [w for w in letter_to_words[search_word[0]] if enchant.utils.levenshtein(w, search_word) == i]
                    all_similar_words.extend(similar_words)
                general_similarity.append(all_similar_words[:4])
                print(f"Word ({search_word}) not found\nThe nearest words for it are: {all_similar_words[:4]}\n\n")
        return general_similarity




    #@profile(precision = 4)
    def updating_dictionary(self, original_letter_to_words):
        """adding new word(s) to the input dictionary if words aren't already inside it.
        Args:
            original_letter_to_words (dict): all words corresponding to each starting letter
        Returns:
            letter_to_words (dict): new copy of the original dictionary that have updated the data
        """
        flag = 1
        search_words = input("Enter the word(s) you want to insert: ").split(",")
        search_words = [word.lower().strip() for word in search_words]
        print(f"you entered: {search_words}")

        # letter_to_words = self.create_dictionary_of_words()
        letter_to_words = deepcopy(original_letter_to_words)

        for search_word in search_words:
            if search_word in letter_to_words[search_word[0]]:
                print(f"Word ({search_word}) already found in the dictionary in the ({letter_to_words[search_word[0]].index(search_word) + 1}) postition of letter ({search_word[0]})\n\n")
            else:
                if flag:
                    password = input("Enter your password to allow adding to the dictionary: ")
                    flag = 0
                if password == self.password:
                    num_of_words_before = len(letter_to_words[search_word[0]])
                    letter_to_words[search_word[0]].append(search_word)
                    letter_to_words[search_word[0]].sort()
                    num_of_words_after = len(letter_to_words[search_word[0]])
                    print(f"({search_word}) successfully added to the dictionary in the ({letter_to_words[search_word[0]].index(search_word) + 1}) postition of letter ({search_word[0]})")
                    print(f"The vocabulary in the ({search_word[0]}) was {num_of_words_before}, but it becomes {num_of_words_after}\n\n")
                else:
                    print("Wrong password, you're unautherized\nYou can only search, or try again\n\n")
        return letter_to_words




    #@profile(precision = 4)
    def remove_vocab(self, original_letter_to_words):
        """removing existing word(s) from the input dictionary if words are already inside it.
        Args:
            original_letter_to_words (dict): all words corresponding to each starting letter
        Returns:
            letter_to_words (dict): new copy of the original dictionary that have updated the data
        """
        flag = 1
        search_words = input("Enter the word(s) you want to remove: ").split(",")
        search_words = [word.lower().strip() for word in search_words]
        print(f"you entered: {search_words}")

        # letter_to_words = self.create_dictionary_of_words()
        letter_to_words = deepcopy(original_letter_to_words)

        for search_word in search_words:
            if search_word in letter_to_words[search_word[0]]:
                if flag:
                    password = input("Enter your password to allow removing from the dictionary: ")
                    flag = 0
                if password == self.password:
                    num_of_words_before = len(letter_to_words[search_word[0]])
                    letter_to_words[search_word[0]].remove(search_word)
                    num_of_words_after = len(letter_to_words[search_word[0]])
                    print(f"Word ({search_word}) has been removed")
                    print(f"The vocabulary in the ({search_word[0]}) was {num_of_words_before}, but it becomes {num_of_words_after}\n\n")
                else:
                    print("Wrong password, you're unautherized\nYou can only search, or try again\n\n")
            else:
                print(f"Word ({search_word}) not found\n\n")

        return letter_to_words




    #@profile(precision = 4)
    def save_dictionary_dict(self, letter_to_words, fname):
        """saving the input dictionary.
        Args:
            letter_to_words (dict): all words corresponding to each starting letter
            fname (str): name of the file to save in
        Returns:
            None
        """
        dictionary = []
        for k in letter_to_words:
            dictionary.append(k)
            dictionary.extend(letter_to_words[k])
        with open(fname + ".txt", "w") as f:
            for word in dictionary:
                f.write(word + "\n")
        print(f"The created dictionary is saved in {fname+'.txt'} file\n\n")




    @profile(precision = 4)
    def main(self, flag = ["NULL"], fname = "saved_dic.txt"):
        """allow executing any of the above methods and prints the time and space
           complexity for each of them.
        Args:
            fname (str): name of the file to save in.
                        ( default = "saved_dic.txt")
        Returns:
            None
        """
        flag = [word.lower() for word in flag]

        if "create" in flag:
            start = time.time()
            letter_to_words = self.create_dictionary_of_words(print_status = False)
            print(f"Execution Time for function (create_dictionary_of_words): {time.time() - start}\n\n")

            if "check" in flag:
                start = time.time()
                self.spell_checking(letter_to_words)
                print(f"Execution Time for function (spell_checking): {time.time() - start}\n\n")

            if "update" in flag:
                start = time.time()
                updated_dic = self.updating_dictionary(letter_to_words)
                print(f"Execution Time for function (updating_dictionary): {time.time() - start}\n\n")

                if "remove" in flag:
                    start = time.time()
                    self.remove_vocab(updated_dic)
                    print(f"Execution Time for function (remove_vocab): {time.time() - start}\n\n")

                if "save" in flag:
                    start = time.time()
                    self.save_dictionary_dict(updated_dic, fname)
                    print(f"Execution Time for function (remove_vocab): {time.time() - start}\n\n")
