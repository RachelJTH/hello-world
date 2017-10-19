
class mapping_output:
    def output(self, output_pwd, enriched_mapping_dict, kyword_mapping_dict):
        # output_file =
    for enriched_GOid in enriched_mapping_dict:
        mapped_dict = enriched_mapping_dict[enriched_GOids]["mapped_with_keyword_GOid_dict"]
        category = enriched_mapping_dict["category"]
        if len(mapped_dict) > 0:

            for keyword_goid in mapped_dict:
                keyword = mapped_dict[keyword_goid]
                Targeted_GO_id = keyword_goid
                Enriched_GO_id = enriched_GOid
                Category = category


    # File columns:
    # Keyword – from customer
    # Targeted_GO_id -  Query and mapping result
    # Enriched_GO_id – from target prediction enrichment result
    # Category -  from target prediction enrichment result
    # Other enriched information -  from target prediction enrichment result
