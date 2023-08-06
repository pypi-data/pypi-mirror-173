def sigma_dq_helper_generate_final_result (runid,target_table,results_final,dq_action,dq_message):
  results_out = {}
  results_out['runid'] = runid
  results_out['target_table'] = target_table
  results_out['results_final'] = results_final
  results_out['dq_action'] = dq_action
  results_out['dq_message'] = dq_message
  results_out['statistics'] = {}

  evaluated_quality_checks = len(results_final)
  successful_expectations = 0
  unsuccessful_expectations = 0
  success_percent = 0.0

  for a in results_final:

    if results_final[a]['success'] == True:
      successful_expectations =  successful_expectations + 1
    else:
      unsuccessful_expectations = unsuccessful_expectations + 1

  results_out['statistics']['evaluated_quality_checks'] = evaluated_quality_checks 
  results_out['statistics']['successful_expectations'] = successful_expectations 
  results_out['statistics']['unsuccessful_expectations'] = unsuccessful_expectations 
  results_out['statistics']['success_percent'] = (successful_expectations/evaluated_quality_checks) * 100
  #for a in results_final:
  #  print(a)
  #  return results_out
  return results_out