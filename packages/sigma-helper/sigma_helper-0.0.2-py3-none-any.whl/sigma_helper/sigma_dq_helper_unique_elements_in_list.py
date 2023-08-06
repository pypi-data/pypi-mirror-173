## generate unique emelents in a list  
def sigma_dq_helper_unique_elements_in_list(list1):
  unique_list = []
  for x in list1:
    if x not in unique_list:
      unique_list.append(x)
  return unique_list