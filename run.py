from Spell_Checker import Spell_Checker


if __name__ == "__main__":
    create = Spell_Checker().create_dictionary_of_words()
    similar = Spell_Checker().spell_checking(create)
    print(similar)
    update = Spell_Checker().updating_dictionary(create)
    remove = Spell_Checker().remove_vocab(create)
