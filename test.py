### test comparison
import re
candidate_term = "piRNA cluster binding"
keyword = "piRNA"
pattern = ".*"+keyword+".*"
if re.match(pattern, candidate_term):
    print "ok"
