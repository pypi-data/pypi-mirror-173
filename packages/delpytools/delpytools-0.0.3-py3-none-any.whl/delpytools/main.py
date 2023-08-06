class PreProcessFunctions:
    """ 
    This class contains custom preprocess functions
    They can be used separately, but the main purpose of this is implementing 
    the class into the BinningProcess master-function defined below
    """
    def __init__(self,name):
        self.name = name

def ImputeMissingData(dataframe, ft_list, estimator = "ridge"):
    """ 
    The idea here is to inpute the missing values in an advanced way only for those
    features that we deem to have true missing data
    We will use the Iterative Imputer with ExtraTreesRegressor as the estimator for numerical
    features, as it tends to yield the best results; for categorical features, we will replace with
    the most frequent value.
    Features with 100% missing values must be cleaned before using this function
    The function expects float, int and obj inputs
    """
    from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.experimental import enable_iterative_imputer 
    from sklearn.impute import IterativeImputer, SimpleImputer
    import pandas as pd

    #estimators: 
    estimator_dict = {"ridge" : Ridge(),
                        "random_forest" : RandomForestRegressor(),
                        "extra_trees" : ExtraTreesRegressor()  
                        }

    
    #copy the data and select the features
    imputed_data = dataframe.copy(deep=True)
    imputed_data = imputed_data[ft_list]

    #delete columns with 100% missing values
    imputed_data = imputed_data[imputed_data.columns[imputed_data.isnull().mean()< 1 ]]

    #select numerical and categorical data
    num_data = imputed_data.select_dtypes(include='number')
    cat_data = imputed_data.select_dtypes(include='object') #account for string

    #initialize imputer
    num_imputer = IterativeImputer(estimator = estimator_dict[estimator], max_iter = 10)

    #transform
    num_data_imputed = num_imputer.fit_transform(num_data)
    num_data_imputed = pd.DataFrame(num_data_imputed, columns = num_data.columns)

    #account for categorical data
    if len(cat_data.columns) != 0:
        cat_imputer = SimpleImputer(strategy = "most_frequent")
        cat_data_imputed = cat_imputer.fit_transform(cat_data)
        cat_data_imputed = pd.DataFrame(cat_data_imputed, columns = cat_data.columns)
        final_imputed_data = pd.concat([num_data_imputed, cat_data_imputed], axis = 1)
        return final_imputed_data
    else:
        return num_data_imputed

        
    def check_gaussian_distribution(dataframe, feature, alpha = 0.05, print_details = False):
        """
        The purpose of this function is to check if a sample was drawn from a Gaussian distribution
        We use 3 tests which should increase the rigidity of our accepted conclusion
        The function can be called without print details, to only return a "Gaussian" or "Not Gaussian" string
        The 3 tests that we use are:
            - Shapiro-Wilk, which is a reliable test of normality, although there is some suggestion 
            that it may be suitable for smaller samples of data
            - D'Agostino's K^2 test calculated summary statistics (skewness and kurtosis) to determine if the distribution departs from a normal distribution
            - Anderson-Darling test is a modified version of the nonparametric goodness-of-fit statistical test Kolmogorov-Smirnov;
                a feature of this test is that it returns a list of critical values rather than a single p-value, which can provide the basis for more thorough interpretation of the results
        """

        #dependencies
        from scipy.stats import shapiro, normaltest, anderson
        import numpy as np
        
        data = dataframe[feature].values
        shapirostat, p = shapiro(data)
        k2stat, l = normaltest(data)
        adtest = anderson(data)
        adtest_sig_position = np.where(adtest.significance_level == alpha * 100)[0]
        adtest_critical_value = adtest.critical_values[adtest_sig_position][0]

        if print_details:
            print("🟢🟢🟢🟢 Normality Tests 🟢🟢🟢🟢")
            print("H0: variable follows a Gaussian distribution\nH1: variable does not follow a Gaussian distribution")
            print("----------------------------------\nShapiro Statistics = %.3f, p = %.3f" % (shapirostat, p))
            if p > alpha:
                print("Shapiro test: Sample appears to be drawn from a normal distribution (fail to reject H0)")
            else:
                print("Shapiro test: Sample does not look Gaussian (reject H0)")

            print("----------------------------------\nK^2 Statistics = %.3f, p = %.3f" % (k2stat, l))
            if l > alpha:
                print("K^2 test: Sample appears to be drawn from a normal distribution (fail to reject H0)")
            else:
                print("K^2 test: Sample does not look Gaussian (reject H0)")

            print("----------------------------------\nAnderson-Darling Statistics = %.3f\nCritical value: %.3f" % (adtest.statistic, adtest_critical_value))
            if adtest.statistic < adtest_critical_value:
                print("Sample appears to be drawn from a normal distribution (fail to reject H0)")
            else:
                print("Sample does not look normal (reject H0)")

            if((p>alpha) & (l>alpha) & (adtest.statistic < adtest_critical_value)):
                print("All of the normality tests conclude that the feature " + feature + " follows a normal Gaussian distribution")
            else:
                print("At least 1 of the normality tests conclude that the feature " + feature + " does not follow a normal Gaussian distribution")
        else:
            if((p>alpha) & (l>alpha) & (adtest.statistic < adtest_critical_value)):
                return "Gaussian"
            else:
                return "Not Gaussian"

    def cap_outliers(dataframe, plots = False):
        """
        This function will cap the outliers of the given dataframe (if they exist)
        Optional, if the feature number is low enough, it can plot the histogram and boxplot before and after capping
        Outlier detection is based on the distribution that the features' values have
        For normal distribution, data points which fall below mean-3*(sigma) or above mean+3*(sigma) are outliers
        For skewed distributions, data points which fall below Q1-1.5*IQR or above Q3+1.5*IQR are outliers
        """
        #dependencies
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np

        capped_df = dataframe.copy(deep = True)
        capped_df = capped_df.select_dtypes(include='number')
        counter = 0
        for ft in capped_df.columns:
            #check for normality
            normality_check = check_gaussian_distribution(capped_df, ft)
            if normality_check == "Not Gaussian":
                #calculate percentiles, IQR and upper/lower limits
                percentile25 = capped_df[ft].quantile(0.25)
                percentile75 = capped_df[ft].quantile(0.75)
                IQR = percentile75 - percentile25

                sd_upper_limit = percentile75 + 1.5 * IQR
                sd_lower_limit = percentile25 - 1.5 * IQR

                capped_df[ft] = np.where(capped_df[ft] > sd_upper_limit, sd_upper_limit,
                                        np.where(capped_df[ft] < sd_lower_limit, sd_lower_limit, capped_df[ft])
                                        )
            else:
                nd_upper_limit = capped_df[ft].mean() + 3*capped_df[ft].std()
                nd_lower_limit = capped_df[ft].mean() - 3*capped_df[ft].std()
                capped_df[ft] = np.where(capped_df[ft] > nd_upper_limit, nd_upper_limit,
                                        np.where(capped_df[ft] < nd_lower_limit, nd_lower_limit, capped_df[ft])
                                        ) 

            if plots:
                #original feature
                plt.figure(figsize = (15,8))
                plt.subplot(2,2,1)
                sns.distplot(dataframe[ft])
                plt.subplot(2,2,2)
                sns.boxplot(dataframe[ft])
                #feature with capped outliers
                plt.subplot(2,2,3)
                sns.distplot(capped_df[ft])
                plt.subplot(2,2,4)
                sns.boxplot(capped_df[ft])
            return capped_df

    def BinVariables(dataframe, ft_list, min_iv = 0.05):
        from optbinning import BinningProcess
        #copy the data and select the features
        imputed_data = dataframe.copy(deep=True)
        imputed_data = imputed_data[ft_list]
        #select numerical and categorical data
        num_data = imputed_data.select_dtypes(include='number')
        cat_data = imputed_data.select_dtypes(include='object')

        """Binning Continuous Variables"""

        # filter by inter-bin chiqsuare test p-value of 5% and min 2 bins per var
        bp_cont = BinningProcess(variable_names=num_data.columns.values,
                                max_pvalue=0.05,
                                min_n_bins=2)
        bp_res_cont = bp_cont.fit(num_data, y)
        bp_res_cont.summary().T

        # filter by min IV

        iv_filtered = []
        for var_ in num_data.columns:
            optb = bp_cont.get_binned_variable(var_)
            if optb.binning_table.iv>min_iv and len(optb.splits)>1:
                iv_filtered.append(var_)
                print(var_)
                print(optb.binning_table.analysis())
        print("IV filtering continuous leads to {} out of {} variables".format(len(iv_filtered),
                                                                            len(num_data.columns)))
        # re-fit cont binning only with filtered variables per above criteria
        num_data_filtered = num_data[iv_filtered].copy()

        bp_filter = BinningProcess(variable_names=iv_filtered,
                                max_pvalue=0.05)
        bp_res_cont_filtered = bp_filter.fit(num_data_filtered, y)
        bp_res_cont_filtered.summary().T

        # transform CONTINUOUS data
        num_data_transf = bp_res_cont_filtered.transform(num_data_filtered, metric='mean')

        """Binning Categorical Variables"""

        # filter by inter-bin chiqsuare test p-value of 5%, min 2 bins per var
        #  and min_prebin_size of 1% to address category imbalance
        bp_categ = BinningProcess(variable_names=cat_data.column.values,
                                max_pvalue=0.05,
                                categorical_variables=cat_data.columns,
                                min_prebin_size=0.01,
                                min_n_bins=2)
        bp_res_categ = bp_categ.fit(cat_data.values, y)
        bp_res_categ.summary().T

        # filter by min IV 
    
        iv_filtered = []
        for var_ in cat_data.columns:
            optb = bp_categ.get_binned_variable(var_)
            if optb.binning_table.iv>min_iv and len(optb.splits)>1:
                iv_filtered.append(var_)
                print(var_)
                print(optb.binning_table.analysis())
        print("IV filtering categorical leads to {} out of {} variables".format(len(iv_filtered),
                                                                                len(cat_data.columns)))

        # re-fit categ binning only with significant variables
        cat_data_filtered = cat_data[iv_filtered].copy()
        cat_data_filtered = cat_data_filtered.astype('category')

        bp_filter_categ = BinningProcess(variable_names=iv_filtered,
                                        max_pvalue=0.05,
                                        categorical_variables=iv_filtered,
                                        min_prebin_size=0.001)
        bp_res_categ_filtered = bp_filter_categ.fit(cat_data_filtered, y)
        bp_res_categ_filtered.summary().T

        # export results for each variable to excel
        writer = pd.ExcelWriter('categ_binning.xlsx', engine='xlsxwriter')
        for var_ in cat_data_filtered.columns:
            optb = bp_filter_categ.get_binned_variable(var_)        
            temp = optb.binning_table.build()
            temp.to_excel(writer, sheet_name=var_)
        writer.save()

        # transform CATEGORICAL data
        cat_data_transf = bp_res_categ_filtered.transform(cat_data_filtered, metric='indices')


        """ POOL TRANSFORMED DATA """
        pooled_data = pd.concat([num_data_transf, cat_data_transf], axis=1)

        return pooled_data
    def PCA(train, test, variance_kept = 0.8):
        """ 
        This functions applies principal components analysis
        The model will learn on the training set, then transform both the training and test sets
        The number of components is chosen so that they cumulatively explain 80% of the variance
        in the dataset (default value, can be changed in the parameters)
        The function expects only numeric values and the values should be standardized
        """
        from sklearn.decomposition import PCA

        #initialize the instance of the model
        pca = PCA(n_components = variance_kept)

        #fitting on training set

        pca.fit(train)

        #transforming both sets

        train = pca.transform(train)
        test = pca.transform(test)

        print(pca.explained_variance_ratio_)

        #turning results into dataframes and renaming the columns accordingly

        train_dataset = pd.DataFrame(train)
        test_dataset = pd.DataFrame(test)
        
        cols = []
        for i in train_dataset.columns:
            cols.append("Component " + str(i+1))

        train_dataset.columns = cols
        test_dataset.columns = cols

        return train_dataset, test_dataset





def preprocess(dataset, features = False, 
                eliminate_vars = True, miss_threshold = 0.9,
                normalize = False, standardize = False, cap_outliers = False,
                impute_missing_data = False, bin_variables = False, PCA = False):
    """ 
    Master function capable of preprocessing a dataset
    Use this function without the target variable.
    To only preprocess a subset of features,
    pass a list in the features parameter
    """
    #dependencies
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    from sklearn.decomposition import PCA
    #data copy
    try:
        df = dataset[features].copy(deep = True)
    except:
        df = dataset.copy(deep = True)

    #select numerical and categorical data
    num_df = df.select_dtypes(include='number')
    cat_df = df.select_dtypes(include='object') 


    #preprocess function initializer
    preprocessor = PreProcessFunctions

    #basic feature elimination based on percentage of missing values
    if eliminate_vars:
        num_df = num_df[num_df.columns[num_df.isnull().mean() <= miss_threshold]]

    #outlier capping based on the feature's distribution (normal or skewed)
    if cap_outliers:
        num_df = preprocessor.cap_outliers(num_df)

    #normalization
    norm_counter = 0
    if normalize:
        scaler = MinMaxScaler()
        num_df = pd.DataFrame(scaler.fit_transform(num_df))
        norm_counter += 1
        if cap_outliers == False:
            raise Warning("Normalization is subject to outliers, it is recommended you deal with outliers before this step")

    #standardization
    std_counter = 0
    if standardize:
        if norm_counter == 1:
            raise ValueError("Data was already normalized (scaled)")
        else:
            stdscaler = StandardScaler()
            num_df = pd.DataFrame(stdscaler.fit_transform(num_df))
            std_counter +=1

    #below are the functions that work both on categorical and numerical measures
    df = pd.concat([num_df, cat_df], axis = 1)
    
    #imputing missing data
    if impute_missing_data:
        df = preprocessor.ImputeMissingData(df, ft_list = df.columns)

    #bin variables
    if bin_variables:
        df = preprocessor.BinVariables(df)


    return df
