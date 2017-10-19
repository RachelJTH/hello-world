import MySQLdb, re

class GO_test:
    def __init__(self, go_id):
        ##### custormized setting #####
        self.query_field_set = ["go_id", "name", "synonym", "is_a", "intersection_of"]
            ## whole fields/item and definition, process function: show_table_columns_and_def

        ##### database_setting #####
        self.host = "192.168.11.116"
        self.user_name = "rachel"
        self.pass_wd = "bioinfo123$"
        self.query_db = "go_obo"

        ##### other solid parameter #####
        self.go_id = go_id
        self.query_summary = ', '.join(self.query_field_set)

    def show_table_columns_and_def(self):
        query_cmd = "show columns from go_summary;"
        result = self.connect_db(query_cmd)
        # print result
        for line in result:
            print line

    def connect_db(self, query_cmd):
        host = self.host
        user_name = self.user_name
        pass_wd = self.pass_wd
        query_db = self.query_db

        db = MySQLdb.connect(host= host, user=user_name, passwd=pass_wd, db=query_db)
        sor = db.cursor()
        sor.execute(query_cmd)
        db.close()
        result = sor.fetchall()
        return result

    def get_go_summary(self):
        go_id = self.go_id
        query_summary = self.query_summary
        query_cmd = "SELECT "+query_summary+" FROM go_summary WHERE go_id LIKE \""+ go_id + "\";"
        # print query_cmd
        result = self.connect_db(query_cmd)
        results = result[0]
        go_id = results[0]
        name = results[1]
        synonym = results[2]
        is_a = results[3]
        intersection_of = results[4]
        # print "go_id: "+go_id
        # print "name: "+name
        # print "synonym: "+synonym
        # print "is_a: "+is_a
        # print "intersection_of: "+intersection_of
        return go_id, name

# if __name__ == "__main__":
#     go_id = "GO:0015937"
#     go_obj = GO_test(go_id)
#     # go_obj.show_table_columns_and_def()
#     go_obj.get_go_summary()
