import mesa

from covid_19.agents import Person, Animal, Home, Visual
from covid_19.model import COVID


def covid_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Person:
        # if agent.infected:
        #     portrayal["Color"] = "red"
        # if agent.recovered_from_covid or agent.normal:
        #     portrayal["Color"] = "green"
        portrayal["Shape"] = "covid_19/resources/person.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Animal:
        # if agent.infected:
        #     portrayal["Color"] = "red"
        # if agent.recovered_from_covid or agent.normal:
        #     portrayal["Color"] = "green"
        # portrayal["Filled"] = "true"
        portrayal["Shape"] = "covid_19/resources/animal.png"
        # https://icons8.com/icon/4823/exterior
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.immunity, 1)
        portrayal["text_color"] = "White"
        # portrayal["Color"] = "red"

    elif type(agent) is Home:
        # https://icons8.com/icons/set/household
        # portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        # portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "covid_19/resources/house.png"
        # portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["text_color"] = "White"
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    elif type(agent) is Visual:
        # print(f"===> agent color : {agent.color} <===")
        if agent.color == 1: # infected ["#00FF00", "#00CC00", "#009900"] ffcccb
            portrayal["Color"] = "#ffcccb" # red
        else: # no covid ["#84e184", "#adebad", "#d6f5d6"] 90EE90
            portrayal["Color"] = "#90EE90" # green

        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(covid_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Effected", "Color": "Red"},
        {"Label": "Normal", "Color": "Green"},
        {"Label": "Recovered", "Color": "Blue"}
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "home": mesa.visualization.Checkbox("House Enabled", True),
    "initial_homes": mesa.visualization.Slider("Initial number of houses", 20, 1, 50),
    "initial_persons": mesa.visualization.Slider(
        "Initial Person Population", 100, 10, 300
    ),
    "person_vaccination_rate": mesa.visualization.Slider(
        "Human Vaccination Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_animals": mesa.visualization.Slider("Initial Animal Population", 50, 10, 300),
    "animal_vaccination_rate": mesa.visualization.Slider(
        "Animal Vaccination Rate",
        0.05,
        0.01,
        1.0,
        0.01,
    ),
    "person_immunity": mesa.visualization.Slider("Initial person immunity", 50, 10, 300),
    "animal_immunity": mesa.visualization.Slider("Initial Animal immunity", 50, 10, 300),
    "person_gain_immunity_from_vaccine": mesa.visualization.Slider(
        "Person Gain Immunity From vaccine", 20, 1, 50
    ),
    "animal_gain_immunity_from_vaccine": mesa.visualization.Slider(
        "Animal Gain Immunity From vaccine", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    COVID, [canvas_element, chart_element], "COVID 19 Model", model_params
)
# server.port = 8521
