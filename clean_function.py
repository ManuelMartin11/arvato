

def clean(dtM THRES=30):
    """

    :input: dataset
    :output: cleaned dataset
    """

    # Drop non-informative features
    dt = dt.drop(["ALTER_HH", "GEBURTSJAHR", "KBA05_BAUMAX", "KK_KUNDENTYP", "AGER_TYP", "TITEL_KZ"], axis = 1)
   
    # Get only low missing values features
    mv_inrows = dt.isna().sum(axis=1)
    dt = dt[mv_inrows < THRES]

    # Imputing missing values
    imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    dt = dt.copy()
    dt[:] = imp.fit_transform(dt)

    dt.CAMEO_DEUG_2015 = dt.CAMEO_DEUG_2015.apply(lambda x: float(x) if x is not np.nan else np.nan)
    dt.CAMEO_INTL_2015 = dt.CAMEO_INTL_2015.apply(lambda x: float(x) if x is not np.nan else np.nan)
    dt.OST_WEST_KZ = dt.OST_WEST_KZ.astype("category").cat.codes
    dt.CAMEO_DEU_2015 = dt.CAMEO_DEU_2015.astype("category").cat.codes

    for feature in feat_info[feat_info.type.isin(["mixed", "categorical"])].attribute.values.tolist():
        if feature in dataset.columns:
            rows = dataset[feature].shape[0]
            cat_dist = dataset[feature].value_counts().sort_values(ascending=False)
            cat_dist_norm = cat_dist/rows
            if cat_dist_norm.shape[0] > 2:
                if cat_dist_norm.iloc[0] > 0.75:
                    cat_to_group1 = cat_dist_norm[0:1]
                    cat_to_group2 = cat_dist_norm[2:]
                else:
                    cat_to_group1 = cat_dist_norm.iloc[0: int(cat_dist_norm.shape[0]/2)].index.tolsit()
                    cat_to_group2 = cat_dist_norm.iloc[int(cat_dist_norm.shape[0]/2) :].index.tolist()
    
                 dt[feature] = dt[feature].replace(groups[0], 1)
                 dt[feature] = dt[feature].replace(groups[1], 0)

    yearmap = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7:2, 8: 3, 9:4, 10:4, 11: 4, 12: 4, 13:4,
          14:5, 15: 5}
    a = "avantgarde"
    m = "mainstream"
    nummapper = {a: 0, m: 1}
    movementmap = {1:m, 2:a, 3:m, 4:a, 5:m, 6:a, 7:a, 8:m, 9:a, 10:m, 11:a, 12:m,
                13:a, 14:m, 15:a}

    for cls_ in yearmap.keys():
        dt.PRAEGENDE_JUGENDJAHRE = dt.PRAEGENDE_JUGENDJAHRE.replace(cls_, yearmap[cls_])
    for cls_ in movementmap.keys():
        dt.PRAEGENDE_JUGENDJAHRE = dt.PRAEGENDE_JUGENDJAHRE.replace(cls_, nummapper[movementmap[cls_]])
    
    householdmap = {5: [11, 12, 13, 14, 15],
                4: [21,22,23,24,25],
                3: [31,32,33,34,35],
                2: [41,42,43,44,45],
                1: [51,52,53,54,55]}
    for newcls in householdmap.keys():
        dt.CAMEO_INTL_2015 = dt.CAMEO_INTL_2015.replace(householdmap[newcls],
                                                   [newcls]*5)

    lifestagemap = {0: [11, 21, 31, 41, 51],
                1: [12, 22, 32, 42, 52],
                2: [13, 23, 33, 43, 54],
                3: [14, 24, 34, 44, 54],
                4: [15, 25, 35, 45, 55]}
    for newcls in lifestagemap.keys():
    dt.CAMEO_INTL_2015 = dt.CAMEO_INTL_2015.replace(lifestagemap[newcls],
                                                   [newcls]*5)