#### GO API for GO text comparison analysis [2017-10-17]

from bs4 import BeautifulSoup
import re, requests, os, glob, json, sys
from keyword_clean import keyword_clean

from go_local_query import GO_test
class GOlr_api:
    def __init__(self):
        #### Parameter Setting: ####
        self.searched_label = "regulates_closure_label"
        # searched_label = "regulates_closure_label"

        self.row_no = "10"
        self.fq="ontology_class"
        self.version = "2.2"
        self.GOlr_url_prefix = "http://golr.berkeleybop.org/select?qt=standard&fl=*&"

        #### select query format and setting #### >> return jason format -
        ### other avaliable url:
        # test_GOlr = "http://golr.berkeleybop.org/select?qt=standard&fl=*&version=2.2&wt=json&indent=on&rows="+row_no+"&q=id:%22"+q+"%22&fq=document_category:%22"+fq+"%22"
        # test_GOlr = "http://golr.berkeleybop.org/select?qt=standard&fl=*&version=2.2&wt=json&indent=on&rows="+row_no+"&q="+searched_label+":%22"+key_word+"%22&fq=document_category:%22ontology_class%22"
        # test_GOlr = "http://golr.berkeleybop.org/select?qt=standard&fl=*&version=2.2&wt=json&indent=on&rows=1&q=annotation_class_label:%22nucleus%22&fq=document_category:%22ontology_class%22"

    def search_1_keyword_url(self, keyword): #### searching 1 -  ""keyword"" search
        GOlr_url_prefix = self.GOlr_url_prefix
        version = self.version
        row_no = self.row_no
        searched_label = self.searched_label
        fq = self.fq
        GOlr = GOlr_url_prefix+"version="+version+"&wt=json&indent=on&rows="+row_no+"&q="+searched_label+":%22"+keyword+"%22&fq=document_category:%22"+fq+"%22"
        return GOlr

    def search_2_GOid_url(self, GO_id): ### searching 2 -  ""GO id"" search:
        GOlr_url_prefix = self.GOlr_url_prefix
        version = self.version
        row_no = self.row_no
        searched_label = self.searched_label
        fq = self.fq
        GOlr = GOlr_url_prefix+"version="+version+"&wt=json&indent=on&rows="+row_no+"&q=id:%22"+GO_id+"%22&fq=document_category:%22"+fq+"%22"
        return GOlr

    def search_3_all_url(self): ### searching 3 - "search 20 rows":
        GOlr_url_prefix = self.GOlr_url_prefix
        version = self.version
        row_no = self.row_no
        searched_label = self.searched_label
        fq = self.fq
        GOlr = GOlr_url_prefix+"version="+version+"&wt=json&rows=20&indent=on&q=*:*&start=0"
        return GOlr

    def get_url_info(self, GOlr):
        # search_type: 1- using "key word", 2- using "GO id"
        res = requests.get(GOlr)
        res2 = res.text.encode('utf8')
        soup = BeautifulSoup(res2)
        item = soup.p.text
        # print str(item)
        d = json.loads(item)
        no_query_result = d["response"]["numFound"]
        related_id_dic = {}

        if no_query_result > 0:
            # print d
            sub_info = d["response"]["docs"][0]
            go_id = sub_info["id"]
            # annotation_class_label = sub_info["annotation_class_label"]
            tree_go_ids = json.loads(sub_info["topology_graph_json"])["nodes"]
            for item in tree_go_ids:
                node_go_id = item["id"]
                node_go_id_term = item["lbl"]   ### label of GO id
                if node_go_id not in related_id_dic:
                    related_id_dic[node_go_id] = node_go_id_term
            # print go_id, annotation_class_label
            # print related_id_set
            # print len(related_id_set)

        return related_id_dic
        ### [test]
        # return d

    def write_out_file(self, output_string):
        out_file = open(test_output, 'w')
        out_file.write(schema)
        # print type(schema)
        out_file.close()

    def get_enriched_related_GOids(self, go_id): ## key: enriched GO id, value: GO id list
        GOlr = self.search_2_GOid_url(go_id)
        related_goid_dic = self.get_url_info(GOlr)
        if len(related_goid_dic) == 0:
            #### query from local database
            local_db_obj = GO_test(go_id)
            query_go_id, name = local_db_obj.get_go_summary()
            related_goid_dic[go_id] = name
        return related_goid_dic

    def get_keyword_related_GOids(self, keywords): ## key: keyword, value: GO id list
        keyword_related_GOids = {}
        for keyword in keywords:
            GOlr = self.search_1_keyword_url(keyword)
            related_id_set = self.get_url_info(GOlr)
            keyword_related_GOids[keyword] = related_id_set
        # print keyword_related_GOids
        # print len(related_id_set)
        return keyword_related_GOids

    def main(self, working_pwd, query_kw_set):
        enriched_related_GOids = {} ### key: GO_id, category: category, keyword: term
        ### go_dict = {GO_id:{category: category, keyword: term}, GO_id2...}

        ### output object format - 1. enriched_related_GOid_dict
            ##### Enriched GO ids and related GOids parsing from the GO trees
            ##### enriched_related_GOid_dict structure:
            #####    {go_id:{
            #####           "category": "COTERM_MF_DIRECT",
            #####            "keyword": [term name],
            #####            "enriched_related_GOid_dict":{
            #####                                           related_go_id1: term name1,
            #####                                           related_go_id2: term name2, etc}}}

        ### output object format - 2. keyword_related_GOids
            ##### query keywords and related GOids parsing from the GO trees
            ##### keyword_related_GOids structure:
            ##### {"keyword1": {
            #####               related_go_id1: term name1,
            #####               related_go_id2: term name2, etc},
            #####  "keyword2": {},
            #####  "keyword3": {
            #####               related_go_id3: term name3,
            #####               related_go_id4: term name4, etc.} ...}

        ## 1. Import keywords file and constructn keyword set:
        if os.path.exists(working_pwd):
            files = glob.glob(working_pwd+"*.txt")
            for file in files:
                open_file = open(file, 'r')

                ## 2. read each GO files and get the GO id and the related tree GO id set
                for line in open_file.readlines():
                    if re.match("^Category", line.strip()):
                        pass
                    else:
                        item = line.split("\t")
                        info = item[1].split("~")
                        GO_id = info[0]
                        category = item[0]
                        keyword = info[1]
                        # print GO_id, category, keyword
                        if GO_id in enriched_related_GOids: ## remove redundent info
                            pass
                        else:
                            enriched_related_GOids[GO_id] = {}
                            enriched_related_GOids[GO_id]["category"] = category
                            enriched_related_GOids[GO_id]["keyword"] = keyword
                            enriched_related_GOid_dict = self.get_enriched_related_GOids(GO_id)
                            enriched_related_GOids[GO_id]["enriched_related_GOid_dict"] = enriched_related_GOid_dict

                            ##### [Test]: check total GO ids after querying
                            # print GO_id
                            # print len(enriched_related_GOids[GO_id]["enriched_related_GOid_dict"])
                            # print "================================"

        ##### keyword searching and related go ids
        keyword_related_GOids = self.get_keyword_related_GOids(query_kw_set)
        # print enriched_related_GOids
        # print "============================="
        # print keyword_related_GOids
        return enriched_related_GOids, keyword_related_GOids


# if __name__ == "__main__":
    # working_pwd = "D:/RachelHuang/0_Customer service/2017-05-18 John/raw_data/GO/GO/"
        ### result directory of GO enrichment
    # key_words_file = working_pwd+""
        ### key words list

    #### avaliable test : get_keyword_related_GOids
    # query_kw_set = ["Rhino-Deadlock-Cutoff Complex"]
    ### processing main script ###
    # working_pwd = "D:/RachelHuang/python_test/general_codes/GO_analysis/test_file/test_GO/" #### the location of enriched GO directory
    # keyword_filename = "test_keyword.txt"
    # GO_file_name = "GO"
    # keyword_obj = keyword_clean(working_pwd+keyword_filename)
    # print keyword_obj
    # original_kw_set, partial_kw_set = keyword_obj.get_keyword_set()
    # enriched_GO_working_pwd = working_pwd + GO_file_name+"/"
    #
    # golr_obj = GOlr_api()
    # golr_obj.main(enriched_GO_working_pwd, original_kw_set)
    # GOlr = golr_obj.search_1_keyword_url("Activin A")
    # all_info = golr_obj.get_url_info(GOlr)
    # print all_info
