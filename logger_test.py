import unittest
import os
from datetime import datetime
from logger import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing purposes
        self.test_file = 'test_log.txt'
        self.logger = Logger(self.test_file)

    def tearDown(self):
        # Clean up the temporary test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_metadata(self):
        # Test that the metadata is written correctly
        pop_size = 100
        vacc_percentage = 0.2
        virus_name = "Flu"
        mortality_rate = 0.05
        repro_rate = 2.5
        initial_infected = 5

        # Write metadata
        self.logger.write_metadata(pop_size, vacc_percentage, virus_name, mortality_rate, repro_rate, initial_infected)

        # Read the file and check if metadata is written
        with open(self.test_file, 'r') as file:
            content = file.read()

        self.assertIn(f'Virus: {virus_name}', content)
        self.assertIn(f'Population Size: {pop_size}', content)
        self.assertIn(f'Initial Vaccinated Population: {vacc_percentage * 100}%', content)
        self.assertIn(f'Initial Infected Population: {initial_infected}', content)
        self.assertIn(f'Mortality Rate: {mortality_rate}', content)
        self.assertIn(f'Reproductive Rate: {repro_rate}', content)

    def test_log_interactions(self):
        # Test that interaction logs are written correctly
        step_number = 1
        number_of_interactions = 50
        number_of_new_infections = 10

        # Log interactions
        self.logger.log_interactions(step_number, number_of_interactions, number_of_new_infections)

        # Read the file and check if interaction logs are written
        with open(self.test_file, 'r') as file:
            content = file.read()

        self.assertIn(f'Number Interactions: {number_of_interactions}', content)
        self.assertIn(f'New Infections: {number_of_new_infections}', content)

    def test_log_infection_survival(self):
        # Test that infection survival logs are written correctly
        step_number = 2
        population_count = 100
        number_of_new_fatalities = 5

        # Log infection survival
        self.logger.log_infection_survival(step_number, population_count, number_of_new_fatalities)

        # Read the file and check if infection survival logs are written
        with open(self.test_file, 'r') as file:
            content = file.read()

        self.assertIn(f'Total Population: {population_count}', content)
        self.assertIn(f'New Fatalities: {number_of_new_fatalities}', content)

    def test_log_time_step(self):
        # Test that time step logs are written correctly
        infected_and_alive = 50
        total_deaths = 20
        total_interactions = 100
        step = 3
        pop_size = 100

        # Log time step
        self.logger.log_time_step(infected_and_alive, total_deaths, total_interactions, step, pop_size)

        # Read the file and check if time step logs are written
        with open(self.test_file, 'r') as file:
            content = file.read()

        self.assertIn(f'Infected: {infected_and_alive}', content)
        self.assertIn(f'Total Deaths: {total_deaths}', content)
        self.assertIn(f'Total Interactions: {total_interactions}', content)

    def test_log_simulation_outcome(self):
        # Test that simulation outcome logs are written correctly
        simulation_time_step = 10
        pop_size = 100
        total_deaths = 20

        # Log simulation outcome
        self.logger.log_simulation_outcome(simulation_time_step, pop_size, total_deaths)

        # Read the file and check if simulation outcome logs are written
        with open(self.test_file, 'r') as file:
            content = file.read()

        self.assertIn(f'The simulation has ended after {simulation_time_step} iterations', content)
        self.assertIn(f'Initial Population: {pop_size}', content)
        self.assertIn(f'Total Deaths: {total_deaths}', content)
        self.assertIn(f'Surviving Population: {pop_size - total_deaths}', content)
        self.assertIn(f'Calculated Mortality Rate: {total_deaths / pop_size}', content)

if __name__ == '__main__':
    unittest.main()
