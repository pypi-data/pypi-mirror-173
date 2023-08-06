class BitcoinTrading:
  """This class load two files from filesystem from input_data directory (user data and transaction data), modify it, join and save a result in client_data directory""" 

  def file_info_logging(self, val):  
    self.logger.info( val )

  def file_warning_logging(self, val):  
    self.logger.warning( val )

  def file_error_logging(self, val):  
    self.logger.error( val )

  def check_parameters(self):
    """Function validate if we are running code with proper number of attributes
    Proper parameter for running purpose is:
    BitcoinTrading.py <users_input_file> <transactions_input_file> <country_filter>
    """
    if len(self.params) in (4,5):
     # File location and type
     self.file_info_logging('BitcoinTrading.check_parameters: Validating input parameters')
     self.file_users_location = """input_data/""" + str(self.params[1])
     self.file_transactions_location = """input_data/""" + str(self.params[2])
     self.countries = str(self.params[3])
     if len(self.params) == 5:
       self.file_output = """client_data/""" + str(self.params[4]) + '.csv'
     else:
       self.file_output = """client_data/output_data"""
       from datetime import datetime
       now = datetime.now()
       self.file_output = self.file_output +'_' + now.strftime("%d-%m-%Y_%H%M%S") + '.csv' 
       self.file_info_logging('BitcoinTrading.check_parameters: Parameters correctly parsed')
    else:
     self.logger.error('Incorrect input parameters')
     self.logger.error('usage: python3 BitcoinTrading.py <users_input> <transactions_input> <country>')
     print("usage: python3 BitcoinTrading.py <users_input> <transactions_input> <country>")
     exit(0)
    # return file_users_location, file_transactions_location, countries, file_output
  
  def log_initialize(self):
    import logging
    import time
    from logging.handlers import RotatingFileHandler
  
    log_handler = logging.handlers.RotatingFileHandler(filename='BitcoinTrading.log', mode='a', maxBytes=10**3*3, backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s BitcoinTrading [%(process)d]: [%(levelname)s] %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger("BitcoinTrading rotating Log")
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    #return logger
    self.logger = logger

  def dataset_filtering(self, condition):
    self.file_info_logging('BitcoinTrading.dataset_filtering: Output filtered by: ' + condition)
    self.df_users = self.df_users.filter(condition)
    
  def column_remove(self, column_name):
    self.file_info_logging("Remove column from dataset: " + column_name)
    self.df_users = self.df_users.drop(column_name)

  def column_remove_tr(self, column_name):
    self.file_info_logging("Remove column from dataset: " + column_name)
    self.df_transactions = self.df_transactions.drop(column_name)    
    
  def column_rename(self, old_column_name, new_column_name):
    self.file_info_logging("Rename column in dataset: " + old_column_name + ' to ' + new_column_name)
    self.df_users = self.df_users.withColumnRenamed(old_column_name, new_column_name)
  
  def column_create(self, column_name, column_value):
    self.file_info_logging("Create column in dataset: " + column_name + ' as  ' + column_value)
    self.df_users = self.df_users.withColumn(column_name, column_value)
    
  def dataset_join(self):
    self.file_info_logging("Join two datasets")
    self.df_join = self.df_users.join(self.df_transactions, self.df_users.client_identifier== self.df_transactions.id, "inner")
  
  def generate_output(self):
    from pyspark.sql.functions import col
    self.file_info_logging("Generate output")
    self.df_output = self.df_join.select("New name", "client_identifier",col("btc_a").alias("bitcoin_address"),col("cc_t").alias("credit_card_type"))

  def write_output(self):
    try:
     self.file_info_logging("Traying to save a file into filesystem")
     self.df_output.write.format("csv").mode("overwrite").option("header", "true").save(self.file_output)
     self.file_info_logging('File ' + self.file_output + " saved in filesystem with " + str(self.df_output.count()) + ' row(s)')
    except Exception as e:
     print(e)
     self.file_error_logging('Problem during saving ' + self.file_output + " file" )

  def load_file(self, file_name, level):
    file_type = "csv"
    infer_schema = "false"
    first_row_is_header = "true"
    delimiter = ","
    
    self.file_info_logging("Loading file: "+ file_name)
    
    
    
    if level == 0: #users
      try: 
        self.df_users = self.sparkSess.read.format(file_type) \
        .option("inferSchema", infer_schema) \
        .option("header", first_row_is_header) \
        .option("sep", delimiter) \
        .load(file_name)
        self.file_info_logging('Loaded ' + str(self.df_users.count()) + ' users')
      except:
        self.file_warning_logging('File ' + file_name + " doesn't exists")
        print('File ' + file_name + " doesn't exists")
        exit(0)
    elif level == 1: #transaction
      try: 
        self.df_transactions = self.sparkSess.read.format(file_type) \
        .option("inferSchema", infer_schema) \
        .option("header", first_row_is_header) \
        .option("sep", delimiter) \
        .load(file_name)
        self.file_info_logging('Loaded ' + str(self.df_transactions.count()) + ' users')
      except:
        self.file_warning_logging('File ' + file_name + " doesn't exists")
        print('File ' + file_name + " doesn't exists")
        exit(0) 
   
  def __init__(self) -> None:
    print("INIT")
    import sys
    from pyspark.sql.functions import concat, col, lit
    from pyspark.sql import SparkSession
    self.params = sys.argv
    self.log_initialize()
    self.sparkSess = SparkSession.builder.appName("InitializeBitcoinTradingSparkSession ").getOrCreate()