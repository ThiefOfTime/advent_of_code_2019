from dataclasses import dataclass
import numpy as np

@dataclass
class Moon:
    num_indirect_orbit: int
    moons: list
    name: str

    def get_num_orbited_planets(self):
        return (not self.name == "COM") + self.num_indirect_orbit + sum(moon.get_num_orbited_planets() for moon in self.moons)

    def get_distance_between_elements(self, element_1, element_2):
        if self.name == element_1 or self.name == element_2:
            return [self.num_indirect_orbit + 1, 0] if self.name == element_1 else [0, self.num_indirect_orbit + 1]
        res_tmp = [a for a in [moon.get_distance_between_elements(element_1, element_2) for moon in self.moons] if sum(a) > 0]
        if len(res_tmp) in [0, 1]:
            return res_tmp[0] if len(res_tmp) else [0, 0]
        else:
            return list(np.array(res_tmp[0], dtype=np.int) + np.array(res_tmp[1], dtype=np.int) - (self.num_indirect_orbit + 2))

    @staticmethod
    def build_system(indirect_orbits, start_name, orbits):
        moons = [moon.split(")")[1] for moon in orbits if moon.startswith(start_name + ")")]
        return Moon(num_indirect_orbit=indirect_orbits, name=start_name, moons=[Moon.build_system(indirect_orbits + 1 if not start_name == "COM" else 0, moon, orbits) for moon in moons])


with open("input.txt", "r") as d_file:
    system = Moon.build_system(0, "COM", [f.strip() for f in d_file])
    print(f"Part 1: {system.get_num_orbited_planets()}")
    print(f"Part 2: {sum(system.get_distance_between_elements('YOU', 'SAN'))}")
