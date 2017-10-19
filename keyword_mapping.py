# -*- coding: utf-8 -*-
import re

class keyword_mapping:
    def __init__(self, enriched_related_GOids, keyword_related_GOids, query_keywd_set):
        self.enriched_related_GOids = enriched_related_GOids
        self.keyword_related_GOids  = keyword_related_GOids
        self.query_keywd_set = query_keywd_set

    def select_conserved_GOids(self, enriched_related_GOids, keyword_related_GOids, query_keywd_set):
        ### output object format:
            ##### Enriched GO ids and related GOids parsing from the GO trees
            ##### enriched_related_GOid_dict structure:
            #####    {go_id:{
            #####           "category": "COTERM_MF_DIRECT",
            #####            "keyword": [term name],
            #####            "enriched_related_GOid_dict":{
            #####                                           related_go_id1: term name1,
            #####                                           related_go_id2: term name2, etc}
            #####            "mapped_with_keyword_GOid_dict":{
            #####                                           related_go_id2: {[mapped_keyword], [term_name]}
            #####                                          }}

        keyword_mapped_dict = {}
        enriched_mapped_dict = {}
        for GOid in enriched_related_GOids:
            enriched_related_GOids[GOid]["mapped_with_keyword_GOid_dict"] = {}

        # for keyword in keyword_related_GOids:
        #     keyword_related_GOids[keyword]["similar_keyword_pattern_dict"] = {}
        # test_go_id = "GO:0043565"  ### belong to GO:0019237
        for keyword in keyword_related_GOids:
            keyword_GOid_dic = keyword_related_GOids[keyword] ## key: GOid, value: term name
            keyword_num_GOids = len(keyword_GOid_dic)
            if keyword_num_GOids>0:
                for keywd_GO_id in keyword_GOid_dic:
                    for GOids in enriched_related_GOids:

                        ## 1. Get mapped GO id(s):
                        related_tree_GOids = enriched_related_GOids[GOids]["enriched_related_GOid_dict"]
                        # print GOids, related_tree_GOids

                        ### test mapping and selection ###
                        # if test_go_id in related_tree_GOids:
                            # print GOids, test_go_id
                        ##################################
                        if keywd_GO_id in related_tree_GOids:
                            term_name = related_tree_GOids[keywd_GO_id]
                            enriched_related_GOids[GOid]["mapped_with_keyword_GOid_dict"][keywd_GO_id] = {keyword, term_name}

                        ## 2. Get similar keyword pattern:
                        # keyword_mapped_dict
                        for desire_keyword in query_keywd_set:
                            for related_tree_goid in related_tree_GOids:
                                enriched_related_term = related_tree_GOids[related_tree_goid]
                                if desire_keyword not in keyword_mapped_dict:
                                    keyword_mapped_dict[desire_keyword] = {}
                                # print desire_keyword +":"+ enriched_related_term
                                if re.match(".*"+desire_keyword+".*", enriched_related_term):
                                    if GOids not in keyword_mapped_dict[desire_keyword]:
                                        keyword_mapped_dict[desire_keyword][GOids] = {}
                                    keyword_mapped_dict[desire_keyword][GOids][related_tree_goid] = enriched_related_term

        # for key in keyword_mapped_dict:
        #     print key
        #     print keyword_mapped_dict[key]
        #     print "========================"
        return enriched_related_GOids, keyword_mapped_dict

    def main(self):
        enriched_related_GOids = self.enriched_related_GOids
        keyword_related_GOids = self.keyword_related_GOids
        query_keywd_set = self.query_keywd_set
        mapped_enrich_related_GOids_dict, mapped_keyword_related_GOids_idct = self.select_conserved_GOids(enriched_related_GOids, keyword_related_GOids, query_keywd_set)
        # self.select_conserved_GOids(enriched_related_GOids, keyword_related_GOids)
        return mapped_enrich_related_GOids_dict, mapped_keyword_related_GOids_idct
        # print mapped_enrich_related_GOids_dict
        # for item in mapped_enrich_related_GOids_dict:
        #
        #     print mapped_enrich_related_GOids_dict[item]["category"]
        #     print mapped_enrich_related_GOids_dict[item]["keyword"]
        #     print mapped_enrich_related_GOids_dict[item]["enriched_related_GOid_dict"]
        #     print mapped_enrich_related_GOids_dict[item]["mapped_with_keyword_GOid_dict"]
        #     print mapped_enrich_related_GOids_dict[item]["similar_keyword_pattern_dict"]
        #     print "======================================================"
        # for keyword in mapped_keyword_related_GOids_idct:
        #     print "keyword: "+keyword
        #     print mapped_keyword_related_GOids_idct
        #     # for mapped_goid in mapped_keyword_related_GOids_idct[keyword]:
        #     #     print mapped_goid +":"+ keyword_related_GOids[keyword][mapped_goid]
        #     print "==============================================================="
