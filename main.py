# -*- coding: utf-8 -*-
from keyword_clean import keyword_clean
from amigo_api import GOlr_api
from keyword_mapping import keyword_mapping
from output_format import mapping_output

# working_pwd = "D:/RachelHuang/0_Customer service/2017-05-18 John/raw_data/GO_key word/key_word_2017oct.txt"
dir_pwd = "D:/RachelHuang/python_test/general_codes/GO_analysis/test_file/test_GO/" #### the location of enriched GO directory
keyword_filename = "test_keyword.txt"
GO_file_name = "GO"

##### keyword preprocessing #####
keyword_obj = keyword_clean(dir_pwd+keyword_filename)
# print keyword_obj
original_kw_set, partial_kw_set = keyword_obj.get_keyword_set()
# print len(original_kw_set)
# print original_kw_set
# print partial_kw_set

##### GOrl Query #####
# enriched_GO_working_pwd = "D:/RachelHuang/0_Customer service/2017-05-18 John/raw_data/GO/GO/"
##### [Test] avaliable : get_keyword_related_GOids
# query_kw_set = ["Rhino-Deadlock-Cutoff Complex"]

enriched_GO_working_pwd = dir_pwd + GO_file_name+"/"
amigo_obj = GOlr_api()
# ori_enriched_related_GOids, ori_keyword_related_GOids = amigo_obj.main(enriched_GO_working_pwd, original_kw_set)
part_enriched_related_GOids, part_keyword_related_GOids = amigo_obj.main(enriched_GO_working_pwd, partial_kw_set)

##### [Test] Partial query dataframe
# print "GO id query: "
# print part_enriched_related_GOids
# print "================================"
# print "Keyword query: "
# print part_keyword_related_GOids

##### [Test] Ori query dataframe
# print "GO id query: "
# print ori_enriched_related_GOids
# print "================================"
# print "Keyword query: "
# print ori_keyword_related_GOids

# ori_mapping_obj = keyword_mapping(ori_enriched_related_GOids, ori_keyword_related_GOids, original_kw_set)
# ori_enriched_related_GOids, ori_keyword_mapped_dict = ori_mapping_obj.main()
part_mapping_obj = keyword_mapping(part_enriched_related_GOids, part_keyword_related_GOids, partial_kw_set)
part_enriched_related_GOids, part_keyword_mapped_dict = part_mapping_obj.main()

### Write output
mapping_output_obj = mapping_output()
output_pwd = dir_pwd + "part_enriched_goid_mapped_test.txt"
mapping_output_obj.output(output_pwd, part_enriched_related_GOids)
