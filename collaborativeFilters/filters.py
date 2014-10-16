import sys
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from math import sqrt

DEBUG = True

# abstract base class - must be extended by all
# types of collaborative filter classes
class CollaborativeFilter(metaclass=ABCMeta):
    @abstractmethod
    def readTrainingData(self, data_file):
        with open(data_file, "r") as f:
            tr_data = [line.strip().split("\t") for line in f]
        return tr_data

    @abstractmethod
    def readTestData(self, data_file):
        with open(data_file, "r") as f:
            tr_data = [line.strip().split("\t") for line in f]
        return tr_data

    @abstractmethod
    def calculate(self):
        pass



class Average(CollaborativeFilter):
    """Collaborative filter based on users' average ratings. By definition,
     is independent of user's identity.
    """

    training_data = None
    test_data = None    

    
    def readTrainingData(self, data):
        self.training_data = super(Average, self).readTrainingData(data)
        flat_list = ([int(x) for x in [i for row in self.training_data for i in row]])
        users = flat_list[0::4]
        ratings = flat_list[2::4]
        z = zip(users, ratings)
        users_to_ratings = defaultdict(list)
        for k, v in z:
            users_to_ratings[k].append(v)
       
        self.training_data = users_to_ratings
                

    def readTestData(self, data):
        self.test_data = super(Average, self).readTrainingData(data)
        flat_list = ([int(x) for x in [i for row in self.test_data for i in row]])
        users = flat_list[0::4]
        ratings = flat_list[2::4]
        z = zip(users, ratings)
        users_to_ratings = defaultdict(list)
        for k, v in z:
            users_to_ratings[k].append(v)

        self.test_data = users_to_ratings
        
    def calculateError(self):
        return RSME(self.training_data, self.test_data)

    def calculate():
        pass
        
        


class UserEucledian(CollaborativeFilter):

    training_data = None

    def readTrainingData(self, data):
        self.training_data = super(UserEucledian, self).readTrainingData(data)

        user_col = 0
        item_col = 1
        rating_col = 2
        timestamp_col = 3

        # loop through all combinations of 2 users, not matching a user with himself
        first_user_idx = 0
        sum_diff_sq_user = 0
        for first_user in self.training_data:
            # sum of squared differences in rating for first_user, second_user
            
            second_user_idx = 0
            sum_diff_sq_item = 0
            for second_user in self.training_data:
                # true if the user is not himself, and he rated the same item as the second user                
                if self.training_data[first_user_idx][user_col] != self.training_data[second_user_idx][user_col] and self.training_data[first_user_idx][item_col] == self.training_data[second_user_idx][item_col]:
                    # the squared difference between first_user and second_user's rating for the same item
                    diff_sq = (int(self.training_data[first_user_idx][rating_col]) - int(self.training_data[second_user_idx][rating_col])) ** 2
                    sum_diff_sq_item += diff_sq                    
                    if(DEBUG):
                        print("User: ", self.training_data[first_user_idx][user_col], " Item: ", self.training_data[first_user_idx][item_col], " Rating:", self.training_data[first_user_idx][rating_col], "\n", "User:", self.training_data[second_user_idx][user_col], " Item: ", self.training_data[second_user_idx][item_col], " Rating:", self.training_data[second_user_idx][rating_col], "Difference^2: ", str(diff_sq))
                second_user_idx += 1  
            print(sum_diff_sq_item)
            sum_diff_sq_user += sum_diff_sq_item

            first_user_idx += 1
        


    def readTestData(self, tr_data):
        pass
    def run():
        pass
    def calculate():
        pass



class UserPearson(CollaborativeFilter):
    def readTrainingData(self, tr_data):
        print("in child")
    def readTestData(self, tr_data):
        pass
    def calculate():
        pass


class ItemCosine(CollaborativeFilter):
    training_data = None
    cosine_similarities = {}

    def readTrainingData(self, data):
        self.training_data = super(ItemCosine, self).readTrainingData(data)
        
        user_col = 0
        item_col = 1
        rating_col = 2
        timestamp_col = 3

        items = [row[item_col] for row in self.training_data] 
        ratings = [row[rating_col] for row in self.training_data] 
        item_to_ratings = defaultdict(list)

        z = zip(items, ratings)

        for k, v in z:
            item_to_ratings[k].append(v)        

        item_pairs_to_ratings = {}
        for item1 in item_to_ratings.items():
            for item2 in item_to_ratings.items():
                item_pairs_to_ratings[item1[0], item2[0]] = [None]
                # don't compare the same item
                if(item1[0] != item2[0]):
                    print("one", item1, "two", item2)
                    item_pairs_to_ratings[item1[0], item2[0]] = [item1[1], item2[1]]
                    
        
        for k, v in item_pairs_to_ratings.items():
            if(k[0] != None and v[0] != None and k[1] != None and v[1] != None and len(v[0]) == len(v[1])):
                dot_prod = self.dotProduct(v[0], v[1])
                mag_vec0 = self.vecMagnitude(v[0])
                mag_vec1 = self.vecMagnitude(v[1])
                cosine_similarity = dot_prod/(mag_vec0 * mag_vec1)
                key_table = [k[0][0]]
                key_table.append(k[1][0])

                # convert to tuple so it can be hashed & used as dict key
                key_tuple = tuple(key_table)
                               
                self.cosine_similarities[key_tuple] = cosine_similarity

                if(DEBUG):
                    print("\nItems: ", k[0], k[1])
                    print("Dot product of ", v[0], " and ", v[1], " = ", dot_prod)
                    print("vec1 magnitude: ", mag_vec0)
                    print("vec2 magnitude: ", mag_vec1)
                    print("Cosine Similarity: ", cosine_similarity)

    def dotProduct(self, vec1, vec2):
        if len(vec1) != len(vec2):
            print("ERROR - vector length mismatch")
        else:
            z = zip(vec1, vec2)
            dot_prod = 0
            for k in z:
                dot_prod += int(k[0]) * int(k[1]) 
            return dot_prod    

    def vecMagnitude(self, vec):
        mag = 0
        for i in vec:
            mag += int(i) ** 2
        return sqrt(mag)
    
    def showCosineSimilarities(self):
        print("\nCOSINE SIMILARITIES:")
        for k in self.cosine_similarities:
            print(k, self.cosine_similarities[k])

    def readTestData(self, tr_data):
        pass
    def calculate():
        pass

class ItemAdjustedCosine(CollaborativeFilter):
    def readTrainingData(self, tr_data):
        print("in child")
    def readTestData(self, tr_data):
        pass
    def calculate():
        pass


class SlopeOne(CollaborativeFilter):
    def readTrainingData(self, tr_data):
        print("in child")
    def readTestData(self, tr_data):
        pass
    def calculate():
        pass

def RSME(training_data, test_data):
    sum_squared_dif = 0
    num_obvs = 0

    for k_training, v_training in training_data.items():
        for k_test, v_test in test_data.items():
            if(k_training == k_test):
                for rating_training, rating_test in zip(v_training, v_test):
                    sum_squared_dif += (rating_training - rating_test) ** 2
                    num_obvs += 1

    rmse = sqrt(sum_squared_dif/num_obvs)
    return rmse
                
        
             
    pass