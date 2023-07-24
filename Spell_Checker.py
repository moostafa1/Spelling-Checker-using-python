import time
import enchant
import matplotlib.pyplot as plt
from copy import deepcopy
from memory_profiler import profile
import requests



class Spell_Checker:
    def __init__(self, dictionary_fname = "dictionary.txt"):
        self.dictionary = dictionary_fname
        self.password = "authenticated_1"
        # self.punctuation = ["!", "?", "@", "#", "$", "%", "^", "&", "*", "/", "(", ")", "_", "-"]




    #@profile(precision = 4)
    def read_text_dictionary(self):
        with open(self.dictionary) as f:
            dictionary = f.read().split('\n')[:-1]
        unique_dictionary = list(sorted(set(dictionary)))

        a_to_z = [letter for letter in unique_dictionary if len(letter) == 1]
        return a_to_z, unique_dictionary




    #@profile(precision = 4)
    def words_per_letter(self, letter_to_words):
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
        letters = list(letter_to_words.keys())
        num_of_words = list(letter_to_words.values())

        plt.bar(range(len(letter_to_words)), num_of_words, tick_label = letters)
        plt.show()




    #@profile(precision = 4)
    def create_dictionary_of_words(self, print_status = False, plot = False):   # , a_to_z, dictionary
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
        search_words = input("Enter the word(s) you want to search for: ").split(",")
        search_words = [word.lower().strip() for word in search_words]
        print(f"you entered: {search_words}")

        # letter_to_words = self.create_dictionary_of_words()
        for search_word in search_words:
            if search_word in letter_to_words[search_word[0]]:
                print(f"Word ({search_word}) already found in the dictionary in the ({letter_to_words[search_word[0]].index(search_word) + 1}) postition of letter ({search_word[0]})\n\n")
            else:
                all_similar_words = []
                for i in range(1, 5):
                    similar_words = [w for w in letter_to_words[search_word[0]] if enchant.utils.levenshtein(w, search_word) == i]
                    all_similar_words.extend(similar_words)
                print(f"Word ({search_word}) not found\nThe nearest words for it are: {all_similar_words[:4]}\n\n")




    #@profile(precision = 4)
    def updating_dictionary(self, original_letter_to_words):
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
