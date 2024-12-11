from datetime import datetime

class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name

    # The methods below are just suggestions. You can rearrange these or 
    # rewrite them to better suit your code style. 
    # What is important is that you log the following information from the simulation:
    # Meta data: This shows the starting situtation including:
    #   population, initial infected, the virus, and the initial vaccinated.
    # Log interactions. At each step there will be a number of interaction
    # You should log:
    #   The number of interactions, the number of new infections that occured
    # You should log the results of each step. This should inlcude: 
    #   The population size, the number of living, the number of dead, and the number 
    #   of vaccinated people at that step. 
    # When the simulation concludes you should log the results of the simulation. 
    # This should include: 
    #   The population size, the number of living, the number of dead, the number 
    #   of vaccinated, and the number of steps to reach the end of the simulation. 

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       repro_rate, initial_infected):
        current_date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        meta_data = (
            f'- - - - - - - {virus_name} Simulation - - - - - - - \n\n'
            f'Simulation Date: {current_date}\n'
            f'Virus: {virus_name}\n'
            f'Population Size: {pop_size}\n'
            f'Initial Vaccinated Population: {vacc_percentage * 100}%\n'
            f'Initial Infected Population: {initial_infected}\n'
            f'Mortality Rate: {mortality_rate}\n'
            f'Reproductive Rate: {repro_rate}\n'
            f' - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n'
        )

        with open(self.file_name, 'w') as file:
            file.write(meta_data)

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        interactions = (
            f'- - - INTERACTIONS - STEP NUMBER {step_number} - - -\n'
            f'Number Interactions: {number_of_interactions}\n'
            f'New Infections: {number_of_new_infections}\n\n'
        )

        with open(self.file_name, 'a') as file:
            file.write(interactions)


    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        survival = (
            f'- - INFECTION SURVIVAL - STEP NUMBER {step_number} - -\n'
            f'Total Population: {population_count}\n'
            f'New Fatalities: {number_of_new_fatalities}\n\n'
        )

        with open(self.file_name, 'a') as file:
            file.write(survival)


    def log_time_step(self, infected_and_alive, total_deaths, total_interactions, step, pop_size):
        '''
            infected_and_alive can never be negative because at the end of the simulation those people with either be vaccinated/immune or dead
        '''
        adjusted_infected_and_alive = max(0, infected_and_alive)
        time_step = (
            f'- - - - - - - - STEP NUMBER {step} - - - - - - - -\n\n'
            f'Infected: {adjusted_infected_and_alive}\n'
            f'Vaccinated or Immune: {pop_size - total_deaths - adjusted_infected_and_alive}\n'
            f'Total Deaths: {total_deaths}\n'
            f'Total Interactions: {total_interactions}\n\n'
        )

        with open(self.file_name, 'a') as file:
            file.write(time_step)
        

    def log_simulation_outcome(self, simulation_time_step, pop_size, total_deaths, saved_by_vax):
        simulation_end_reason = ''
        if pop_size == total_deaths:
            simulation_end_reason = 'Entire population is dead'
        else:
            simulation_end_reason = 'Entire population is either vaccinated or immune'

        summary = (
            f'- - - - - - - - SIMULATION OUTCOME - - - - - - - -\n\n'
            f'The simulation has ended after {simulation_time_step} iterations\n'
            f'**************************************************\n'
            f'{simulation_end_reason}\n'
            f'**************************************************\n'
            f'Initial Population: {pop_size}\n'
            f'Total Deaths: {total_deaths}\n'
            f'Surviving Population: {pop_size - total_deaths}\n'
            f'Interactions Saved by Vaccination: {saved_by_vax}\n'
            f'Calculated Mortality Rate: {total_deaths / pop_size}'
        )

        with open(self.file_name, 'a') as file:
            file.write(summary)