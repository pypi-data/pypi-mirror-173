

def sigma_dq_helper_update_dqaction_dqmessage(results_final,target_table_cleaned,dq_action,dq_message,runid):
  w_cond = sigma_dq_helper_generate_update_condition(results_final)
  w_cond_count = (len(w_cond))
  stmnt_list = []
  for a in w_cond :
    if w_cond_count > 1:
      stmnt_ = a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\') OR'
      stmnt_list.append(stmnt_)
    else:
      stmnt_ = a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\')'
      stmnt_list.append(stmnt_)

  x = 'update ' + target_table_cleaned + ' set  DQ_Action = "' + dq_action + '" , DQ_Message = "' + ' '.join(str(x) for x in dq_message) +'" where '
  if w_cond_count > 1:
    x_ = x + ' '+ ' '.join(stmnt_list)[:-3]
  else:
    x_ = x + ' '+ ' '.join(stmnt_list)
  
  try:
    spark.sql(x_)
    status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" completed "
  except Exception as e:
    status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" failed\n" + str(e)
    
  return(status_)