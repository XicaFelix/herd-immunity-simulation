class Virus(object):
    # Properties and attributes of the virus used in Simulation.
    def __init__(self, name, repro_rate, mortality_rate):
        # Define the attributes of your your virus
        self.name = name
        # TODO Define the other attributes of Virus
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate
        pass


# Test this class
if __name__ == "__main__":
    # Test your virus class by making an instance and confirming 
    # it has the attributes you defined
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    # Test a virus with a high reproduction rate and low mortality rate
    flu = Virus("Flu", 1.5, 0.05)
    assert flu.name == "Flu"
    assert flu.repro_rate == 1.5
    assert flu.mortality_rate == 0.05

    # Test a virus with a low reproduction rate and high mortality rate
    ebola = Virus("Ebola", 0.4, 0.9)
    assert ebola.name == "Ebola"
    assert ebola.repro_rate == 0.4
    assert ebola.mortality_rate == 0.9

