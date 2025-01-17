import pandas as pd
import os
import sys

branching_csv_file_path = 'app/code/experiments/function_calls/data/getrgfapc_data.csv'
nobranching_csv_file_path ='app/code/experiments/branch_apc/data/noBranching_data.csv'
pythonBranching_csv_file_path ='app/code/experiments/branch_apc/data/pythonBranch.csv'


if os.path.exists(branching_csv_file_path):
    getrgfapc_df = pd.read_csv(branching_csv_file_path)
    getrgfapc_df = getrgfapc_df.iloc[:,1:]
else:
    print("PANIC, no getrgf data, cannot proceed")
    sys.exit()
    

###########Initializing dataframes##############

noBranching_df = pd.DataFrame(columns = ["graph_name", "noBranchingapc", "noBranching_time", 'noBranchingMathTime', 'noBranchingFirstHalfTime', "(no)longest for getrgf", "(no)longest time",'noBranchingCase','noBranchingGamma'])
noBranching_df['graph_name'] = getrgfapc_df['graph_name']
noBranching_df = noBranching_df.fillna('na')

pythonBranching_df = pd.DataFrame(columns = ["graph_name", "pythonBranchingAPC", "pythonBranching_time", 'pythonBranchingMathTime', 'pythonBranchingFirstHalfTime', "(python)longest for getrgf", "(python)longest time",'pythonBranchingCase','pythonBranchingGamma'])
pythonBranching_df['graph_name'] = getrgfapc_df['graph_name']
pythonBranching_df = pythonBranching_df.fillna('na')

#############################################

if os.path.exists(nobranching_csv_file_path):
    df = pd.read_csv(nobranching_csv_file_path)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        noBranching_df = df
        noBranching_df = noBranching_df.iloc[:,1:] #drop first column
if os.path.exists(pythonBranching_csv_file_path):
    df = pd.read_csv(pythonBranching_csv_file_path)
    df.rename(columns = {'firstHalfTime':'naiveFirstHalfTime'}, inplace = True)
    if df['graph_name'].equals(getrgfapc_df['graph_name']):
        pythonBranching_df = df
        pythonBranching_df = pythonBranching_df.iloc[:,1:]

merge1 = pd.merge(noBranching_df,pythonBranching_df)
mergefinal = pd.merge(merge1, getrgfapc_df)

new_order = ['graph_name',"noBranchingapc",'getrgfapc', "pythonBranchingAPC",
                          "noBranching_time",'getrgfapc_time',"pythonBranching_time",
                          'noBranchingFirstHalfTime', 'noBranchingMathTime',"(no)longest for getrgf", "(no)longest time",'noBranchingCase','noBranchingGamma',
                          'firstHalfTime','getrgfTime','longest for getrgf','longest time','case','gamma',
                          'pythonBranchingMathTime', 'pythonBranchingFirstHalfTime', "(python)longest for getrgf", "(python)longest time",'pythonBranchingCase','pythonBranchingGamma']
mergefinal = mergefinal[new_order]



mergefinal.rename(columns = {'getrgfapc':'BranchingAPC'}, inplace = True)
mergefinal.rename(columns = {'getrgfapc_time':'BranchingAPC_time'}, inplace = True)
mergefinal.rename(columns = {'firstHalfTime':'BranchingFirstHalfTime'}, inplace = True)
mergefinal.rename(columns = {'getrgfTime':'BranchingMathTime'}, inplace = True)



mergefinal.to_csv("app/code/experiments/branch_apc/data/final_branching_data.csv")

print('=========================printing final data table=================================')
print(mergefinal[['graph_name',"noBranchingapc",'BranchingAPC', "pythonBranchingAPC",
                          "noBranching_time",'BranchingAPC_time',"pythonBranching_time"]])


