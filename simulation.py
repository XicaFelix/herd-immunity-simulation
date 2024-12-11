import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        
        # TODO: Store the virus in an attribute
        # TODO: Store pop_size in an attribute
        # TODO: Store the vacc_percentage in a variable
        # TODO: Store initial_infected in a variable
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not. 
        # Use the _create_population() method to create the list and 
        # return it storing it in an attribute here. 
        # TODO: Call self._create_population() and pass in the correct parameters.

        self.logger = Logger('answers.txt')
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        # self.total_vaccinated = int(self.pop_size * self.vacc_percentage)
        self.total_infected = 0 # Int
        self.total_deaths = 0 # Int
        self.population = self._create_population(self.initial_infected) # List of Person objects
        self.file_name = f"{self.virus.name}_simulation_pop_{self.pop_size}_vacc_pcnt_{self.vacc_percentage}"
        self.newly_infected = []
        self.dead_population = [] # tip
        self.simulation_end_reason = ''
        self.num_interactions = 0
        self.vaccine_interactions = 0
        self.death_interactions = 0

    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people

        # Determine who will be vaccinated
        vaccinated_indices = set(random.sample(range(self.pop_size), int(self.pop_size * self.vacc_percentage)))

        population = [
            Person(i, is_vaccinated=(i in vaccinated_indices)) if i >= self.initial_infected
            else Person(i, is_vaccinated=False, infection=self.virus)
            for i in range(self.pop_size)
        ]
        return population


    def _simulation_should_continue(self):
        # This method will return a booleanb indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        should_continue =True
        if self.pop_size == self.total_vaccinated + self.total_dead:
            self.simulation_end_reason = 'Entire population is either vaccinated, has had the infection and is now immune, or has died'
            should_continue = False

        if self.total_infected == 0:
            self.simulation_end_reason = 'No more infections'
            should_continue = False

        should_continue = True
        return should_continue


    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        print(f"****Begin Simulation****\n Virus: {self.virus.name} | Initial Infected: {self.initial_infected}")
        self.logger.write_metadata(
            self.pop_size, 
            self.vacc_percentage, 
            self.virus.name, 
            self.virus.mortality_rate, 
            self.initial_infected
            )
        time_step_counter = 0
        should_continue = True

        while should_continue:
            # TODO: Increment the time_step_counter
            time_step_counter +=1
            # TODO: for every iteration of this loop, call self.time_step() 
            self.time_step()
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            should_continue = self._simulation_should_continue()

        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 
        self.logger.log_simulation_outcome(time_step_counter, self.pop_size, self.total_deaths, self.simulation_end_reason)

    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        pass

    def interaction(self, infected_person, random_person):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0.0 and 1.0.  If that number is smaller
            #     than repro_rate, add that person to the newly infected array
            #     Simulation object's newly_infected array, so that their infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        pass

    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the imulation
    virus = Virus(virus, pop_size, vacc_percentage, initial_infected)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    # sim.run()
