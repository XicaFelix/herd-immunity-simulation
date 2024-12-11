import random
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        """
        Initialize the simulation with the virus, population size, vaccination percentage,
        and the number of initially infected people.

        Attributes:
        - pop_size: Total number of people in the simulation.
        - virus: The virus object being used for the simulation.
        - vacc_percentage: Percentage of the population that is vaccinated.
        - initial_infected: Number of people initially infected with the virus.
        - logger: Logs all events during the simulation.
        """
        self.pop_size = pop_size  
        self.next_person_id = 0  
        self.virus = virus  
        self.initial_infected = initial_infected  
        self.vacc_percentage = vacc_percentage  
        self.infected_and_alive = 0  
        self.total_deaths = 0  
        self.population = self._create_population()  
        self.newly_infected = set()  
        self.dead_population = set() 
        self.total_interactions = 0
        self.death_interactions = 0
        self.num_steps = 0
        self.logger = Logger(f"{self.virus.name}_simulation_pop_{self.pop_size}_vacc_pcnt_{self.vacc_percentage}")

    def _create_population(self):
        """
        Create the initial population for the simulation. 
        - Some individuals are vaccinated based on `vacc_percentage`.
        - Some individuals are infected based on `initial_infected`.
        """
        # Determine who will be vaccinated
        num_vaccinated = int(self.pop_size * self.vacc_percentage)
        vaccinated_indices = set(random.sample(range(self.pop_size), num_vaccinated))

        # Create the population with vaccinated and infected individuals
        population = [
            Person(i, is_vaccinated=(i in vaccinated_indices)) if i >= self.initial_infected
            else Person(i, is_vaccinated=False, infection=self.virus)
            for i in range(self.pop_size)
        ]
        return population

    def _simulation_should_continue(self):
        """
        Determine whether the simulation should continue.
        The simulation ends if:
        - Everyone is either dead or immune (vaccinated).
        - No unvaccinated individuals are left alive in the population.
        """
        if self.pop_size == self.total_deaths + self.infected_and_alive:
            return False
        
        for person in self.population:
            if person.is_alive and not person.is_vaccinated:
                return True
        
        return False

    def run(self):
        """
        Run the simulation until it reaches an end condition.
        Log metadata, simulate each time step, and record the final outcomes.
        """
        print(f"****Begin Simulation****\n Virus: {self.virus.name} | Initial Infected: {self.initial_infected}")

        should_continue = True

        # Log metadata for the simulation
        self.logger.write_metadata(
            self.pop_size, 
            self.vacc_percentage, 
            self.virus.name, 
            self.virus.mortality_rate, 
            self.virus.repro_rate,
            self.initial_infected
        )
        self.num_steps = 0

        # Loop through each step of the simulation
        while should_continue:
            self.time_step()
            should_continue = self._simulation_should_continue()
            self.num_steps += 1
            self.logger.log_time_step(
                self.infected_and_alive, 
                self.total_deaths, 
                self.total_interactions, 
                pop_size=self.pop_size, 
                step=self.num_steps
            )

        # Log the final outcome of the simulation
        print('Log simulation completed')
        self.logger.log_simulation_outcome(self.num_steps, self.pop_size, self.total_deaths)

    def time_step(self):
        """
        Simulate one step in time. Handle interactions between individuals,
        update the status of infected individuals, and count deaths or new infections.
        """
        newly_dead = 0
        # List of healthy, non-infected people who are alive
        healthy_population = [p for p in self.population if p.is_alive and p.infection is None] 
        
        # Handle interactions for infected individuals
        for infected_person in (p for p in self.population if p.is_alive and p.infection):
            interactions = 0
            while interactions < 100 and healthy_population:
                random_person = random.choice(healthy_population)
                self.interaction(infected_person, random_person)
                self.total_interactions += 1
                interactions += 1

            # Check if the infected person survives the infection
            if infected_person.did_survive_infection():
                self.infected_and_alive -= 1
            else:
                if infected_person not in self.dead_population:
                    self.dead_population.add(infected_person)
                    self.total_deaths += 1
                    self.infected_and_alive -= 1
                    newly_dead += 1

        self.death_interactions += newly_dead
        self._infect_newly_infected()

    def interaction(self, infected_person, random_person):
        """
        Simulate an interaction between an infected person and a random person.
        If the random person is not vaccinated and not already infected, they
        have a chance to get infected based on the virus' reproduction rate.
        """
        if random_person.is_vaccinated or random_person.infection is not None:
            return
        if random.random() < self.virus.repro_rate:
            if random_person._id not in self.newly_infected:
                self.newly_infected.add(random_person)

    def _infect_newly_infected(self):
        """
        Infect individuals who were marked as newly infected during the time step.
        Clear the `newly_infected` list for the next step.
        """
        for person in self.newly_infected:
            person.infection = self.virus
            self.infected_and_alive += 1
        self.newly_infected.clear()

if __name__ == "__main__":
    # Virus details
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Simulation parameters
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Create and run the simulation
    sim = Simulation(pop_size=pop_size, vacc_percentage=vacc_percentage, initial_infected=initial_infected, virus=virus)
    sim.run()
