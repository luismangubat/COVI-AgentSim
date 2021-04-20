import simpy
from store0 import model
import numpy as np
from numpy.random import default_rng
import mlflow

class Store0:
    """Models a local-level location for use by the global-level agent-based model"""

    people_list = []  # People will get added to this list instead of the usual way they are processed for other locations
    history_queue = []  # We will keep a history of the output from the model
    model = None  # The pretrained model
    rng = None

    INTERVAL = 10e4  # Same inverval used in preparing the training data
    TIMESERIES = 9
    FEATURES = 1
    BATCH_SIZE = 1
    INITIAL_VIRAL_LOAD = 0.5
    SEED = 9

    def __init__(self, env=None):
        self.env = env  # Allows us to put the store on the simpy event queue
        self.model = model.load()
        self.rng = default_rng()
        self.history_queue = np.zeros(self.TIMESERIES).reshape(self.TIMESERIES, self.FEATURES)  # For the first call to the model will send all zeros
        self.seed = 0

    def add(self, person):
        self.people_list.append(person)

    def pulse(self):
        """Call this method to put a local-level event on the gobal-level event queue"""
        while True: # This event will run at regular intervals
            yield self.env.timeout(self.INTERVAL)  # Wait ...
            # ... at the end of the interval
            tot = sum([p.is_infectious for p in self.people_list])
            mlflow.log_metric('store0_init_sum_is_infectious', tot)  # From ABM

            # Seed input to local model from global model
            if self.seed < self.SEED:
                self.save(np.array([tot]).reshape(1, 1))
                self.seed += 1
            else:
                y_nd = self.predict()  # Get a prediction of the number of infected people leaving the location
                y_int = round(y_nd.reshape(1, )[0])
                infected_people_list = self.sample(y_int)  # Randomly select which people should get infected
                self.update(infected_people_list) # Update their state
                #self.save(y_nd)  # Save this for input to the model next iteration
                self.save(np.array([tot]).reshape(1, 1)) # What if we always used the incoming population for prediction
                mlflow.log_metric('store0_prediction', y_int) # For validation
            self.people_list = [] # Get ready for next iteration


    def sample(self, number_of_infected):
       """Given a the number of infected people leaving the store, sample this number of people"""
       if number_of_infected >= len(self.people_list):
           return self.people_list
       return self.rng.choice(self.people_list, size=number_of_infected, replace=False)

    def update(self, people_list, status=True):
        """Update the infectious state of these people"""

        # Reset everyone's infection status first
        for person in self.people_list:
            person.ts_covid19_immunity = float('inf')
            person.ts_death = float('inf')
            person.ts_covid19_infection = float('inf')

        for person in people_list:
            person._get_infected(self.INITIAL_VIRAL_LOAD)
            person.is_infectious = True
            #person.infection_timestamp = self.env.timestamp



    def save(self, feature_vector):
        """Save a feature vector to the history sequence of this location and truncate history"""
        self.history_queue = np.append(self.history_queue[:-1], feature_vector, axis=0)

    def predict(self):
        """Get the predicted number of infected people leaving the store from the pretrained model."""
        predictors = self.history_queue # We will use the history of output from the model for now
        predictors = predictors.reshape(self.BATCH_SIZE, -1, self.FEATURES)
        return self.model(predictors).numpy()

