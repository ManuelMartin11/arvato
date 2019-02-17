import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_na_dist(dataset, title):
    """Function to plot missing values from the dataset"""
    
    mv = dataset.isna().sum()
    total_rows = dataset.shape[0]
    mv_only = mv[mv/total_rows > 0.1].sort_values().to_dict()
    col_names, missing_values = list(mv_only.keys()), list(mv_only.values())
    missing_values = [(mv/total_rows)*100 for mv in missing_values]
            
    sns.set()
    plt.figure(figsize=[14, 3])
    plt.bar(col_names, missing_values)
    plt.ylabel("Percent of Missing Values")
    plt.xticks(rotation=90)
    plt.title(title)
    plt.show()
    
def apply_nan(dataset, ref_set):
    """Replace missing values with NaNs"""
    
    atts = ref_set.attribute.values
    miss_codes = ref_set.missing_or_unknown.values
    exc_str = {"[-1,XX]":"[-1,'XX']", "[-1,X]":"[-1,'X']", "[XX]":"['XX']"}
    
    for att, mcodes in zip(atts, miss_codes):
        if att and mcodes:
            
            if mcodes in exc_str.keys():
                mcodes = exc_str[mcodes]
            
            mcodes_ = eval(mcodes)
            for co in mcodes_:
                dataset[att] = dataset[att].replace(co, np.nan)
                
    return dataset

def get_misval_features(dataset, threshold):
    """Get the features from the dataset with missing values"""
    
    mv = dataset.isna().sum()
    total_rows = dataset.shape[0]
    mv_only = mv[mv/total_rows > threshold].sort_values().to_dict()
    
    features = mv_only.keys()
    return features

def get_information_level_att(dataset, information_level, ref):
    """Retrieve a filtered dataset with the information level required"""
    cols = list(ref[ref.information_level == information_level].attribute)
    removed_cols = ["ALTER_HH", "GEBURTSJAHR", "KBA05_BAUMAX", "KK_KUNDENTYP", "AGER_TYP", "TITEL_KZ"]
    good_cols = [col for col in cols if col not in removed_cols]
    d = dataset.loc[:, dataset.columns.isin(good_cols)]
    return d.copy()

def join_df(df1, df2):
    """Concatenate the 2 dataframes given"""
    result = pd.concat([df1, df2], axis=1, sort=False)
    return result

def plot_corrmat(corr_df, il1, il2):
    """PLot a correlation matrix with the dataframe.corr() matrix given"""
    #plt.figure(figsize=[15, 10]) 
    sns.heatmap(corr_df,cmap=cmap, cbar=False, linewidth=0.5, square=True)
    plt.title(f"Correlation Matrix for {il1.capitalize()} and {il2.capitalize()} Information Levels")
    plt.show()
    
"""
INFORMATION LEVELS:
person', 'household', 'building', 'microcell_rr4',
'microcell_rr3', 'postcode', 'region_rr1', 'macrocell_plz8',
'community'"""

def corrmat_information_levels(dataset, il1, il2):
    """plot a group A versus a group B correlation matrix"""
    
    dfil1 = get_information_level_att(dataset, il1)
    dfil2 = get_information_level_att(dataset, il2)
    dfil1_il2 = join_df(dfil1, dfil2)
    dfil1_il2 = dfil1_il2.corr()[dfil1.columns].filter(items=list(dfil2.columns), axis=0)
    plot_corrmat(dfil1_il2, il1, il2)
    

def subplots_(dataset, plot_name):
    """ """
    fig, axs = plt.subplots(3, 3)
    
    
