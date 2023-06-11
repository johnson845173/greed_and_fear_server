from dbcon import processquery

tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM website.policy_data where policy_type = 1")

tc_json =tc_df.to_json(orient='index')