"""
COVID-19 Model
"""

import mesa

from covid_19.scheduler import RandomActivationByTypeFiltered
from covid_19.agents import Person, Animal, Home, Visual

class COVID(mesa.Model):
    """
    COVID-19 Model
    """

    height = 20
    width = 20

    initial_persons = 100
    initial_animals = 50
    initial_homes = 10

    person_vaccination_rate = 0.05
    animal_vaccination_rate = 0.04

    person_gain_immunity_from_vaccine = 20

    home = False
    animal_gain_immunity_from_vaccine = 4

    person_immunity = 40
    animal_immunity = 15

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating covid - 19 modelling."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_persons=100,
        initial_animals=50,
        person_vaccination_rate=0.04,
        animal_vaccination_rate=0.05,
        person_gain_immunity_from_vaccine=20,
        person_immunity=20,
        animal_immunity=4,
        home=False,
        initial_homes=10,
        animal_gain_immunity_from_vaccine=4,
    ):
        """
        Create a new COVID - 19 model with the given parameters.

        Args:
            initial_persons: Number of humans to start with
            initial_animals: Number of animals to start with
            person_vaccination_rate: Probability of each person increasing immunity each step
            animal_vaccination_rate: Probability of each animal increasing immunity each step
            home: Whether the human entered home or not.
            person_immunity: immunity set for each person initially.
            animal_immunity: immunity set for each animal initially.
            person_gain_immunity_from_vaccine: immunity gained by person from vaccination
            animal_gain_immunity_from_vaccine: immunity gained by animal from vaccination
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_persons = initial_persons
        self.initial_animals = initial_animals
        self.initial_homes = initial_homes
        self.person_vaccination_rate = person_vaccination_rate
        self.animal_vaccination_rate = animal_vaccination_rate
        self.person_gain_immunity_from_vaccine = person_gain_immunity_from_vaccine
        self.home = home
        self.person_immunity = person_immunity
        self.animal_immunity = animal_immunity
        self.animal_gain_immunity_from_vaccine = animal_gain_immunity_from_vaccine

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        # infected 0, recovered 1, normal 2
        self.datacollector = mesa.DataCollector(
            {
                "Effected": lambda m: m.schedule.get_type_count(Person, Animal, 
                                                    lambda x: x.infected),
                "Recovered": lambda m: m.schedule.get_type_count(Person, Animal, 
                                                    lambda x: x.recovered),
                "Normal": lambda m: m.schedule.get_type_count(Person, Animal, 
                                                    lambda x: x.normal),
            }
        )

        # Create person:
        for i in range(self.initial_persons):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            mask = self.random.choice([True, False])
            age = self.random.randint(1, 100)
            immunity = self.random.randrange(2 * self.person_gain_immunity_from_vaccine)
            if i == 0:
                infected = True
            else:
                infected = False
            persons = Person(self.next_id(), (x, y), self, True, 
                             person_immunity, mask=mask, age=age,
                             immunity_gain=immunity, infected=infected, rate_of_vaccine=self.person_vaccination_rate)
            # if infected:
            #     print(f"infected person : {persons.infected} ====> {x,y}")
            self.grid.place_agent(persons, (x, y))
            self.schedule.add(persons)
        
        self.datacollector.collect(self)

        # Create animal
        for i in range(self.initial_animals):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            mask = self.random.choice([True, False])
            age = self.random.randint(1, 100)
            if i == 0:
                infected = True
            else:
                infected = False
            immunity = self.random.randrange(2 * self.animal_gain_immunity_from_vaccine)
            animal = Animal(self.next_id(), (x, y), self, True, 
                            animal_immunity,mask=mask,age=age,
                            immunity_gain=immunity, infected=infected, rate_of_vaccine=self.animal_vaccination_rate)
            # print(f"infected animal : {animal.infected}")
            self.grid.place_agent(animal, (x, y))
            self.schedule.add(animal)
        
        self.datacollector.collect(self)

        # Create home patches
        if self.home:
            # for agent, x, y in self.grid.coord_iter():

            #     home_model = Home(self.next_id(), (x, y), self)
            #     self.grid.place_agent(home_model, (x, y))
            #     self.schedule.add(home_model)
            for i in range(self.initial_homes):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                home_model = Home(self.next_id(), (x, y), self)
                self.grid.place_agent(home_model, (x, y))
                self.schedule.add(home_model)
            
            self.datacollector.collect(self)
        
        # used for coloring the cell, if no person infected in cell, its green, else if any one is infected,
        # it will be red.
        for agent, x, y in self.grid.coord_iter():
            # cellmates = self.grid.get_cell_list_contents([(x, y)])
            # print(f"Visual agent: {agent.infected}")
            is_infected = False
            for cell in agent:
                if type(cell) is Person: # check if person
                    if cell.infected:
                        is_infected = True
                    # print(f"==>Person:  {x,y}  ===> {cell.infected}")
                elif type(cell) is Animal: # check if animal
                    if cell.infected:
                        is_infected = True
                    # print(f"==>Animal:  {x,y}  ===> {cell.infected}")
            if is_infected:
                color = 1
                # print(f"===> infected : {x,y} ===> color : {color}")
            else:
                color = 0
            model = Visual(self.next_id(), (x,y), self, color=color)
            self.grid.place_agent(model, (x,y))
            self.schedule.add(model)
        
        self.datacollector.collect(self)
        # print("====> Agents Placed <========")

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        # print("===> Step function starts <===")
        self.schedule.step()

        # making the cells signaled to red, if any one in cell has infected with covid.
        for agent, x, y in self.grid.coord_iter():
            # cellmates = self.grid.get_cell_list_contents([(x, y)])
            is_infected = False
            for cell in agent:
                if type(cell) is Person: # check if person
                    # print(f"{x,y} ==> person ==> {cell.infected}")
                    if cell.infected:
                        is_infected = True
                elif type(cell) is Animal: # check if animal
                    # print(f"{x,y} ==> animal ==> {cell.infected}")
                    if cell.infected:
                        is_infected = True
                # print("============================================")
            
            for cell in agent:
                if type(cell) is Visual:
                    # print(f"{x,y} ==> Visual ==> {cell.color}")
                    if is_infected:
                        cell.color = 1
                    else:
                        cell.color = 0

        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(Person),
                    self.schedule.get_type_count(Animal),
                    self.schedule.get_type_count(Home),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number Persons: ", self.schedule.get_type_count(Person))
            print("Initial number Animals: ", self.schedule.get_type_count(Animal))
            print(
                "Initial number Homes: ",
                self.schedule.get_type_count(Home),
            )

        for i in range(step_count):
            self.step()
        

        if self.verbose:
            print("")
            print("Final number Persons: ", self.schedule.get_type_count(Person))
            print("Final number Animals: ", self.schedule.get_type_count(Animal))
            print(
                "Final number Home: ",
                self.schedule.get_type_count(Home),
            )