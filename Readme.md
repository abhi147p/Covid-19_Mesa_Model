# COVID 19 Model (Tutorial)

## Summary

A simple model analysing the various analogical data analysis for covid 19. Consisting of 4 agents: Person, Animal, House, Visual. Here, Person is normal human being with both male, females and childrens. Animals is normal animals such as dog, cat, flies etc. House is normal homes, where a person or animals live. Visual is where it is used display the each cell as red(infected) and green(healthy). 

Here, If one person or animal comes in contact with other and if any one of them having covid, then the others might get effected based on certain conditions. 

Parameters:
 - title (text): Title of the model
 - home (boolean): if enabled, houses are available and isolation is possible.
 - initial_homes (decimal): initial number of homes available in particular stage.
 - initial_persons (decimal): initial number of humans
 - person_vaccination_rate (float): At what rate, vaccination is provided for persons
 - initial_animals (decimal): initial number of animals
 - animal_vaccination_rate (float): At what rate, vaccination is provided for animals
 - person_immunity (decimal): initial immunity for all the person agents
 - animal_immunity (decimal): initial immunity for all the animal agents
 - person_gain_immunity_from_vaccine (decinmal): The immunity gained or raised when a person agent is vaccinated
 - animal_gain_immunity_from_vaccine: The immunity gained or raised when a animal agent is vaccinated

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (PErson, Animal, Home, Visual)
 - Writing a model composed of multiple files.
 - Dynamically adding and moving agents from the schedule

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    # First, we clone the Mesa repo
    $ git clone https://github.com/projectmesa/mesa.git
    $ cd mesa
    # Then we cd to the example directory
    $ cd examples/wolf_sheep
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``covid-19/random_walk.py``: This defines the ``RandomWalker`` agent, which implements the behavior of moving randomly across a grid, one cell at a time. Both the Person and Animal agents will inherit from it.
* ``covid-19/agents.py``: Defines the Person, Animal, House and Visual agent classes.
* ``covid-19/scheduler.py``: Defines a custom variant on the RandomActivationByType scheduler, where we can define filters for the `get_type_count` function.
* ``covid-19/model.py``: Defines the COVID-19 Predation model itself
* ``covid-19/server.py``: Sets up the interactive visualization server
* ``run.py``: Launches a model visualization server.

## Further Reading

This model is closely based on the sample of Wolf-Sheep Model