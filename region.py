"""
Aidan Loten
12/10/2020
"""

class Region:
    """
    A region (represented by a list of long/lat coordinates) along with
    republican, democrat, and other vote counts.
    """

    def __init__(self, coords, r_votes, d_votes, o_votes):
        self.coordinates = coords
        self.republican_votes = r_votes
        self.democrat_votes = d_votes
        self.other_votes = o_votes

    def lats(self):
        "Return a list of the latitudes of all the coordinates in the region"
        result = []
        for coord in self.coordinates:
            result.append(coord[1])
        return result
        
            
    def longs(self):
        "Return a list of the longitudes of all the coordinates in the region"
        result = []
        for coord in self.coordinates:
            result.append(coord[0])
        return result

    def min_lat(self):
        "Return the minimum latitude of the region"
        return min(self.lats())

    def min_long(self):
        "Return the minimum longitude of the region"
        return min(self.longs())
    
    def max_lat(self):
        "Return the maximum latitude of the region"
        return max(self.lats())

    def max_long(self):
        "Return the maximum longitude of the region"
        return max(self.longs())

    def plurality(self):
        """return 'REPUBLICAN','DEMOCRAT', or 'OTHER'
        depending on plurality of votes"""
        plur = max(self.republican_votes, self.democrat_votes, self.other_votes)
        if plur == self.republican_votes:
            return 'REPUBLICAN'
        elif plur == self.democrat_votes:
            return 'DEMOCRAT'
        else:
            return 'OTHER'
    
    #def plurality_weight(self):
        #'''return the weight of a vote count of the plurality party based on a min of 64 votes and max of 2,652,072 votes in a region'''
        #if self.plurality() == "REPUBLICAN":
            #return int(self.republican_votes / (10000))
        #elif self.plurality() == "DEMOCRAT":
            #return int(self.democrat_votes / (10000))
        #else:
            #return int(self.other_votes / (10000))
        

    def total_votes(self):
        "The total number of votes cast in this region"
        return self.republican_votes + self.democrat_votes + self.other_votes

    def republican_percentage(self):
        "The percentage of republication votes cast in this region"
        return self.republican_votes / self.total_votes()

    def democrat_percentage(self):
        "The percentage of democrat votes cast in this region"
        return self.democrat_votes / self.total_votes()
        

    def other_percentage(self):
        "The percentage of other votes cast in this region"
        return self.other_votes / self.total_votes()
