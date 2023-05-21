from typing import Type, Callable

import mesa


class RandomActivationByTypeFiltered(mesa.time.RandomActivationByType):
    """
    A scheduler that overrides the get_type_count method to allow for filtering
    of agents by a function before counting.

    Example:
    >>> scheduler = RandomActivationByTypeFiltered(model)
    >>> scheduler.get_type_count(AgentA, AgentB, lambda agent: agent.some_attribute > 10)
    """

    def get_type_count(
        self,
        type_class1: Type[mesa.Agent] = None,
        type_class2: Type[mesa.Agent] = None,
        filter_func: Callable[[mesa.Agent], bool] = None,
    ) -> int:
        """
        Returns the current number of agents of certain type in the queue that satisfy the filter function.
        """
        count = 0
        # persons
        if type_class1:
            for agent in self.agents_by_type[type_class1].values():
                if filter_func is None or filter_func(agent):
                    count += 1
        # Animals
        if type_class2:
            for agent in self.agents_by_type[type_class2].values():
                if filter_func is None or filter_func(agent):
                    count += 1
        # print(f"======>{y}=======>")

        return count
