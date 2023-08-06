## execute validations
def  sigma_dq_helper_execute_validation_stmnts(expectation_suite):
  columns_values_parent = {}
  columns_values_child = {}
  i = 0 
  DQ_action = 'Pass'
  for stmnt in expectation_suite:
    if stmnt.startswith('sigma_dq_check') == True:
      stmnt_ = eval(stmnt)
      columns_values_child = {}
      if stmnt_['success'] == False:
        columns_values_child['column'] = stmnt_['column']
        columns_values_child['rule'] = stmnt_['rule']
        columns_values_child['total_rows_checked'] = stmnt_['total_rows_checked']
        columns_values_child['total_rows_failed'] = stmnt_['total_rows_failed']
        columns_values_child['success'] = stmnt_['success']
        columns_values_child['failed_percent'] = stmnt_['failed_percent']
        columns_values_child['failed_values'] = stmnt_['failed_values']
        columns_values_child['meta'] = stmnt_['meta']
        columns_values_parent[i] = columns_values_child
        DQ_action = 'Fail'
        i = i + 1
      else:
        columns_values_child['column'] = stmnt_['column']
        columns_values_child['rule'] = stmnt_['rule']
        columns_values_child['total_rows_checked'] = stmnt_['total_rows_checked']
        columns_values_child['total_rows_failed'] = stmnt_['total_rows_failed']
        columns_values_child['success'] = stmnt_['success']
        columns_values_child['passed_percent'] = stmnt_['passed_percent']
        columns_values_child['meta'] = stmnt_['meta']
        columns_values_parent[i] = columns_values_child
        DQ_action = 'Fail'
        i = i + 1
      
    else:
      stmnt_ = eval(stmnt)
      columns_values_child = {}
      if stmnt_['success'] == False:
        failed_column = stmnt_['expectation_config']['kwargs']['column']
        failed_rule = stmnt_['expectation_config']['expectation_type']
        total_rows_checked = stmnt_['result']['element_count']
        total_rows_failed = stmnt_['result']['unexpected_count']
        failed_percent = stmnt_['result']['unexpected_percent_total']
        raw_fail_list = stmnt_['result']['unexpected_list']
        raw_fail_list_ = unique_elements_in_list(raw_fail_list)
        columns_values_child['column'] = failed_column
        columns_values_child['rule'] = failed_rule

        columns_values_child['total_rows_checked'] = total_rows_checked
        columns_values_child['total_rows_failed'] = total_rows_failed
        columns_values_child['failed_percent'] = failed_percent
        columns_values_child['failed_values'] = raw_fail_list_
        columns_values_child['success'] = False
        columns_values_child['meta'] = stmnt_['meta']
        columns_values_parent[i] = columns_values_child
        DQ_action = 'Fail'
        i = i + 1
      else:
        #print(stmnt_)
        pass_column = stmnt_['expectation_config']['kwargs']['column']
        pass_rule = stmnt_['expectation_config']['expectation_type']
        total_rows_checked = stmnt_['result']['element_count']
        total_rows_failed = stmnt_['result']['unexpected_count']
        passed_percent = ((total_rows_checked - total_rows_failed)/total_rows_checked) * 100
        columns_values_child['column'] = pass_column
        columns_values_child['rule'] = pass_rule

        columns_values_child['total_rows_checked'] = total_rows_checked
        columns_values_child['total_rows_failed'] = total_rows_failed
        columns_values_child['success'] = True
        columns_values_child['passed_percent'] = passed_percent
        columns_values_child['meta'] = stmnt_['meta']
        columns_values_parent[i] = columns_values_child

        ## logic to filter and update dq message json
        i = i + 1
  #columns_values_parent[i] = {'DQ_action':   DQ_action} 
  return columns_values_parent