import re

class keyword_clean:
    def __init__(self, pwd):
        self.pwd = pwd

    def get_partial_kw(self, string):
        if re.match(".*-[0-9]+", string) or re.match(".* [0-9]+", string):
            # print reline
            re_word = string.split("-")[0]
            return re_word

        else:
            return string

    def get_keyword_set(self):
        pwd = self.pwd
        read_input = open(pwd, "r")
        original_kw_set = set() #### construct original keyword set
        partial_kw_set = set() #### construct partial keyword set
        for line in read_input:
            reline = line.strip()

            if re.match(".*\/.*", reline):
                # print line
                words = reline.split("/")
                for word in words:
                    original_kw_set.add(word)
                    par_word = self.get_partial_kw(word)
                    if par_word not in original_kw_set:
                        partial_kw_set.add(par_word)

            elif re.match(".*\({1}.*", reline):
                # print reline
                words = re.split("\(|\)", reline)
                for word in words:
                    if len(word.strip()) >0:
                        original_kw_set.add(word.strip())
                        par_word = self.get_partial_kw(word.strip())
                        if par_word not in original_kw_set:
                            partial_kw_set.add(par_word)
            else:
                original_kw_set.add(reline)
                par_word = self.get_partial_kw(reline)
                if par_word not in original_kw_set:
                    partial_kw_set.add(par_word)

        # print original_kw_set
        # print len(original_kw_set)
        # print "=========================================="
        # print partial_kw_set
        # print len(partial_kw_set)
        read_input.close()
        return original_kw_set, partial_kw_set
