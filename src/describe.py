from DataFrame import DataFrame

if __name__ == "__main__":
    try:
        df = DataFrame()
        df.read_csv("datasets/dataset_test.csv")
        df.print_describe()
    except Exception as e:
        print(e)
    # Pandas describe to compare
    # pd.set_option('display.max_columns', None)
    # pd_df = pd.read_csv('../datasets/dataset_test.csv')
    # print(pd_df.describe())
