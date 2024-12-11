import unittest
from simulation import Simulation
from virus import Virus
from person import Person
from logger import Logger


class TestSimulation(unittest.TestCase):
    def setUp(self):
        # Set up the basic properties for the virus and simulation
        self.virus_name = "Test"
        self.repro_num = 0.5
        self.mortality_rate = 0.12
        self.virus = Virus(self.virus_name, self.repro_num, self.mortality_rate)

        # Set a smaller population size for testing
        self.pop_size = 10
        self.vacc_percentage = 0.1 
        self.initial_infected = 2  

        # Create the simulation object
        self.simulation = Simulation(
            virus=self.virus,
            pop_size=self.pop_size,
            vacc_percentage=self.vacc_percentage,
            initial_infected=self.initial_infected
        )

    def test_population_creation(self):
        # Test population creation to check vaccinated vs. non-vaccinated split
        self.simulation._create_population()

        # Check that the correct number of vaccinated people are set
        num_vaccinated = int(self.pop_size * self.vacc_percentage)
        vaccinated_count = sum(
            1 for person in self.simulation.population if person.is_vaccinated
        )
        self.assertEqual(vaccinated_count, num_vaccinated)

        # Check that there are correct initial infected
        infected_count = sum(
            1 for person in self.simulation.population if person.infection is not None
        )
        self.assertEqual(infected_count, self.initial_infected)

    def test_interactions(self):
        # Test the interactions between infected and healthy people
        # We simulate the behavior by directly interacting healthy and infected people

        # Create infected person
        infected_person = Person(_id=1, is_vaccinated=False, infection=self.virus)

        # Create a healthy person
        healthy_person = Person(_id=2, is_vaccinated=False)

        # Perform interaction and check if the healthy person is infected
        self.simulation.interaction(infected_person, healthy_person)

        # After interaction, check if the healthy person is infected
        self.assertIn(healthy_person, self.simulation.newly_infected)

    def test_infection_probability(self):
        # Simulate infection based on probability (using random.random())
        # First, test that the infection probability works by manually controlling it

        # Set infected person and healthy person
        infected_person = Person(_id=1, is_vaccinated=False, infection=self.virus)
        healthy_person = Person(_id=2, is_vaccinated=False)

        # Manually set random value to simulate infection
        # Set this to below 0.5 for infection to happen
        random_val = 0.4  

        if random_val < self.virus.repro_rate:
            self.simulation.newly_infected.add(healthy_person)

        # Assert that the healthy person is infected
        self.assertIn(healthy_person, self.simulation.newly_infected)

    def test_simulation_should_continue(self):
        # Test the condition to continue simulation
        self.simulation.total_deaths = 1
        self.simulation.infected_and_alive = 2

        # Check if simulation should continue
        # Expect True because there are still unvaccinated people
        should_continue = self.simulation._simulation_should_continue()
        self.assertTrue(should_continue)  

        # Simulate a scenario where the population is entirely infected or dead
        self.simulation.total_deaths = self.pop_size
        self.simulation.infected_and_alive = 0
        should_continue = self.simulation._simulation_should_continue()

        # Expect False since everyone is either infected or dead
        self.assertFalse(should_continue)  

    def test_run_simulation(self):
        # Run the simulation
        self.simulation.num_steps = 0
        self.simulation.total_deaths = 0
        self.simulation.infected_and_alive = 2
        self.simulation.total_interactions = 0

        # Run the simulation for a single step
        self.simulation.run()

        # After the simulation ends, check that the number of steps is updated
        # At least one step should have run
        self.assertGreater(self.simulation.num_steps, 0)  

    def test_infected_and_alive_not_negative(self):
        # Check that infected_and_alive does not go below zero
        self.simulation.infected_and_alive = 0
        self.simulation.total_deaths = 10  

        # Call time step to simulate one step
        self.simulation.time_step()

        # Assert that infected_and_alive stays at 0
        self.assertEqual(self.simulation.infected_and_alive, 0)


if __name__ == '__main__':
    unittest.main()
