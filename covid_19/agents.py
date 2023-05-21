import mesa 
from covid_19.random_walk import RandomWalker



def is_object(self, obj):

    if type(self) is type(obj):
        return True
        
    return False

def process_Step_func(self):
    cellmates = self.model.grid.get_cell_list_contents([self.pos])

    is_Home = False
    is_infected = False
    living_lists = []
    for cell in cellmates:
        if type(cell) is Home:
            # print(f"type of obj: Home")
            is_Home = True
        elif type(cell) is Person:
            # print(f"type of obj: Person")
            living_lists.append(cell)
            # print("ok")

            if cell.infected:
                is_infected = True
        elif type(cell) is Animal:
            # print(f"type of obj: Animal")
            living_lists.append(cell)
            # print("ok animal")
            if cell.infected:
                is_infected = True
    
    # print(f"List of living one's: {living_lists}")
    # print(f"====> Home: {is_Home} is_infected: {is_infected} <-----")
    # print(f"=====>  is infected: {is_infected},  is_Home: {is_Home}<======")
    for cell in living_lists:
        # print(cell)
        if is_Home:
            cell.isolated = True
        
        # check if anyone is infected
        # print(f"isolated: {cell.isolated}")
        # print(f"infected: {cell.infected}")
        # print(f"immunity: {cell.immunity}")
        # print(type(cell.immunity))
        # print((cell.immunity - 50)//2)    
        # print(f" mask: {cell.mask}")
        # print(f"vaccine: {cell.vaccinated}")
        if is_infected and not cell.infected:
            # print("=============================")
            # print(f"immunity: {cell.immunity}")
            # print(type(cell.immunity))
            # print((cell.immunity - 50)//2)
            
            # print(f" mask: {cell.mask}")
            # print(f"vaccine: {cell.vaccinated}")
            # print(f"isolated: {cell.isolated}")
            # print(f"==> mask: {cell.mask}, vaccine: {cell.vaccinated}, isolated: {cell.isolated}")
            immunity_power_of_cell = ( cell.immunity - 50 )//2
            # print(f"immunity: {immunity_power_of_cell}")
            # print(f"==> mask: {cell.mask}, vaccine: {cell.vaccinated}, isolated: {cell.isolated}, immunity: {immunity_power_of_cell}")
            if cell.mask and cell.vaccinated and cell.isolated and (immunity_power_of_cell > 0):
                continue
            elif cell.mask and (immunity_power_of_cell > 0):
                continue
            elif cell.vaccinated and (immunity_power_of_cell > 0):
                continue
            elif cell.isolated and (immunity_power_of_cell > 0):
                continue
            else:
                cell.infected = True
                cell.normal = False

    # check if any person got vaccine
    rand_var = self.random.uniform(0.0, 1.0)
    # print(f"random: {rand_var}  vaccine rate: {self.vaccine_rate}")
    if rand_var < self.vaccine_rate:

        # provide the vaccine
        for cell in living_lists:
            # print(cell)
            cell.vaccinated = True
            if cell.infected:
                cell.mask = True
                cell.isolated = True
                cell.infected = False
                cell.recovered = True
            cell.immunity += cell.immunity_gain
        
    #     print(f"Updated the details successfully for {self.pos}")


class Person(RandomWalker):
    """
    A person that walks around, gets effected to covid and recovers. 

    The init is the same as the RandomWalker.
    """
    
    def __init__(self, unique_id, pos, model, moore, immunity=None,
                 vaccinated=False, infected=False, mask=False, isolated=False,
                 age=None, normal=True, recovered_from_covid=False, 
                 immunity_gain=None, rate_of_vaccine = None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.immunity = immunity
        self.vaccinated = vaccinated
        self.infected = infected
        self.mask = mask
        self.isolated = isolated
        self.age = age
        self.normal = normal
        self.recovered = recovered_from_covid
        self.immunity_gain = immunity_gain
        self.vaccine_rate = rate_of_vaccine
    
    def step(self):
        self.random_move()
        process_Step_func(self)
        

class Animal(RandomWalker):
    """
    A person that walks around, gets effected to covid and recovers. 

    The init is the same as the RandomWalker.
    """
    
    def __init__(self, unique_id, pos, model, moore, immunity=None,
                 vaccinated=False, infected=False, recovered_from_covid=False,
                 age=None,normal=True,immunity_gain=None, mask=False, rate_of_vaccine=None, isolated = False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.immunity = immunity
        self.vaccinated = vaccinated
        self.infected = infected
        self.recovered = recovered_from_covid
        self.age = age
        self.normal = normal
        self.immunity_gain = immunity_gain
        self.mask = mask
        self.vaccine_rate = rate_of_vaccine
        self.isolated = isolated

        # defining the immunity for each person according to their age
        if self.age <= 15: # kids
            self.immunity = self.immunity//2
        elif self.age <= 50: # youngsters and middle aged
            self.immunity = self.immunity + 1
        else: # old people
            self.immunity = self.immunity//3
    
    
    def step(self):
        self.random_move()
        process_Step_func(self)
        

class Home(RandomWalker):
    """
    A place of home where the persons meet
    """

    def __init__(self, unique_id, pos, model):
        """
        Creates a new place of home
        """
        super().__init__(unique_id, pos, model)

    def step(self):
        pass


class Visual(RandomWalker):
    """
    A place of home where the persons meet
    """

    def __init__(self, unique_id, pos, model, color):
        """
        Creates a new place of home
        """
        super().__init__(unique_id, pos, model)
        self.color = color

    def step(self):
        pass
