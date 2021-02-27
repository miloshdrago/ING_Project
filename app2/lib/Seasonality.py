# Import dependencies
import numpy as np
import pandas as pd


class Seasonality(object):
    """ Seasonality adjust the maximum transaction rate according to a specified .csv
    file containing a scaler for certain time stamps
    """

    def __init__(self, seasonality_file, enviroment=None):
        self.seasonality_file = seasonality_file
        self.env = enviroment

        # Import seasonality .csv file
        self.seasonality_df = pd.read_csv(self.seasonality_file, sep=";")

        # Find highest time value in seasonality seasonality_dataframe
        self.max_time_seasonality = max(self.seasonality_df["time"].values)

    def scale(self, timestamp=None):
        """ Return scalar to adjust amount of messages, use timestamp if given,
        otherwise call envoirment to determine current time
        """

        # If no timestamp is given, use Simpy envoirment to get time
        if timestamp is None:
            if self.env is None:
                raise BaseException("No timestamp or envoirment specified")
            timestamp = self.env.now

        # Loop if timestamp is larger than max seasonality time
        timestamp = timestamp % self.max_time_seasonality
        # Find time value closest to timestamp
        closest_time = abs(self.seasonality_df["time"]-timestamp).values.argmin()
        # Return scaler value correspoding to closest_time
        return self.seasonality_df["scaler_value"][closest_time]


class TransactionInterval(Seasonality):
    """
    TransactionInterval uses a specified seasonality to generate a time
    interval between two transactions.
    """

    def __init__(self, seasonality_file, enviroment=None, max_volume=None):
        Seasonality.__init__(self, seasonality_file, enviroment)
        self.max_vol = max_volume

    def interval(self, timestamp=None):
        if self.max_vol is None:
            raise BaseException("No Maximum volume given")
        # Generate a random expected volume given a seasonality and maximum volume
        random_volume = np.random.gamma(self.scale(timestamp) * self.max_vol, 1)
        # Create a time interval by dividing a time unit (second) by the volume
        time_interval = 1/random_volume
        return time_interval
