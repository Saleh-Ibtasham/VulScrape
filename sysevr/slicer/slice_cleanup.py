import os

def cleanup(sentences):
    temp_sentences = []
    temp_sentence = ""
    for index, sentence in enumerate(sentences):
        try:
            number = int(sentence.split(" ")[-1])
            temp_sentence = temp_sentence + sentence
            temp_sentences.append(temp_sentence)
            temp_sentence = ""

        except:
            temp_sentence = temp_sentence + sentence

    return temp_sentences

def clean_slices(working_directory):
    slice_path = working_directory + "slice_files/"

    for filename in os.listdir(slice_path):
        if (filename.endswith('.txt') is False) or ("new" in filename):
            continue

        file_path = os.path.join(slice_path, filename)
        f = open(file_path, 'r')

        slicelists = f.read().split('------------------------------')
        f.close()

        if slicelists[0] == '':
            del slicelists[0]
        if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
            del slicelists[-1]

        new_file_path = os.path.join(slice_path, "new_" + filename)
        f = open(new_file_path, 'w')
        index = -1
        for slicelist in slicelists:
            index += 1
            sentences = slicelist.split('\n')
            sentences = cleanup(sentences)
            if sentences[0] == '\r' or sentences[0] == '':
                del sentences[0]
            if sentences == []:
                continue
            if sentences[-1] == '':
                del sentences[-1]
            if sentences[-1] == '\r':
                del sentences[-1]

            unsorted_sentences = sentences[1:]

            # unsorted_list = []
            #
            # for sentence in unsorted_sentences:
            #     temp_list = sentence.split(" ")
            #     unsorted_list.append(temp_list)
            #
            # sorted_list = sorted(unsorted_list, key=lambda x: int(x[-1]))

            f.write(str(sentences[0]) + '\n')
            # for sentence in sorted_list:
            #     temp_sentence = (" ").join(sentence)
            #     f.write(str(temp_sentence) + '\n')

            for sentence in unsorted_sentences:
                f.write(str(sentence) + '\n')
            f.write('------------------------------' + '\n')
        f.close()

    for filename in os.listdir(slice_path):
        if (filename.endswith('.txt') is False) or ("new" in filename):
            continue
        file_path = os.path.join(slice_path, filename)
        os.remove(file_path)

    for filename in os.listdir(slice_path):
        if filename.endswith('.txt') and ("new" in filename):
            file_path = os.path.join(slice_path, filename)
            new_file_path = os.path.join(slice_path, filename.replace("new_", ""))
            os.rename(file_path, new_file_path)
