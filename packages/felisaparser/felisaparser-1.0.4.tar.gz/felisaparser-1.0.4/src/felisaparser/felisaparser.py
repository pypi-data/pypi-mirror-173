class parser:
    def __init__(self, path, sep=','):
        self.sep=sep
        self.path = path

    def excel_to_csv(self):
        try:
            import sys
            import pandas as pd
        except ImportError:
            print("pandas is not installed. Please install it and try again.")
            sys.exit(1)
        df = pd.read_excel(self.path)
        if self.path.endswith('.xlsx'):
            self.path = self.path[:-5]
        if self.path.endswith('.xls'):
            self.path = self.path[:-4]        
        df.to_csv(self.path + '.csv', index=False, sep=self.sep)